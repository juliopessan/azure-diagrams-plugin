# DIAGRAM-RULES — the `AZD-xxx` rule table

Canonical diagnostic codes for the `azure-diagram` Skill. `SKILL.md` states the rules in
prose and stays the authority on *how* to build a diagram; this file assigns each rule a
stable code so a review can say **"0 open AZD violations"** instead of "looks good."

Cite the code whenever you fix something — `fixed AZD-301: label overlapped the main
arrow — re-anchored` — so a diff between two versions of a diagram is auditable rather
than anecdotal.

## Ranges

| Range | Domain |
|---|---|
| `AZD-0xx` | Pipeline & setup |
| `AZD-1xx` | Canvas & layers |
| `AZD-2xx` | Visual style |
| `AZD-3xx` | Anti-overlap |
| `AZD-4xx` | Icons |
| `AZD-5xx` | Layout & narrative |
| `AZD-6xx` | Language & legend |

## Severity

- **Blocking** — do not deliver with this open. These are the rules whose violation makes
  a diagram wrong or unreadable, not merely imperfect.
- **Advisory** — fix unless there is a reason worth stating out loud. If you ship an open
  advisory, say which one and why in the delivery note.

---

## `AZD-0xx` — Pipeline & setup

| Code | Rule | Severity |
|---|---|---|
| `AZD-001` | The source `.mmd` is saved next to the `.drawio` | Blocking |
| `AZD-002` | The mode is declared in one line before composing XML (`Mode: Architecture — layered service system`) | Blocking |
| `AZD-003` | No unimplemented mode is attempted (Sequence, Data Flow, Lifecycle) — fall back to Flowchart or Architecture and disclose the limitation | Blocking |
| `AZD-004` | Narrative reconstruction ran before layout — the business process was understood, not just the Mermaid graph | Blocking |
| `AZD-005` | The diagram was validated through the draw.io MCP `create_diagram` and every reported error fixed | Blocking |
| `AZD-006` | A visual verification pass happened before delivery — the render was actually looked at | Blocking |
| `AZD-007` | No XML comments in the `mxGraphModel` passed to `create_diagram` (the validator rejects them) | Blocking |

## `AZD-1xx` — Canvas & layers

| Code | Rule | Severity |
|---|---|---|
| `AZD-101` | `mxGraphModel` carries an explicit `background="#FFFFFF"` — without it the diagram renders dark in some viewers | Blocking |
| `AZD-102` | Canvas is 16:9 and a single page. `1600×900` is the default; dense architectures may extend the canvas (the shipped `agentic-sales-intelligence` reference runs at `2200×1240`) as long as the ratio and the 4-layer contract hold | Blocking |
| `AZD-103` | Default cells `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>` are present (required by the MCP validator) | Blocking |
| `AZD-104` | The four named layers exist in stacking order: `Zones` → `Connectors` → `Nodes` → `Annotations` | Blocking |
| `AZD-105` | All content sits inside the 40px page margin | Advisory |

## `AZD-2xx` — Visual style

| Code | Rule | Severity |
|---|---|---|
| `AZD-201` | Connectors use the palette of the declared mode, not one flat style for everything | Blocking |
| `AZD-202` | Zones are unfilled with a dotted gray border (`dashed=1;dashPattern=1 2;strokeColor=#999999`), title top-center at fontSize 13 | Advisory |
| `AZD-203` | Service nodes use the standard card **format**: `rounded=1;arcSize=12`, 40px icon top-center, label inside the same cell | Blocking |
| `AZD-204` | Node border/fill comes from the five semantic pairs (green, blue, purple, orange, red) — no invented colors | Advisory |
| `AZD-205` | Edges are orthogonal at `strokeWidth=1.5` | Advisory |
| `AZD-206` | Node labels are names, not descriptions — max 3 lines × ~18 characters, official Microsoft terminology | Advisory |
| `AZD-207` | Icon size is identical across every node | Advisory |
| `AZD-208` | Title (top-left, fontSize 18 bold) and signature (top-right) are present | Advisory |
| `AZD-209` | Card size is the 130×96 default. Deviating is allowed only where it encodes hierarchy per `AZD-506`, and the icon size still never changes (`AZD-207`) | Advisory |

## `AZD-3xx` — Anti-overlap

| Code | Rule | Severity |
|---|---|---|
| `AZD-301` | **Arrows never cross text.** The most common violation | Blocking |
| `AZD-302` | Every edge declares explicit `exitX/exitY/entryX/entryY` | Blocking |
| `AZD-303` | Parallel edges are offset by ≥10px | Advisory |
| `AZD-304` | Edge×edge crossings are perpendicular and only where unavoidable | Advisory |
| `AZD-305` | Edge labels are anchored near their origin and carry `labelBackgroundColor=#FFFFFF` | Advisory |
| `AZD-306` | No node or zone geometry overlaps another | Blocking |

## `AZD-4xx` — Icons

