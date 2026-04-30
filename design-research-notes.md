# Design research notes

Current portfolio direction follows these public-facing patterns:

- Product-first presentation: live demos and product surfaces appear before long explanation.
- Persona/evaluator routing: reviewers can choose the path that matches what they need to verify.
- Outcome -> mechanism -> proof: claims are paired with the system mechanism and reviewable evidence.
- Bento/signal boards: small proof blocks make capability range scannable.
- Interactive proof: static pages include small runnable flows where possible instead of only screenshots.

Sources reviewed on 2026-04-29:
- SaaS homepage/demo pattern articles emphasized interactive demos, persona routing, product-first storytelling, and structural clarity.
- UX/design portfolio examples emphasized distinct art direction without disrupting the viewer experience, simple project-focused layouts, and direct purpose-driven communication.
- Engineering/system-design references emphasized showing architecture, scale/constraint thinking, and decision tradeoffs rather than only screenshots.

## Architecture proof layer

Additional research emphasized that advanced engineering presentation should make constraints and tradeoffs visible. Architecture Decision Records and tradeoff analysis are useful because they capture context, alternatives, consequences, and risk. The portfolio now includes a Systems Atlas to make those decisions inspectable without exposing private production code.

Sources reviewed on 2026-04-29:
- CMU/SEI Architecture Tradeoff Analysis Method materials.
- Recent ADR/tradeoff writing about documenting context, alternatives, and consequences.
- Software architecture portfolio examples that foreground deep-dive case studies, architecture diagrams, and decision rationale.

## Non-generic proof direction

To avoid sounding like a generic portfolio, the public work should keep replacing broad claims with concrete decision records:

- What constraint shaped the system?
- What decision was made?
- What tradeoff did that create?
- What public proof shows the decision in code or output?

This pass added repo-native ADR folders to SquadBrain and Lasting Ground so the Systems Atlas links to durable implementation-adjacent decision records.
# Design research notes

## 2026-04-29 visual correction research pass

Sources reviewed:
- Reddit portfolio critiques in r/webdev and r/UI_Design.
- GitHub curated portfolio repositories and portfolio inspiration lists.
- GitHub README research on how popular projects use images, lists, and links.

Lessons applied in this pass:

1. Project images need separation from the page.
   Reddit critique repeatedly flags cards/images that lack contrast from the background. If the page uses a pale gradient, images need a darker stage, visible border, or browser/device frame instead of floating softly into the page.

2. Do not use decorative graphics if they do not clarify the product.
   GitHub portfolio lists show lots of visual variety, but the useful pattern for this portfolio is not maximal animation. It is a clean proof surface with richer screenshots, strong hierarchy, and obvious routes into demos/source.

3. Keep the front page curated.
   Reddit feedback consistently punishes portfolios that show too much text or too many weak projects. This portfolio should keep SquadBrain and Lasting Ground prominent, and make the visual proof for those two builds stronger rather than adding filler projects.

4. Make images feel like product artifacts.
   GitHub/portfolio examples often use thumbnails, live previews, and device/browser frames. For this portfolio, system graphics should sit inside premium artifact frames with labels, not blend into the page as flat illustrations.

5. README/project proof should stay visual and linked.
   README research indicates popular projects tend to be organized with lists, images, and external links. The public repos already have tests/docs; the next visual layer should make those artifacts easier to scan and click.

Changes this research supports:
- Darken and frame the main portfolio visual proof section.
- Give SVG graphics stronger contrast against their cards.
- Add browser/device-style chrome and artifact labels.
- Strengthen project image treatments so GIF/PDF previews read as product screenshots.
- Keep copy concise and route quickly to live demos, case studies, and GitHub proof.

## 2026-04-29 advanced responsive QA pass

Additional research-supported rules applied:

1. Mobile should not be a shrunken desktop composition.
   Portfolio critique patterns on Reddit punish horizontal clipping, oversized headings, and decorative sections that only work on desktop. The mobile version now uses explicit headline rhythm, one-column navigation, and narrower artifact cards.

2. Proof visuals need a safe reading measure.
   GitHub project pages and strong portfolio examples rely on screenshots that remain readable in constrained widths. The revised mobile layout uses an inset 330px proof column instead of forcing wide desktop cards into a phone viewport.

3. Navigation must be readable before it is clever.
   Mobile nav pills now stack into full-width rows rather than clipping labels in a compressed two-column layout.

4. Headline wrapping should be designed, not left to browser luck.
   The main portfolio, Systems Atlas, and Lasting Ground hero headlines now use deliberate line breaks so the first impression is clean on mobile and desktop.
