# Azure Diagrams

Turn Mermaid definitions or plain-language architecture descriptions into presentation-ready, editable draw.io diagrams with official Microsoft Azure and Power Platform icons.

## What it does
- **azure-diagram skill** — the full generation pipeline: narrative reconstruction, semantic 16:9 layout (1600×900), four draw.io layers, color-coded cards and connectors, anti-overlap routing, validated official icons (azure2 set), legend strip, and a 10/10 quality scorecard. All diagram content in EN-US.
- **draw.io MCP server** — connects the official `https://mcp.draw.io/mcp` endpoint, providing `create_diagram` (structural validation + interactive rendering) and `search_shapes` (official icon discovery).

## Usage
Ask for an Azure diagram, paste a Mermaid flowchart, or say "convert this to draw.io". Outputs: `.drawio` (editable), the source `.mmd`, and optional high-resolution PNG exports for PowerPoint.

## Requirements
Internet access to `mcp.draw.io` and `app.diagrams.net` (icon validation).
