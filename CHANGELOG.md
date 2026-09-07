# Changelog

All notable changes to this project are documented here.

## [0.2.2] — 2026-09-07

### Added
- **`skills/azure-diagram/audit.py`** — the `AZD` audit as a runnable tool instead of a manual read-through. Checks 14 codes mechanically from geometry and style strings; exits non-zero on any Blocking violation, so it drops into CI or a pre-commit hook.
- **The delivery gate** (`DIAGRAM-RULES.md`) — three gates that run on every diagram: MCP structural check → `audit.py` → the eye. Written down with what each one *cannot* catch, and the rule that a visual pass which did not happen must be declared, not implied.
- **`examples/agentic-sales-intelligence/agentic-sales-intelligence-v1-41-connectors.drawio`** — the pre-declutter v1 the v0.1.0 entry describes but never kept. Regenerated from the original 41-edge Mermaid and validated through the MCP. Both files now ship, so the −17% connector claim can be verified by counting rather than trusted.
- `AZD-209` (card size is the 130×96 default, deviation allowed only where it encodes hierarchy) and `AZD-605` (legend items must sit inside the legend box).

### Fixed
- **`AZD-602` in `examples/solution-platform`** — all 15 legend entries had `spacingLeft=4` against an 18px icon, so every label began underneath its own icon. This is the same defect the v0.2.0 audit fixed in the other example; it was reintroduced in 0.2.1 and the first checker missed it because it matched legend cells by the id prefix `legend_`, while these are named `leg1..leg15`.
- **`AZD-105` in `examples/agentic-sales-intelligence`** — the last legend entry sat at x=2127..2267 on a 2200px page, rendering "Azure Monitor" off the page edge and outside the legend box. All 15 entries re-pitched from 148px to 140px.
- **`AZD-101`/`AZD-105` in `examples/solution-platform`** — no explicit white background, and a legend strip running past the bottom margin.
- **`AZD-203` contradicted `AZD-506`** — the rule demanded a fixed 130×96 card while `AZD-506` asks for weight variation by role. `AZD-203` now governs the card *format*; size moved to advisory `AZD-209`. Second rule-table contradiction found and fixed after `AZD-102` in 0.2.1; both came from writing a rule stricter than the Skill it documents.

### Notes
- Both shipped examples now pass with 0 Blocking violations. Two advisories are left open deliberately: the Content Safety card at 110×80 (`AZD-209`, encodes hierarchy) and the Agent Orchestration zone holding 7 components (`AZD-502`).
- GitHub Pages cannot be enabled from CI: `actions/configure-pages` with `enablement: true` fails as `Resource not accessible by integration`, because the default `GITHUB_TOKEN` may not create a Pages site. The flag was removed and the one manual setting is documented in the README.

## [0.2.1] — 2026-09-07

Documentation and packaging pass. No change to diagram generation, the visual system, or any shipped `.drawio`.

### Added
- **`skills/azure-diagram/DIAGRAM-RULES.md`** — the canonical `AZD-xxx` rule table, which both `SKILL.md` and the README had been pointing at since v0.2.0 without it existing in the repo. 33 codes across the seven documented ranges, each with a **Blocking** or **Advisory** severity, plus the non-destructive audit workflow written down as a procedure. Codes already cited in shipped work (`001`, `101`, `201`, `301`, `401`, `402`, `501`, `502`, `503`, `602`) are marked as load-bearing; the rest formalize rules that already existed in prose in `SKILL.md` and gained a code, not new authority.
- **`docs/index.html`** — a self-contained landing page (single file, no build step, no runtime dependencies) for GitHub Pages. Verified in Chromium: computed bar widths 425px/353px (100%/83%), count-up settling on 41/34, all seven reveal targets reaching `.is-in`, rail and scroll-progress transforms applied, zero `!important`, balanced markup, both extracted scripts passing `node --check`.

### Fixed
- **Dead reference in the Skill** — `SKILL.md` pointed its "Reference implementation" at `azure-diagrams/email-triage-copilot.drawio` "in the juliopessan repo", a path that does not exist in this repository. Now points at the two examples that actually ship here.
- **Unverifiable evidence in the README** — the v0.2.0 audit claim cited a `Legal Document Automation` reference that is not in this repository, so no one cloning it could check the claim. Rewritten to cite the audit that *is* reproducible here: `examples/agentic-sales-intelligence/`, including the four defects the pass actually found rather than only its clean end state.
- **`examples/solution-platform/` was invisible** — the example was committed but appeared in neither the README's examples section nor its repository-layout tree. Documented, with its counts verified against the file (16 nodes, 5 zones, 13 connectors) and its two proxy icons called out.
- **Stale version narrative** — the "Where this is going" section still described v0.1.0 as the current state while the badge and manifest read v0.2.0. Rewritten for the current state, and extended with an explicit list of what is *not* done: three unimplemented modes, no automated test suite, no timing study and therefore no hours-saved claim.

## [0.2.0] — 2026-07-30

