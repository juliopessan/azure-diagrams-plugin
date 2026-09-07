#!/usr/bin/env python3
"""Mechanical AZD audit for .drawio files.

Checks the subset of DIAGRAM-RULES.md that can be verified from geometry and
style strings alone. It does not replace the visual pass (AZD-006) or the MCP
structural check (AZD-005) — it catches the defects a human eye reliably misses:
off-page cells, wrong card sizes, missing anchors, zone overcrowding, legend
items that drifted out of their own box.

    python3 skills/azure-diagram/audit.py examples/**/*.drawio

Exit code is 1 if any Blocking violation is open, else 0.
"""
import re
import sys
import pathlib

BLOCKING = {
    'AZD-101', 'AZD-102', 'AZD-103', 'AZD-104', 'AZD-203',
    'AZD-302', 'AZD-306', 'AZD-402', 'AZD-403', 'AZD-504',
    'AZD-505', 'AZD-601', 'AZD-602', 'AZD-605',
}

# The title and signature sit in a header band above the content margin by
# design (see the shipped reference); exempt them from the margin check.
HEADER_IDS = {'title', 'sig', 'title1', 'title2'}


def parse(path):
    x = pathlib.Path(path).read_text()
    cells = []
    for m in re.finditer(r'<mxCell\b([^>]*)>\s*(?:<mxGeometry([^/]*)/>)?', x):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        geo = {k: float(v) for k, v in
               re.findall(r'(\w+)="([-\d.]+)"', m.group(2) or '')}
        cells.append((attrs, geo))
    return x, cells


def is_zone(a):
    """A zone is an unfilled dashed container - detect by style, never by id.
    (Naming zones z1.. vs zone1.. is free, so an id-prefix test silently
    misclassifies them and corrupts the whitespace figure.)"""
    s = a.get('style', '')
    return ('dashPattern=1 2' in s and 'fillColor=none' in s
            and not a.get('id', '').startswith('legend')
            and 'legendBox' not in a.get('id', ''))


