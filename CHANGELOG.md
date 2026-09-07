# Changelog

All notable changes to this project are documented here.

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
