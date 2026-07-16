# Azure Diagrams

**Azure Architecture Assistant** — turn Mermaid definitions or plain-language architecture descriptions into presentation-ready, editable draw.io diagrams with official Microsoft Azure and Power Platform icons, generated and refined conversationally inside Claude.

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Repo](https://img.shields.io/badge/github-juliopessan%2Fazure--diagrams--plugin-181717?logo=github)](https://github.com/juliopessan/azure-diagrams-plugin)

## What it does

- **`azure-diagram` Skill** — the full generation pipeline: narrative reconstruction, semantic zone-based layout (16:9 by default, extendable for dense architectures), four mandatory draw.io layers (`Zones`, `Connectors`, `Nodes`, `Annotations`), color-coded cards and connectors, anti-overlap/anti-crossing routing, validated official icons (`azure2` set via live shape search), legend strip, and a quality scorecard. All diagram content in EN-US.
- **draw.io MCP server** — connects the official `https://mcp.draw.io/mcp` endpoint, providing `create_diagram` (structural validation + interactive rendering, with optional `postLayout: "elk"` auto-layout or `routing: "libavoid"` obstacle-avoiding edge routing) and `search_shapes` (official icon discovery — no hard-coded/guessable icon paths).

## Usage

Ask Claude for an Azure diagram, paste a Mermaid flowchart, or say "convert this to draw.io." Outputs: a native, editable `.drawio` file (wrapped in a valid `mxfile` container), the source Mermaid/XML, an inline rendered preview, and a short summary of the design choices made.

Because generation happens inside the conversation, revisions are conversational too — for example:

- *"The connectors are cluttering the visual, reduce them."*
- *"Move Content Safety directly under the orchestrator."*
- *"Render this with cleaner obstacle-avoiding routing."*

Claude regenerates the XML, re-renders it through `create_diagram`, and reports exactly what changed.

## Repository layout

```
azure-diagrams/
├── .claude-plugin/plugin.json   # plugin manifest
├── .mcp.json                    # official draw.io MCP endpoint
├── skills/azure-diagram/        # the Skill: design system, layout rules, quality gates
├── examples/                    # end-to-end reference architecture, iterated v1 → v3
│   └── agentic-sales-intelligence/
├── docs/                        # project submission document (Claude edition)
├── CHANGELOG.md
└── LICENSE
```

## Reference example: Agentic Sales Intelligence Platform

`examples/agentic-sales-intelligence/` walks through a real end-to-end generation and revision cycle for a 30+ node Azure architecture (agent orchestration, model routing, data platform, ingestion, platform foundations):

| File | What it shows |
|---|---|
| `v1.drawio` | First render from the supplied Mermaid — 32 nodes, 41 connectors, 8 zones. |
| `v2.drawio` | Fixed legend overlap and detangled the Orchestration ↔ Model Layer connector fan. |
| `v3-final.drawio` | Decluttered on request — cross-cutting and duplicate edges removed, 41 → 34 connectors (-17%), rendered with `routing: "libavoid"`. |

Open any file directly in [draw.io](https://app.diagrams.net) or the desktop app.

## Install

```bash
git clone https://github.com/juliopessan/azure-diagrams-plugin.git
```

Then enable it as a Claude plugin (Cowork mode or Claude Code) pointing at the cloned folder — it ships its own `.mcp.json` wiring the official draw.io MCP endpoint, so no extra server setup is needed.

## Requirements

- Claude Desktop (Cowork mode) or Claude Code with plugin support.
- Internet access to `mcp.draw.io` (diagram rendering/validation) and `app.diagrams.net` (icon asset loading).

## Project submission

`docs/Azure-Architecture-Assistant-Claude-Edition.docx` is the full project write-up (use case, solution details, user journey, technology, KPIs, and roadmap), separating what's technically validated today from what's a pilot target.

## Contributing / versioning

See [CHANGELOG.md](CHANGELOG.md) for release history and known gotchas. Version follows the `plugin.json` manifest.

## License

[MIT](LICENSE) — see the license file for details.
