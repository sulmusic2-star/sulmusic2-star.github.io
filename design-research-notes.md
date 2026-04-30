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

5. README and implementation evidence should stay visual and linked.
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

## 2026-04-30 portfolio advancement pass

Current design direction applied:

1. Treat the portfolio as an evaluator product, not a poster.
   The strongest modern portfolio pattern is a fast proof route: what it is, what works, what can be inspected, and where the claims are bounded. Added an inspection board that routes directly to demos, architecture, lab, code examples, ADRs, and sample artifacts.

2. Use bento layout only when it clarifies priority.
   Bento cards can become generic fast. The new board uses one dominant dark control card and four smaller proof tiles so the hierarchy is obvious: first understand the work, then inspect evidence.

3. Motion should be quiet and nonessential.
   Added a subtle reduced-motion-safe pulse to the inspection board, not animated clutter. It improves polish without becoming the product.

4. Links are part of the UX.
   Each tile points to a real public artifact. The page is stronger when the visual design and evidence routes are the same object.

## 2026-04-30 — Operating model / implementation-evidence layer

Research direction: stronger product-engineering portfolios do not just show pretty pages. They show the evaluator how the work was shaped, what decisions were made, what tradeoffs exist, and where proof lives. The useful pattern for this portfolio is a visible operating model: workflow translation → state/rule design → validation/review gates → inspectable artifacts → QA/delivery.

Applied changes:
- Added `/operating-model/` as a public build-system surface between case studies and architecture.
- Added a blueprint-style hero graphic so the page feels like a system artifact, not a resume paragraph.
- Connected each workflow stage to a real proof route: SquadBrain case study, public examples, Lasting Ground examples, sample packet, and Systems Lab.
- Kept wording professional and evidence-led: no self-conscious framing, no claims that cannot be inspected, no hidden-method language.
- Synced the profile mirror navigation so the GitHub profile routes reviewers into the new proof path.

Design bar for future passes:
- Prefer pages that behave like tools or review surfaces over pages that only describe skills.
- Keep every advanced capability paired with a public proof path.
- Use custom system graphics only when they clarify workflow, logic, validation, or delivery.
- Continue mobile-first visual QA; most portfolio mistakes show up as cramped navigation, clipped headings, or unreadable proof panels.

## 2026-04-30 — Outcome evidence board

Research direction: portfolio reviewers skim. Strong case-study surfaces lead with the end state, the problem being solved, and the evidence that proves the work. Reddit UX critique threads repeatedly point to the same issue: portfolios over-explain process but under-show outcomes, impact, and what changed. Portfolio guides also emphasize result sections, proof artifacts, and scannable evidence.

Applied changes:
- Added `/outcomes/` as an evidence-led outcome board.
- Structured each project around starting condition → system built → evidence visible.
- Used honest measurable public proof only: test counts, coverage summaries, demos, sample packet, examples, and ADRs.
- Added a homepage outcome preview so the first screen path now points to evaluation evidence, not just project descriptions.
- Linked the outcome board from selected work, evaluator console, systems atlas, operating model, systems lab, and case studies.

Design bar for future passes:
- Lead with what changed, but avoid invented business metrics.
- If a number is shown, it must map to a real artifact that can be opened.
- Keep case-study evidence scannable: problem, system response, proof links.
- Prefer fewer stronger proof routes over adding more generic pages.

## 2026-04-30 — Diligence packet / portable proof layer

Research direction: hiring and collaboration review often happens outside the portfolio page itself. Strong evidence systems give a reviewer a fast online path and a clean portable artifact. Current portfolio guidance repeatedly emphasizes concise case-study summaries, proof of impact, readable outcomes, and downloadable/shareable portfolio material when appropriate.

Applied changes:
- Created an earlier public diligence packet PDF with embedded links.
- Added `/diligence/` as a polished packet page with PDF preview and review rationale.
- Added a homepage shareable-packet section and synced the profile mirror.
- Linked the packet from the outcome board and evaluator console.
- Rendered the PDF to PNG and visually checked spacing, card hierarchy, and legibility before shipping.

Design bar for future passes:
- Treat PDFs as proof artifacts, not decoration.
- Keep the packet one page unless there is real new evidence to add.
- Make every metric traceable to a public coverage/test artifact.
- Preserve a clean reviewer journey: homepage -> outcome board -> diligence packet -> lab/code.

## 2026-04-30 — Advanced diligence packet pass

Research direction: the best portfolio artifacts reduce reviewer effort. A PDF should not merely duplicate the homepage; it should create a portable review system with embedded links, clear timing paths, and a proof ledger. The useful pattern is website-first for exploration, PDF-second as a sharable route, and code/artifacts as the final evidence layer.

Applied changes:
- Upgraded the diligence packet from a simple leave-behind to a multi-page public review packet.
- Added a QR route to the live diligence page and embedded links throughout the PDF.
- Added page two as an inspection ledger with 1-minute, 5-minute, 15-minute, and full-review paths.
- Added a public evidence map separating live surface, executable logic, quality proof, and system boundary for both projects.
- Upgraded `/diligence/` with a review command center so the web page now matches the advanced packet structure.

Design bar for future passes:
- Keep the PDF compact but not shallow: two pages is currently the right balance.
- Every PDF element should either route, verify, or clarify.
- The diligence page should feel like a command surface, not a download landing page.

## 2026-04-30 — v16 premium color and artifact-framing pass

