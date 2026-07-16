---
name: azure-diagram
description: Generate 16:9 draw.io architecture/flow diagrams with official Azure and Power Platform icons, from Mermaid definitions or plain-language descriptions. Use when the user asks for an Azure diagram, a .drawio file, an architecture diagram for PowerPoint, to convert Mermaid to draw.io, or mentions "diagrama Azure" / "draw.io".
---

# Azure Diagram Generator (draw.io)

Produce a native, editable `.drawio` file in Microsoft Architecture Center style with color-coded semantics, ready to paste into 16:9 PowerPoint slides. ALL diagram content (labels, zone titles, legend) MUST be in EN-US.

## Core philosophy

Architecture diagrams are communication artifacts: the objective is to EXPLAIN a solution, not to reproduce Mermaid. When visual fidelity conflicts with Mermaid positioning, readability always wins. A CIO should understand the architecture within five seconds by following the visual flow alone. The result must look manually designed by a Principal Azure Architect for the Azure Architecture Center — minimal, technical, quiet, precise, balanced.

## Pipeline

0. **Narrative reconstruction (before drawing anything)** — understand the business process → identify the primary narrative → separate supporting processes → separate exception handling → separate operational concerns → only then create the layout. Common narratives: Email Processing (Reception → Classification → Decision → Routing → Human Review → Audit); RAG (Query → Retrieval → Prompt Assembly → LLM → Response); Agentic AI (User → Orchestrator → Agents → Tools → Aggregation → Response); Data Platform (Sources → Ingestion → Processing → Storage → Analytics → Consumption); API Platform (Consumer → Gateway → Auth → Services → Data).
1. **Parse the source** — Mermaid definition or description. Mermaid defines logical components, dependencies, order and boundaries — NOT coordinates, routing, grouping or containers. Layout is SEMANTIC. Save the source `.mmd` next to the `.drawio`.
2. **Validate every icon before use** — `curl -s -o /dev/null -w "%{http_code}" https://app.diagrams.net/<path>`; only use paths returning 200. To discover shapes, prefer the draw.io MCP `search_shapes` tool (server `drawio` → https://mcp.draw.io/mcp) before falling back to a proxy icon.
3. **Compose the XML** following the layout and style rules below.
4. **Validate with the draw.io MCP** — call `create_diagram` with the `<mxGraphModel>` content (no XML comments allowed). Fix every reported error.
5. **Verify visually** — render via a local `preview.html` embedding `https://viewer.diagrams.net/js/viewer-static.min.js`, screenshot it, and inspect for overlaps BEFORE delivering. Check that every icon, label and connector is attached to the intended component.

## Canvas & layers (mandatory)

- 16:9: `pageWidth="1600" pageHeight="900"`, 40px margins, single page.
- Cells `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>` (default layer required by the MCP validator), then 4 named layers in stacking order: `Zones` → `Connectors` → `Nodes` → `Annotations`.

## Layout (anti-clutter)

- Primary flow LEFT → RIGHT on the top band, grouped into 3–5 phase zones; exceptions & human review in a bottom band spanning the width. One dominant flow per diagram — secondary flows must never compete visually with it.
- One icon per service. Long return edges routed OUTSIDE the zones through reserved corridors (e.g. y≈490–505 between bands, 20px gaps between zones).
- **Component density**: 3–6 services per visual region; if a region exceeds six, split it or introduce a container. Never create empty zones/containers, and never create containers just because Mermaid has subgraphs — merge related services.
- **Whitespace target 40–55%**: prefer expanding the layout over compressing services; the canvas must never look crowded.
- **Decisions**: inline with the primary flow, never diagonal, with symmetric outgoing branches when possible. **Retry blocks** grouped and visually close to the operation they protect. **Human review** visually isolated (lower-right or lower-center), clearly reading as an exception process. **Monitoring/logging/governance** peripheral — never in the middle of the story.
- **Visual hierarchy by weight**: largest — users, applications, core AI; medium — data platform, integration; smallest — monitoring, logging, security, governance.
- **Capability-based grouping** when it improves readability: group services by architectural capability (e.g. "AI Platform" = Azure OpenAI + AI Search + Content Safety + Document Intelligence), so the reader recognizes capabilities before reading individual services.

## Anti-overlap protocol (mandatory)

- Arrows NEVER cross any text. Labels live INSIDE node cells, so edges attach to cell borders below the text.
- Explicit `exitX/exitY/entryX/entryY` on all edges; explicit waypoints for long routes through free corridors; parallel edges offset ≥10px; edge×edge crossings perpendicular only and only when unavoidable.
- Edge labels anchored near their origin (`<mxGeometry x="-0.5..-0.9" relative="1">`), always `labelBackgroundColor=#FFFFFF`.

## Visual style

- **Zone**: no fill, dotted gray border `dashed=1;dashPattern=1 2;strokeColor=#999999`, title top-center, fontSize 13.
- **Service node**: rounded CARD (`rounded=1;arcSize=12`), colored border + soft fill, official icon (40px) top-center with the label inside the same cell:
  `shape=label;html=1;whiteSpace=wrap;imageAlign=center;imageVerticalAlign=top;imageWidth=40;imageHeight=40;verticalAlign=bottom;align=center;fontSize=11;spacingBottom=6;image=<validated path>` — cell 130×96.
- **Color semantics** (border / fill): green `#2E9E4F/#F1FAF4` start·end·confirmations·happy path; blue `#2E77D0/#F2F7FD` standard processes; purple `#7C4DC4/#F7F3FC` AI·retry·analyst·Power Apps; orange `#E8871A/#FEF7EF` escalation·manual triage·business rules·override log; red `#D64550/#FDF3F4` exception queues·failures.
- **Decisions**: white rhombus, border in context color. **Terminals**: green rounded pills.
- **Edges**: orthogonal, `strokeWidth=1.5`. Two color modes:
  - *Flowchart mode* (decision/status flows): dark gray `#333333` normal flow; **red** exception flows; **red dashed** low confidence; **orange** escalation/manual review; **purple dashed** retry-returns to the main flow.
  - *Architecture mode* (service topology): dark gray business flow; **teal `#0E7C7B`** data flow / AI interaction; **purple** integration; **orange** events/messaging; **gray dashed** security, governance, monitoring and other cross-cutting concerns.
- **Edge labels**: bold + colored — Yes/Approved/High green, No/Low red, Medium/Manual review orange, analyst actions purple/blue.
- **Node labels**: max 3 lines × ~18 characters per line; break long names naturally; official Microsoft terminology; names, not descriptions. Labels never dominate icons; icon size identical throughout.
- **Legend strip** at the bottom: dotted box with 20px mini-icons + official service names; proxy icons marked `*`.
- Title top-left (fontSize 18 bold); signature "Microsoft Azure · Power Platform" top-right.
- Numbered green badges (`#54812D`, 28px) are OPTIONAL — only when the audience needs 1-2-3 narration.

## Icon library (pre-validated, azure2 set)

Official: `img/lib/azure2/power_platform/CopilotStudio.svg`, `.../power_platform/Dataverse.svg`, `.../power_platform/PowerApps.svg`, `.../power_platform/PowerAutomate.svg`, `.../ai_machine_learning/Azure_OpenAI.svg`, `.../analytics/Log_Analytics_Workspaces.svg`, `.../app_services/Notification_Hubs.svg`, `.../integration/Service_Bus.svg` (use for queues), `.../integration/Logic_Apps.svg`, `.../compute/Function_Apps.svg`, `.../identity/Users.svg`, `.../general/Error.svg`, `.../general/Recent.svg` (retry).

Proxies (no official image exists — mark with `*` in the legend): Microsoft Graph → `img/lib/azure2/identity/Azure_Active_Directory.svg`; Shared Mailbox/email → `img/lib/azure2/other/Azure_Communication_Services.svg`.

The `mscae` library is NOT served as images (404) — never use `img/lib/mscae/...`. Stencil shapes (`mxgraph.mscae.*`) place labels outside the cell and break the anti-overlap rule — avoid.

## Architecture smells — auto-correct before delivering

Crossing arrows · duplicate services · misaligned icons · uneven spacing · oversized containers · crowded regions (>6 components) · empty regions · poor hierarchy · inconsistent icon sizes · labels over 3×18 · multiple competing flows.

## Final validation scorecard

Before delivering, self-score each category and keep optimizing until ALL are 10/10: grid alignment · visual balance · whitespace (40–55%) · layer/zone organization · primary flow clarity · exception flow separation · connector simplicity · Microsoft style · official icon usage · executive readability (5-second test). Also verify: AI components visually distinct from business logic; human interaction isolated from automated processing; the business story obvious without reading every label.

## Reference implementation

See `examples/agentic-sales-intelligence/` in this repo for a working example with all rules applied.