### Added
- **`AZD-xxx` rule-code taxonomy** — every design-system rule now has a stable diagnostic code (`AZD-0xx` pipeline/setup, `1xx` canvas & layers, `2xx` visual style, `3xx` anti-overlap, `4xx` icons, `5xx` layout & narrative, `6xx` language & legend). Self-correction and review cite the code instead of free-form prose (e.g. *"fixed AZD-301: label overlapped the main arrow — re-anchored"*), making "0 open violations" a reportable, auditable claim instead of a vibe.
- **Explicit mode selection** — before narrative reconstruction, the Skill now declares which of the two implemented modes applies (**Flowchart** for decision/status flows, **Architecture** for system topology) and states it in one line before composing the XML. Sequence, Data Flow and Lifecycle modes are documented as roadmap — not implemented — so the Skill discloses the limitation instead of attempting an unsupported diagram type.
- **Non-destructive audit workflow** — an existing `.drawio` can now be re-validated against the current rule set (structural check via `create_diagram` + a full `AZD-xxx` pass) without regenerating it, producing a compliance report. Verified on the `Legal Document Automation` reference diagram: 0 open violations, no changes required.

### Notes
- Purely additive: canvas, layers, visual style, icon catalog and every previously shipped diagram are unchanged. Only self-review and diagnostics got more precise.
- Ideas partly inspired by [archify](https://github.com/tt-a1i/archify) (named validation rules, mode-first authoring) — evaluated and adapted, not adopted wholesale (its icon-less/dark-theme visual language was intentionally not carried over; official Microsoft iconography remains a hard requirement here).

### Fixed — `examples/agentic-sales-intelligence` audited against v0.2.0 (2026-07-30)

Running the new AZD-xxx checklist against the shipped reference example (built in an earlier Cowork session, before the rule set existed) surfaced three real defects it did not previously catch:

- **`AZD-101`** — `mxGraphModel` had no explicit `background="#FFFFFF"`; the example rendered dark in some viewers. Added.
- **`AZD-201`** — all 34 connectors shared one flat gray/dashed style regardless of meaning, instead of the documented Architecture-mode palette. Recolored: 6 gray `#333333` (business flow: user → UI → gateway → app), 22 teal `#0E7C7B` (data/AI: app/orchestrator/agents/models, functions → data stores), 6 orange `#E8871A` (ingestion/eventing: sources → Data Factory/Functions, intent → Service Bus). Switched from dashed to solid per the same rule.
- **`AZD-602`** — all 15 legend entries had `spacingLeft=6` against an 18px icon, so every icon overlapped its own label's first letter. Corrected to `spacingLeft=24`.
- **`AZD-001`** — no companion Mermaid source existed for this example. Added `agentic-sales-intelligence.mmd`, reconstructed to match the shipped topology exactly (39 nodes, 34 edges).

`preview.png` regenerated to reflect all four fixes. Zone geometry was independently re-verified with no overlaps found (`Agent Orchestration` right edge at x=1580, `Model Layer` left edge at x=1620 — 40px clear). One cosmetic note: the "Model Layer" zone title renders with slightly soft edges in this specific headless-capture pipeline versus the other seven zone titles; the underlying geometry and style are identical to the others and the text is unaffected in the interactive draw.io viewer — flagged for future investigation, not blocking.

## [0.1.0] — 2026-07-16

### Added
- Initial packaging as a Claude plugin: `.claude-plugin/plugin.json`, `.mcp.json` (official `https://mcp.draw.io/mcp` endpoint).
- `azure-diagram` Skill: semantic zone-based layout, Microsoft naming, official `azure2` icon resolution via `search_shapes`, four-layer draw.io contract (Zones, Connectors, Nodes, Annotations), quality scorecard.
- Reference architecture example (`examples/agentic-sales-intelligence/`) generated end-to-end inside Claude (Cowork mode), demonstrating three iterations of visual QA:
  - **v1** — first render from the supplied Mermaid; 32 nodes, 41 connectors, 8 zones.
  - **v2** — fixed legend icon/label overlap and detangled the Agent Orchestration ↔ Model Layer connector fan by swapping the Model Router and Model row positions; widened inter-zone corridors.
  - **v3 (final)** — decluttered connectors on explicit user request: removed 3 cross-cutting dashed lines (UI→Entra ID, App→Key Vault, App→Monitor, now communicated via the zone label instead of wiring), 2 duplicate Orchestrator→Data Platform edges, and 2 Service Bus async return-loop edges. Net: 41 → 34 connectors (-17%), rendered with `routing: "libavoid"` for obstacle-avoiding orthogonal routing.
- `docs/Azure-Architecture-Assistant-Claude-Edition.docx` — full project submission document (Use Case, Details, Journey, Technology, Metrics, Roadmap), adapted from a Codex-plugin template to this Claude plugin, using validated evidence from the build above.
- `LICENSE` (MIT).

### Known gotchas (fixed during development, documented for future contributors)
- `create_diagram` requires **raw, unescaped** `<`/`>` characters in the `xml` parameter — passing HTML-escaped entities (`&lt;`/`&gt;`) fails with "Could not extract draw.io XML from input".
- MCP tool schemas can drop mid-session if the server reconnects; reload via `ToolSearch` (`select:mcp__plugin_azure-diagrams_drawio__create_diagram,...`) before retrying.
