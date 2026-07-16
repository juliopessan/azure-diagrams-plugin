# Changelog

All notable changes to this project are documented here.

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