def audit(path):
    x, cells = parse(path)
    out = []

    def flag(code, msg):
        out.append((code, msg))

    pw = float(re.search(r'pageWidth="(\d+)"', x).group(1))
    ph = float(re.search(r'pageHeight="(\d+)"', x).group(1))
    verts = [(a, g) for a, g in cells if a.get('vertex') == '1' and g]

    if 'background="#FFFFFF"' not in x:
        flag('AZD-101', 'no explicit background="#FFFFFF" (renders dark in some viewers)')
    if abs(pw / ph - 16 / 9) > 0.02:
        flag('AZD-102', f'canvas {pw:.0f}x{ph:.0f} is ratio {pw/ph:.3f}, not 16:9')
    if not re.search(r'<mxCell id="0"\s*/>', x) or 'id="1" parent="0"' not in x:
        flag('AZD-103', 'missing default cells id="0" / id="1"')

    layers = re.findall(r'value="(Zones|Connectors|Nodes|Annotations)"[^>]*parent="1"', x) \
        or re.findall(r'parent="1"[^>]*value="(Zones|Connectors|Nodes|Annotations)"', x)
    if layers != ['Zones', 'Connectors', 'Nodes', 'Annotations']:
        flag('AZD-104', f'layer order is {layers}')

    for a, g in verts:
        if a.get('id') in HEADER_IDS:
            continue
        if (g['x'] < 40 or g['y'] < 40
                or g['x'] + g['width'] > pw - 40 or g['y'] + g['height'] > ph - 40):
            flag('AZD-105', f'"{a["id"]}" outside the 40px margin '
                            f'(x {g["x"]:.0f}..{g["x"]+g["width"]:.0f}, '
                            f'y {g["y"]:.0f}..{g["y"]+g["height"]:.0f}, page {pw:.0f}x{ph:.0f})')

    for a, g in verts:
        s = a.get('style', '')
        if 'shape=label' in s and 'imageWidth=40' in s:
            for prop in ('rounded=1', 'arcSize=12', 'imageVerticalAlign=top', 'verticalAlign=bottom'):
                if prop not in s:
                    flag('AZD-203', f'"{a["id"]}" is not the standard card ({prop} missing)')
            # 130x96 is the default, not a hard size: AZD-506 asks for weight
            # variation, so a deliberate deviation is advisory, not blocking.
            if (g['width'], g['height']) != (130.0, 96.0):
                flag('AZD-209', f'"{a["id"]}" card is {g["width"]:.0f}x{g["height"]:.0f} '
                                f'(default 130x96 - intentional only if it encodes hierarchy, AZD-506)')

    for a, _ in cells:
        if a.get('edge') == '1':
            s = a.get('style', '')
            if not all(k in s for k in ('exitX', 'exitY', 'entryX', 'entryY')):
                flag('AZD-302', f'edge "{a["id"]}" has no explicit exit/entry anchors')

    if 'mscae' in x:
        flag('AZD-402', 'mscae library referenced (404s as an image)')

    zones = [(a, g) for a, g in verts if is_zone(a)]
    inner = [(a, g) for a, g in verts
             if not is_zone(a) and not a.get('id', '').startswith(('legend', 'leg'))
             and a.get('id') not in HEADER_IDS]
    for za, zg in zones:
        held = [a['id'] for a, g in inner
                if g['x'] >= zg['x'] and g['y'] >= zg['y']
                and g['x'] + g['width'] <= zg['x'] + zg['width']
                and g['y'] + g['height'] <= zg['y'] + zg['height']]
        label = (za.get('value', '') or za.get('id', ''))[:34]
        if not held:
            flag('AZD-504', f'zone "{label}" is empty')
        elif len(held) > 6:
            flag('AZD-502', f'zone "{label}" holds {len(held)} components (limit 6)')

    ink = sum(g['width'] * g['height'] for a, g in verts if not is_zone(a))
    ws = 100 * (1 - ink / (pw * ph))
    if ws < 40:
        flag('AZD-503', f'whitespace {ws:.1f}% is below the 40% floor')

    legend = [(a, g) for a, g in verts if a.get('id', '').startswith(('legend_', 'leg'))
              and 'legendBox' not in a.get('id', '')]
    box = next(((a, g) for a, g in verts if 'legendBox' in a.get('id', '')), None)
    for a, g in legend:
        s = a.get('style', '')
        iw = re.search(r'imageWidth=(\d+)', s)
        sl = re.search(r'spacingLeft=(\d+)', s)
        if iw and sl and int(sl.group(1)) < int(iw.group(1)):
            flag('AZD-602', f'"{a["id"]}" spacingLeft={sl.group(1)} does not clear '
                            f'its {iw.group(1)}px icon (label starts under the icon)')
    if box:
        bx, bg = box
        for a, g in legend:
            if not (g['x'] >= bg['x'] and g['y'] >= bg['y']
                    and g['x'] + g['width'] <= bg['x'] + bg['width']
                    and g['y'] + g['height'] <= bg['y'] + bg['height']):
                flag('AZD-605', f'legend item "{a["id"]}" is not inside the legend box '
                                f'(moving the items without moving the box)')

    return out, ws, sum(1 for a, _ in cells if a.get('edge') == '1'), len(verts)


def main(paths):
    worst = 0
    for p in paths:
        try:
            found, ws, edges, verts = audit(p)
        except Exception as exc:                       # noqa: BLE001
            print(f'\n=== {p} ===\n    could not audit: {exc}')
            worst = 1
            continue
        print(f'\n=== {pathlib.Path(p).name} ===')
        print(f'    {verts} vertices | {edges} edges | whitespace {ws:.1f}%')
        if not found:
            print('    0 open violations')
            continue
        blocking = [f for f in found if f[0] in BLOCKING]
        print(f'    {len(found)} open ({len(blocking)} blocking):')
        for code, msg in sorted(found):
            mark = 'BLOCKING' if code in BLOCKING else 'advisory'
            print(f'      [{mark}] {code}  {msg}')
        if blocking:
            worst = 1
    return worst


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
