# AgriModel local product UI review example

Session context: Wyatt asked to inspect `/Volumes/T7 Shield/AI_TRAVEL/agri-model-platform-nwafu-windows-complete` and produce reusable UI lessons for the team, with emphasis on page cleanliness and beauty.

## What made the workflow reusable

1. Memory first, but don't overfit it
   - Use `case-router` for product/design work.
   - Report whether memory hits are direct or adjacent.
   - In this case, memory had adjacent AI_TRAVEL / migration / agri-document cases but no direct AgriModel UI-design case, so the final document stated that clearly.

2. Inspect code and visual evidence together
   - Product docs: `README.md`, delivery docs, existing plans.
   - UI source: `frontend/src/index.css`, feature CSS, page components, route/constants files.
   - Visual evidence: delivery screenshots under `交付材料/页面截图/`.
   - Avoid analyzing only screenshots; CSS and component structure reveal reusable patterns such as tokens, breakpoints, and component contracts.

3. Structure the review by user task flow
   - Login / demo account selection.
   - Dashboard / model entry.
   - Core model workbench: input -> inference -> output.
   - Visual recognition: sample image -> upload -> detection evidence -> advice.
   - Statistics cockpit: summary metrics -> trend charts -> heatmap/table.
   - Settings/admin: left subnav -> section cards -> save/test states.

4. Extract design patterns, not only praise
   - Stable left navigation with Chinese label + English technical sublabel.
   - Dark command-center UI kept restrained with low-saturation panels, 1px borders, 8px radius, and sparse semantic accent colors.
   - Model pages share a two-column pattern: left input/control, right conclusion/evidence/details.
   - Results prioritize conclusion first, then visual evidence, then detailed metrics.
   - Default demo data is a first-class UI feature for research-model demos.
   - Statistics pages should tell an operational story before exposing tables.

5. Deliver as team guidance
   - Save a Markdown report into the target repo `docs/` when the user points at a local product repo.
   - Include: memory findings, inspected files, page notes, component patterns, CSS token candidates, and a checklist.
   - Keep the final user response short and state the output path.

## Checklist template for similar future reviews

- [ ] Run memory/case retrieval and classify hits as direct or adjacent.
- [ ] Inventory target repo and key UI files.
- [ ] Read global theme/tokens and feature/page styles.
- [ ] Read core page components and constants/navigation.
- [ ] Inspect screenshots or visual deliverables where available.
- [ ] Summarize by workflow/page type, not by raw file list.
- [ ] Produce a reusable team-facing Markdown document.
- [ ] Include a concrete landing checklist: information structure, visual cleanliness, typography, form organization, image/model output, statistics, responsive behavior, and delivery readiness.

## AgriModel-specific distilled UI lessons

- Research model demos become products when login, navigation, model entries, statistics, and delivery docs are unified.
- For complex model pages, use: hero/status -> left input/sample/forms -> right final result -> evidence -> metrics.
- Default samples reduce demo risk and should be visible near the input area.
- Visual AI pages should show annotated image evidence before long textual advice.
- Dark dashboards look cleaner when the palette is restrained: background layers, semantic accent colors, low-contrast borders, and consistent radius.
- Data dashboards need hierarchy: summary KPI cards, main trend chart, supporting heatmap/distribution/table.