Research direction: Reddit portfolio critiques and GitHub README patterns point to the same practical bar: visual ambition helps only when it does not hide the work. Project images need strong framing, mobile links must remain easy to tap, effects should not distract from proof, and review artifacts should be scannable in seconds. GitHub README research also reinforces that popular projects tend to use organized sections, images, and external links rather than walls of text.

Applied changes:
- Rebuilt the diligence PDF color system into a cooler product-systems palette: navy, teal, cyan, blue, and amber with stronger card separation.
- Re-rendered the PDF and cover after visual inspection; fixed clipped/overlapping card content on page one.
- Replaced the homepage SVG proof graphics with cleaner, more legible product-system visuals.
- Added a global v16 CSS layer across the main portfolio and profile mirror: stronger artifact frames, safer responsive system cards, better contrast, and less beige blending.
- Removed weaker phrasing from the proof-wall graphic and kept the language public-facing and inspectable.

Design bar for future passes:
- Keep one strong accent family and use color for hierarchy, not decoration.
- Make every screenshot, PDF preview, and proof graphic look like a deliberate artifact inside a frame.
- Prefer artifact clarity over animation.
- Keep mobile screenshots in QA because overlap and cramped proof cards are the easiest way to look amateur.

Sources checked:
- Reddit r/webdev portfolio critique thread: https://www.reddit.com/r/webdev/comments/1qs35d7/portfolio_feedback/
- Awesome README examples: https://github.com/matiassingers/awesome-readme
- README popularity study: https://arxiv.org/abs/2206.10772
- Professional README guide: https://coding-boot-camp.github.io/full-stack/github/professional-readme-guide/

## 2026-04-30 — v17 elite packet and profile command surface

Research direction: the strongest public technical profiles reduce reviewer effort. Reddit hiring and portfolio threads emphasize clear READMEs, deployed links, screenshots, tests, and obvious proof routes. GitHub README research reinforces that popular projects are organized, use images, and link outward to useful context. For this portfolio, the design move is not more decoration; it is a stronger command-surface layer that makes the evidence path impossible to miss.

Applied changes:
- Rebuilt the public diligence packet into a three-page proof packet: review route, project evidence ledger, and review-depth/capability map.
- Added a dedicated profile command-surface SVG for the GitHub profile and profile mirror page.
- Added a fast review route to the GitHub profile README so visitors know exactly where to click first.
- Upgraded profile page copy and packet references to the current three-page packet.
- Kept the public language evidence-led: demos, examples, tests, coverage, decision records, and generated outputs.

Design bar for future passes:
- Every visual should answer an evaluator question: what is this, what proves it, where do I inspect it?
- Profile README should behave like a high-signal routing page, not a biography.
- PDF pages should use big hierarchy, fewer claims, and clear proof routes rather than dense text.


## 2026-04-30 — v18 active-proof proof workbench

Research direction: stronger developer and UX portfolios reduce passive passive sections and replace them with reviewable artifacts, interaction, clear outcomes, and evidence paths. The useful pattern here is a product-like proof surface: switchable states, visible signals, direct artifact links, and case-study panels that show working logic rather than only cards.

Applied changes:
- Added an interactive proof console to the homepage and profile mirror so the first proof layer behaves like a small product surface.
- Added JavaScript state switching for SquadBrain, Lasting Ground, and the reviewer route with artifact links, metrics, coverage, and command-style logs.
- Reframed the public profile graphic as a proof router so the page feels like an inspection surface as an inspection surface.
- Upgraded both case-study pages with console-style system panels and direct proof tiles for code paths, guardrails, coverage, ADRs, and packet output.
- Kept every advanced claim tied to a public proof route rather than decorative polish.

Design bar for future passes:
- More surfaces should behave like small evaluators, debuggers, or system maps.
- Avoid adding another static strip unless it has a proof action, state transition, or artifact route.
- Mobile QA must confirm all console panels stack cleanly and proof text stays readable.


## 2026-04-30 — v19 premium PDF density pass

Research direction: the packet should work as a compact proof artifact, not a sparse poster. The strongest leave-behind format gives a reviewer a route, a ledger, and a decision map without forcing them to reconstruct the evidence trail.

Applied changes:
- Rebuilt the packet generator with a denser three-page layout: fast proof route, implementation receipts, and review-depth/capability map.
- Added console-style proof visuals, artifact tiles, a public implementation ledger, and tighter route cards.
- Regenerated the PDF and cover PNG from the same source so the website preview matches the current packet.
- Updated stale packet-length copy on packet-related pages.

Design bar for future passes:
- The PDF should remain a review artifact, not a brochure.
- Any future metric must be publicly verifiable or removed.
- Keep PDF text large enough to skim while using tables and route cards to reduce empty space.

## 2026-04-30 — v20 packet inspector pass

Research direction: portfolio artifacts should reveal the review path before a reviewer commits to opening files. Current GitHub/portfolio advice keeps pointing to the same pattern: make proof scannable in seconds, keep links runnable, and show tests/CI/artifacts instead of static screenshots alone.

Applied changes:
- Added a live packet inspector to `/diligence/` with page-by-page previews for route, ledger, and review-depth map.
- Exported page 2 and page 3 PNG previews from the generated PDF so the page exposes the whole artifact, not only the cover.
- Tightened review command cards so they feel more like a usable review surface and less like empty presentation slides.
- Rechecked desktop and mobile layouts after the interactive section landed.

Design bar for future passes:
- Keep converting static page sections into small tools: inspectors, proof consoles, state switchers, and role routes.
- Do not add motion or decoration unless it makes the proof easier to evaluate.
- The next credibility jump should be more live interaction and cleaner end-to-end route cohesion, not more claims.