| Code | Rule | Severity |
|---|---|---|
| `AZD-401` | Every icon path was validated before use — resolved via `search_shapes` or confirmed HTTP 200. Never guessed | Blocking |
| `AZD-402` | No `mscae` usage — `img/lib/mscae/...` 404s, and `mxgraph.mscae.*` stencils place labels outside the cell, breaking `AZD-301` | Blocking |
| `AZD-403` | Proxy icons (no official asset exists) are marked `*` in the legend | Blocking |
| `AZD-404` | One icon per service; no duplicate service nodes | Advisory |

## `AZD-5xx` — Layout & narrative

| Code | Rule | Severity |
|---|---|---|
| `AZD-501` | Layout follows the business narrative, not the Mermaid source order. Mermaid supplies components and dependencies — never coordinates, grouping or containers | Blocking |
| `AZD-502` | No visual region holds more than 6 components — split it or introduce a container | Advisory |
| `AZD-503` | Whitespace stays in the 40–55% band — expand the layout rather than compress services | Advisory |
| `AZD-504` | No empty zones, and no container created merely because Mermaid had a subgraph | Blocking |
| `AZD-505` | One dominant flow — secondary flows never compete with it visually | Blocking |
| `AZD-506` | Visual hierarchy by weight: users/apps/core AI largest, monitoring and governance peripheral — never mid-story | Advisory |
| `AZD-507` | Human review and exception paths are visually isolated, reading clearly as exceptions | Advisory |

## `AZD-6xx` — Language & legend

| Code | Rule | Severity |
|---|---|---|
| `AZD-601` | All diagram content — labels, zone titles, legend — is EN-US | Blocking |
| `AZD-602` | Legend icons do not overlap their labels (`spacingLeft` must clear the icon width — an 18px icon needs `spacingLeft=24`) | Blocking |
| `AZD-603` | A legend strip is present and every shipped icon appears in it | Advisory |
| `AZD-604` | Service names use official Microsoft product naming | Advisory |
| `AZD-605` | Every legend item sits inside the legend box. Moving the entries without moving the box leaves them floating outside it | Blocking |

---

## The delivery gate — run this every time

Not a checklist to read and feel good about: three gates, run in order, on every
diagram before it is handed over. Each catches a class the others cannot.

**Gate 1 — structure (`AZD-005`).** Pass the `<mxGraphModel>` to the draw.io MCP
`create_diagram`. Fix everything it reports. This proves the file parses and renders;
it proves nothing about whether the diagram is any good.

**Gate 2 — mechanics (`audit.py`).** Run the checker next to this file:

```bash
python3 skills/azure-diagram/audit.py path/to/diagram.drawio
```

It exits non-zero on any Blocking violation, so it drops straight into CI or a
pre-commit hook. It reads geometry and style strings, which is exactly where the eye
is unreliable: a legend entry 67px off the page edge, `spacingLeft` that does not clear
its own icon, an edge missing its anchors, a zone quietly holding seven services.

**Gate 3 — the eye (`AZD-006`).** Render and look at it. Gates 1 and 2 cannot see
crossing connectors, a tangled fan, or a diagram that is structurally perfect and still
unreadable. **If you could not actually look at the render, say so in the delivery
instead of implying the pass happened.**

Then deliver with the open violations stated, not buried — including the advisories you
chose to leave open and why.

### Writing checks: two failure modes that have already bitten

Both were found in this repo, by checks that reported clean while missing real defects:

- **Never identify a cell class by id prefix.** A check keyed on `legend_*` silently
  skipped a diagram whose entries were named `leg1..leg15`, and every one of them had a
  broken `spacingLeft`. Zones named `z1..z5` instead of `zone1..` were counted as ink
  and corrupted the whitespace figure. Match on structure — style properties — never on
  naming convention.
- **Verify the checker before trusting its output.** The first run of this audit flagged
  the title and signature as margin violations; they sit in the header band by design.
  A checker that cries wolf gets ignored, which is worse than no checker. Confirm each
  finding is real before acting on it or reporting it.

### Auditing an already-shipped diagram

The gate above is non-destructive, so it runs against shipped files without
regenerating them — it produces a compliance report, not a new diagram.

This is how `examples/agentic-sales-intelligence/` was audited under v0.2.0: the pass
surfaced four real defects (`AZD-101`, `AZD-201`, `AZD-602`, `AZD-001`) in a diagram
shipped under v0.1.0, before the rule set existed. Re-running the mechanical gate in
v0.2.2 found a fifth it had missed — the last legend entry rendering off the page edge
(`AZD-105`) — and a matching pair of defects in `examples/solution-platform/`. A rule
set earns trust by continuing to find things, not by reporting clean.

## Provenance

The codes `AZD-001`, `101`, `201`, `301`, `401`, `402`, `501`, `502`, `503` and `602` are
load-bearing — they have been cited in shipped work and appear in
[`CHANGELOG.md`](../../CHANGELOG.md). The remaining entries formalize rules that already
existed in prose in [`SKILL.md`](SKILL.md); they gained a code here, not new authority.
When the two files disagree, `SKILL.md` wins and this table is the bug.
