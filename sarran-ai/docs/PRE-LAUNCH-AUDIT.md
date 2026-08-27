# Pre-Launch Website Audit — Sarran AI Solutions LLC

| | |
|---|---|
| **Date** | 2026-08-26 |
| **Scope** | `sarran-ai/` — `index.html`, `styles.css`, `main.js`, `assets/` |
| **Method** | Static inspection + headless Chrome rendering, in-browser DOM measurement at 8 viewports, contrast computation, link/anchor enumeration, JS safety scan, live font-payload measurement |
| **Overall score** | **64 / 100** |
| **Launch status** | **Not ready** |

> This file is documentation, not part of the deployable site. Exclude `docs/`, `scripts/`, and
> `README.md` from any production upload.

---

## Pick up here — open actions

Work top to bottom. Items 1–8 gate launch.

### Blockers
- [ ] **1.** Set the live scheduling URL on the booking CTA — `index.html:469`, currently `href="#"` (**B1**)
- [ ] **2.** Replace or remove the three placeholder testimonials + footer "Clients" link — `index.html:387, 394, 401` (**B2**)

### High
- [ ] **3.** Set the domain; uncomment and populate canonical / `og:url` / `og:image` — `index.html:11–16` (**H1**)
- [ ] **4.** Add `robots.txt` and `sitemap.xml` (**H2**)
- [ ] **5.** Raise `--line` to meet 3:1 contrast for control boundaries (**H3**)
- [ ] **6.** Add privacy policy + footer legal links; move to a domain email (**H4**)

### Pre-launch hygiene
- [ ] **7.** Remove orphaned assets and `scripts/` from the deployable directory (**M3**)
- [ ] **8.** Re-test the whole funnel end-to-end on a real device once booking is live

### After launch
- [ ] Self-host + subset fonts, preload display face (**M2**)
- [ ] Metric-matched `@font-face` fallbacks to remove swap reflow (**M1**)
- [ ] Analytics / conversion tracking (**M9**)
- [ ] Spacing scale + `--accent-rgb` channel token (**M4**, **M5**)
- [ ] Increase footer link and hamburger target heights past 24px (**M6**)
- [ ] Content-Security-Policy at the host
- [ ] Constrain `.lede__sub` measure (**M7**)

### Optional polish
- [ ] `:active` states (**L3**) · remove orphan IDs `foot-contact`, `masthead` (**L1**) ·
      resolve `<figure>` `aria-label`/`figcaption` conflict (**L2**) · 404 page + web manifest (**L4**) ·
      real imagery or commit to type-only (**M8**) · obfuscate email against harvesters

---

## 1. Executive verdict

**Overall score: 64 / 100** · **Launch status: Not ready**

The site is well-built at the craft level — valid HTML, zero console errors, no horizontal overflow at any of eight tested viewports, clean progressive enhancement, and text contrast that passes AA — but it cannot go live because the entire conversion funnel terminates in a dead link and the social-proof section is three visible "Placeholder" strings. Every "Book" button routes to `#book`, and the button there is `href="#"`, so no visitor can ever book anything. Supporting launch infrastructure is also absent or inert: canonical, `og:url`, and `og:image` are commented out with `REPLACE-ME`, and there is no `robots.txt` or `sitemap.xml`. The underlying design and engineering are solid; the launch-readiness layer is not.

**Issue counts:** 2 Blocker · 4 High · 9 Medium · 6 Low

## 2. Scorecard

| Category | Score / 10 | Weight | Weighted score | Main reason |
|---|---|---|---|---|
| Visual hierarchy and layout | 8 | 8% | 6.4 | Clear hierarchy, consistent rhythm; testimonials block reads empty |
| Typography | 7 | 6% | 4.2 | Deliberate pairing and scale; 85-char measure, unmatched fallback metrics |
| Color and imagery | 7 | 6% | 4.2 | Fully tokenized palette; non-text contrast failure, effectively no imagery |
| Motion and interaction | 8 | 7% | 5.6 | Purposeful, reduced-motion honoured, verified working; no `:active` states |
| Design system consistency | 7 | 7% | 4.9 | Color/type tokenized; no spacing scale, 11 hard-coded rgba values |
| Performance and responsiveness | 7 | 15% | 10.5 | No overflow anywhere, tiny JS; 143 KB blocking third-party fonts, confirmed reflow |
| Trust and conversion | 3 | 10% | 3.0 | Primary CTA dead, placeholder testimonials, no legal pages, personal Gmail |
| Functionality | 4 | 15% | 6.0 | 27/28 links work, but the one that matters most is dead |
| Accessibility | 8 | 10% | 8.0 | Strong semantics/keyboard/motion; 1.4.11 boundary failure, borderline targets |
| Security | 8 | 10% | 8.0 | No secrets, no eval/innerHTML/storage/network; no CSP, exposed email |
| Code quality and production readiness | 6 | 6% | 3.6 | Clean and documented; no robots/sitemap, inert meta, orphan assets |
| **Total** | | **100%** | **64.4** | |

## 3. Launch blockers

### B1 — Primary conversion CTA is a dead link

- **Issue:** The terminal booking button does nothing.
- **Evidence:** Link enumeration across all 28 anchors returned exactly one failure: `DEAD (href="#") — "Book an AI Readiness Assessment"`. Source carries `<!-- TODO: replace "#" with the live scheduling URL -->`.
- **Location:** `index.html:469`, `#book` section.
- **Impact:** Total conversion failure. Every other CTA — header, mobile drawer, hero, trust section — points to `#book`, which scrolls the user to a button that cannot be clicked through. There is no working booking path anywhere on the site. The only functioning contact routes are a `mailto:` and a `tel:`.
- **Suggested correction:** Set the live Calendly/Cal.com URL. Since all upstream CTAs funnel here, this single href is the whole funnel.

### B2 — Testimonials section ships literal placeholder text

- **Issue:** All three social-proof cards display "Placeholder — replace with a real client quote." with "Client name / Role · Company".
- **Evidence:** `index.html:387, 394, 401`, preceded by `<!-- PLACEHOLDER — replace all three ... -->`. Rendered and confirmed visible in browser output.
- **Location:** `#voices` section; also linked from the footer as "Clients".
- **Impact:** Directly credibility-destroying on a site whose stated purpose is establishing trust and authority. A visitor who scrolls sees a section headed "What people say after the work ships" containing three admissions that nobody has said anything. Worse than omitting the section.
- **Suggested correction:** Replace with real attributed quotes, or remove the section and its footer "Clients" link until quotes exist.

## 4. Confirmed issues

### High

**H1 — Canonical, `og:url`, and `og:image` are inert**
*Category: SEO / production readiness.* `index.html:11–16` wraps all three in an HTML comment with `https://REPLACE-ME/`. An automated substring pass produced a false positive here; direct inspection of the head confirms they are commented out. Social shares will render with no image, and there is no canonical URL. Set the domain and uncomment; absolute URLs are required.

**H2 — No `robots.txt`, no `sitemap.xml`, no manifest**
*Category: SEO / discoverability.* Full file inventory shows neither. This matters more than usual here: the business sells AI-search visibility, and AI crawler access is governed largely by `robots.txt`. Shipping without one is off-message as well as ineffective.

**H3 — Secondary button boundary fails WCAG 2.2 AA 1.4.11**
*Category: Accessibility.* `.button--quiet` uses `--line #1B3557` on `--void #05101F` = **1.54:1**, against a 3:1 requirement for identifying a UI control. Affects "See what we build", "Talk through your setup", "Email instead". Label text passes (17:1), so the control is readable but its boundary is nearly invisible. Also affects `.callsheet` border (1.41:1).

**H4 — No privacy policy, no legal links, personal Gmail as sole business contact**
*Category: Trust / legal.* The footer contains no privacy, terms, or cookie links. The only email is `robertgangasarran@gmail.com` — a personal Gmail presented as the contact for an LLC selling to regulated businesses. Once a third-party scheduler is embedded (the plan for B1), a privacy notice becomes a practical requirement, not a nicety.

### Medium

**M1 — Web-font swap causes visible reflow (CLS risk)**
*Category: Performance.* Rendered the page twice, once with `fonts.gstatic.com`/`fonts.googleapis.com` blackholed. Layouts diverge from scanline ~20 onward; the hero transcript wraps to two lines with the webfont and one line without. `display=swap` paints the fallback first, so this reflow happens on real loads. No `size-adjust` / `ascent-override` metric matching is defined. Viewport: all.

**M2 — 143 KB of render-blocking third-party fonts**
*Category: Performance.* Measured the actual Google Fonts payload: 143 KB across 4 latin-subset `woff2` files, plus a 9 KB render-blocking stylesheet on a third-party origin. Three families (Archivo variable with a width axis, Public Sans, IBM Plex Mono) is the largest single cost on the page — roughly 2/3 of total transfer.

**M3 — Orphaned assets shipped**
*Category: Production readiness.* `assets/sarran_emblem.png` (313 KB) is referenced only from the commented-out `og:image`; four legacy teal SVGs (`Sarran_AI_logo_*.svg`, `Sarran_AI_icon.svg`) are referenced nowhere. `scripts/mklogo.py` is a build tool that would deploy with the site.

**M4 — No spacing scale**
*Category: Design system.* Color and typography are tokenized (125 `var()` references, zero unused CSS classes), but spacing is not: **19 distinct `gap` values**. Section `padding-block` is consistent (`7rem` × 6), so the inconsistency is concentrated in component-level spacing.

**M5 — Hard-coded rgba values bypass the accent token**
*Category: Design system / maintainability.* 11 colour literals sit outside `:root`, including `rgba(59,158,255,…)` × 6 for the hero bloom, callsheet shadow, pip animation, and booking glow. Changing `--accent` will not update any of them. This is a demonstrated risk, not theoretical — the earlier teal→blue change required separately rewriting these values.

**M6 — Footer link targets at the WCAG 2.2 minimum**
*Category: Accessibility.* Measured at every viewport: footer nav links render **24px tall** (width is generous, 219–461px). WCAG 2.2 AA 2.5.8 requires 24×24 CSS px; these sit exactly on the line with 11px gaps. Passing, but with no margin.

**M7 — Section sub-headings exceed comfortable measure**
*Category: Typography.* `.lede__sub` measures 736px at 16.8px ≈ **85 characters per line** against a 45–75 ideal. Other body copy measures well (hero 55, cards 60, trust 64, booking 73).

**M8 — The site has essentially no imagery**
*Category: Imagery.* The only raster asset is the logo emblem. Against a brief asking for "immersive" and "interactive visual elements", the page is entirely type, rules, and one badge. Defensible as restraint, but it is thin for the stated ambition and there is no visual evidence of the work.

**M9 — No analytics or conversion tracking**
*Category: Conversion.* No measurement of any kind. Once B1 is fixed there will be no way to know whether the funnel converts.

### Low

- **L1 — Two orphan IDs:** `foot-contact` and `masthead` are declared but referenced by nothing (`foot-contact` lost its `aria-labelledby` when the footer was restructured).
- **L2 — `<figure aria-label>` overrides its own `<figcaption>`:** the callsheet's accessible name comes from `aria-label`, suppressing the figcaption content for screen readers.
- **L3 — No `:active` states:** buttons and links define hover and focus but no pressed state; touch users get no press feedback.
- **L4 — No 404 page:** single-page static site, so not currently reachable, but any mistyped path on the eventual host will fall through to server default.
- **L5 — Hamburger target 38×24px:** meets the 24×24 minimum on height by exactly zero margin.
- **L6 — README documents a build script that ships:** `scripts/mklogo.py` is dev tooling inside the deployable directory.

### Observations

- Scroll-reveal sets `opacity: 0` on 25 elements pending IntersectionObserver. The code correctly guards on `'IntersectionObserver' in window` and skips arming under `prefers-reduced-motion`, so no-JS and no-IO paths render fully. Content remains in the DOM regardless, so extraction is unaffected — visual-only risk.
- The pedigree strip lists American Express, Fiserv, Wells Fargo, BNY Mellon, FINRA. This is correctly captioned "Founder's career history in regulated financial services — not a client list." Keep that disclaimer; removing it would create a misrepresentation risk.
- The hero transcript is labelled "Illustrative transcript of a deployed voice agent" — appropriate and honest.
- Six `!important` declarations, all justified (one on `[hidden]`, five in the reduced-motion block).

## 5. Seven-point design review

### 1. Visual hierarchy and layout — 8/10

**What works:** Section order follows a coherent argument (problem → services → process → trust → proof → about → CTA). A single 1200px `.shell` governs all content width, and `padding-block: 7rem` repeats consistently across six major sections. The hero's asymmetric split gives the signature artifact real prominence without crowding the headline. Scanability is good — every section leads with a mono eyebrow, then an H2, then content.

**What falls short:** The testimonials band is three identical low-content cards and reads as a hole in the page. The pedigree strip is visually thin relative to its importance. `.lede__sub` runs wide enough to weaken the top of each section.

**Recommended improvements:** Resolve the testimonials content (B2). Constrain `.lede__sub` to ~60ch. Consider giving the pedigree strip more vertical presence.

### 2. Typography — 7/10

**What works:** A genuinely deliberate three-role system — Archivo (display, 800 weight at 112% width), Public Sans (body), IBM Plex Mono (data/labels) — where mono carries only real machine data. Type scale is clean: 65.6 / 48 / 24 / 20px with line-heights tightening as size grows (1.08 at H1). Measures are mostly well controlled (55–73 chars). Zoom is unrestricted — no `user-scalable=no`.

**What falls short:** 85-char measure on section subs. Three families is heavy. Fallback stacks have no metric matching, producing confirmed reflow. `font-stretch: 112%` silently does nothing on the Segoe UI fallback, so the fallback rendering diverges more than necessary.

**Recommended improvements:** Self-host and subset the fonts, or drop to two families. Add `size-adjust`/`ascent-override` to a local `@font-face` fallback. Tighten `.lede__sub`.

### 3. Color and imagery — 7/10

**What works:** The palette is fully tokenized and coherent — a blue-black ground that carries hue through every surface rather than neutral black. All text pairs pass AA, several comfortably (ink 17:1, muted 7.9:1, accent 6.8:1, faint 5.0:1 after correction). Red is disciplined to booking CTAs only. The emblem is correctly masked, sized via `srcset` (128/192), and has appropriate empty `alt` with an adjacent text wordmark.

**What falls short:** Non-text contrast fails on control boundaries (1.54:1). There is no imagery beyond the logo. A 313 KB PNG sits in the folder unreferenced by the rendered page.

**Recommended improvements:** Lift `--line` to ≥3:1 for control borders. Add real imagery or commit fully to the type-only direction. Prune orphaned assets.

### 4. Motion and interaction — 8/10

**What works:** Motion is purposeful and verified functional. Direct render at 1440×900 confirms the call log plays 6/6 lines; at full page height all 25 reveals fire and the typewriter completes with the correct string. The drawer opens, sets `aria-expanded` correctly, closes on link click and on Escape. `prefers-reduced-motion` is honoured throughout, and nothing is hidden until JS arms it, so the no-JS page renders complete. No cursor-tracked effects. The typewriter reserves its final height so nothing shifts as characters land.

**What falls short:** No `:active` states. The closing CTA headline is withheld for ~1.9s behind the typing animation — on the page's most conversion-critical text. There are no loading, error, or empty states anywhere, because there is nothing asynchronous.

**Recommended improvements:** Add pressed states. Consider shortening the typewriter or triggering it earlier.

### 5. Design system consistency — 7/10

**What works:** Strong token discipline on colour and type — 125 `var()` references, a single `:root` palette block, zero unused CSS classes, only two z-index values (100/200), four media queries. BEM-ish naming is consistent and readable. Section padding is uniform.

**What falls short:** No spacing scale — 19 distinct gap values. Eleven hard-coded colour literals sit outside the token system and will not follow `--accent`. Border-radius is partly tokenized, partly literal (`2px` × 2).

**Recommended improvements:** Introduce a spacing scale. Add an `--accent-rgb: 59, 158, 255` channel token so the rgba values can reference it.

### 6. Performance and responsiveness — 7/10

**What works:** Responsive behaviour is genuinely clean. Measured `scrollWidth` against `clientWidth` at 320/375/430/768/1024/1280/1440/1920 — **no horizontal overflow at any width**, no clipping, no overlap. Own-code payload is small: 22 KB HTML, 19 KB CSS, 5 KB JS. JS makes no network calls and uses no storage. The emblem is properly sized via `srcset` (29 KB served, not 313 KB) with width/height set and `fetchpriority="high"` on the header instance.

**What falls short:** Fonts dominate — 143 KB over 4 requests from a third-party origin behind a render-blocking stylesheet, roughly two-thirds of total transfer. Font swap causes confirmed reflow. No `preload` on the critical font.

**Recommended improvements:** Self-host and subset fonts; preload the display face; add metric-matched fallbacks.

### 7. Trust and conversion — 3/10

**What works:** CTA language is consistent and specific ("Book an AI Readiness Assessment" rather than "Submit"). CTAs appear at four points. The credibility material is strong and honestly framed — the pedigree strip explicitly disclaims a client relationship, and the hero transcript is labelled illustrative. Objection-handling copy ("no prep", "whether or not you hire us") is well judged.

**What falls short:** The funnel is broken end to end (B1). Social proof is placeholder text (B2). No legal or privacy pages. A personal Gmail is the only email. No analytics. Sharing metadata is inert, so any shared link renders bare.

**Recommended improvements:** Fix B1 and B2 first — nothing else in this category matters until they are resolved. Then add a domain email, privacy page, and analytics.

## 6. Responsive testing matrix

Measured programmatically in-browser (`documentElement.scrollWidth` vs `clientWidth`, plus per-element bounding-box overflow and interactive-target sizing) at every required width.

| Viewport | Pages tested | Result | Confirmed issues |
|---|---|---|---|
| 320px | index.html | Pass | No overflow (305/305). Footer links 24px tall — at WCAG minimum |
| 375px | index.html | Pass | No overflow (360/360). Drawer opens/closes correctly; drawer links 26px, CTA 48px |
| 430px | index.html | Pass | No overflow (415/415). Same target note |
| 768px | index.html | Pass | No overflow (753/753). Two-column grids resolve correctly |
| 1024px | index.html | Pass | No overflow (1009/1009) |
| 1280px | index.html | Pass | No overflow (1265/1265) |
| 1440px | index.html | Pass | No overflow (1425/1425) |
| 1920px | index.html | Pass | No overflow (1905/1905). Content caps at 1200px shell; no stretching |

**Horizontal scrolling:** none at any width. **Clipping/overlap:** none detected. **Breakpoint behaviour:** consistent — nav collapses to hamburger below 860px, grids collapse at 1040px and 680px, no dead zones found. **Touch usability:** hamburger 38×24px and footer links 24px tall both meet WCAG 2.2 AA 2.5.8 with zero margin; the drawer's own links (26px) and CTA (48px) are comfortable.

> Chrome on Windows enforces a ~500px minimum window, so sub-500px widths were tested via a
> fixed-width iframe with `--allow-file-access-from-files`, measuring the inner document directly.
> A plain `--window-size=390` screenshot crops a 497px render rather than reflowing it.

## 7. Functional testing results

**Pages and routes tested:** `index.html` — the entire site. No router, no build step, no server. Direct-URL and refresh behaviour is trivially correct (all navigation is same-page hash anchors, which survive refresh).

**Links tested:** all 28 anchors enumerated and validated against declared IDs.

- 27 resolve correctly (11 hash anchors, 2 `mailto:`, 1 `tel:`, 1 external, plus duplicates across header/drawer/footer)
- 1 dead: `href="#"` on the primary booking CTA
- 0 broken fragments, 0 duplicate IDs
- External LinkedIn link correctly carries `target="_blank"` with `rel="noopener noreferrer"`

**Forms tested:** none exist — 0 `<form>`, 0 `<input>`, 0 `<textarea>`. Contact is `mailto:`/`tel:` only. Form validation, duplicate submission, and submission error handling are therefore **not applicable**, not passing.

**Interactive components tested:** mobile drawer (open, close-on-link, close-on-Escape, `aria-expanded` sync) — all pass. Masthead scroll-tuck — implemented with rAF throttling. Call-log reveal — 6/6. Scroll reveal — 25/25 at full height, correctly deferred below fold. Typewriter — completes with correct text; no-JS fallback verified with `--disable-javascript`.

**Build result:** No build system. Static files served as-is — **not applicable**.

**Console errors:** none captured. **Console warnings:** none captured. **Failed requests:** none for local assets; all local paths resolve.

**Features that could not be verified:**

- Real-device touch interaction (emulated geometry only)
- Actual Core Web Vitals field values (LCP/INP/CLS numbers) — no Lighthouse or CDP tracing available; the CLS *risk* is evidenced by rendered reflow, but not quantified
- Screen-reader output (NVDA/JAWS/VoiceOver) — structure inspected statically, not announced
- Host-level behaviour: security headers, HTTPS, compression, caching, 404 handling — all depend on a host that does not yet exist
- Third-party scheduler behaviour, since none is wired

> **Note on a false negative during testing.** An iframe-based harness initially reported the call
> log, scroll reveals, and typewriter as not firing (0/6, 0/25, not done). This was an artifact —
> IntersectionObserver does not fire reliably inside an iframe under headless virtual time.
> Re-tested with direct rendering: at 1440×900 the call log plays 6/6 with below-fold reveals
> correctly deferred; at full page height all 25 reveals fire and the typewriter completes. The JS
> is correct. Use direct rendering, not iframes, when re-testing these effects.

## 8. Security review

**Confirmed security issues:** none.

**Posture.** This is a static, dependency-free page, which removes most of the attack surface by construction. Scanned `main.js`: **0** uses of `eval`, `new Function`, `innerHTML`, or `document.write`; **0** network calls; **0** use of `localStorage`/`sessionStorage`/cookies. DOM writes use `textContent` exclusively (2 sites). No user input is accepted anywhere, so XSS, injection, CSRF, IDOR, open-redirect, and file-upload categories have no applicable surface.

**Potential risks:**

- **No Content-Security-Policy or security headers.** Not settable from a static file beyond a `<meta>` CSP; must be configured at the host. Given two third-party origins are loaded, a CSP is worth defining.
- **Third-party dependency on Google Fonts.** `fonts.googleapis.com` and `fonts.gstatic.com` are trusted implicitly. Self-hosting removes both the third-party trust and the EU data-transfer question.
- **`REPLACE-ME` placeholder URLs** in the commented meta block would resolve to a non-existent host if uncommented carelessly.
- **Plaintext email in markup** (`robertgangasarran@gmail.com`, appearing twice) is harvestable for spam.

**Secret exposure review:** no API keys, tokens, credentials, or environment variables found in any file. No `.env`, no config files, no build secrets. Nothing to mask.

**Dependency risks:** none — zero npm packages, zero JS libraries, no lockfile, no supply chain.

**Authentication and authorization:** no auth exists and none is required; there are no protected routes or admin surfaces.

**Input/output handling:** no inputs. Output is entirely static author-controlled markup.

**Checks that could not be completed:** TLS configuration, HSTS, security headers, CORS, rate limiting, and host-level abuse protection — all require a deployed origin.

## 9. Accessibility review

**Keyboard navigation:** 19 focusable elements, logical DOM order, **zero positive `tabindex`** values. Skip link present and targets a real `#main`. Drawer is a real `<button>` with `aria-expanded`, `aria-controls` pointing at an existing ID, and Escape-to-close verified working. All interactive elements use native `<a>`/`<button>` — no div-buttons.

**Screen-reader and semantic structure:** HTML parses with zero unclosed tags or stray end tags. `<main>` landmark present; 4 `<nav>` elements, all with distinguishing `aria-label`. Heading order is valid throughout — single H1, no skipped levels. Zero `role` attributes, correctly, since native elements are used. The typewriter keeps its real sentence in the accessibility tree via `opacity` (not `visibility`/`clip`) with the animated copy `aria-hidden`, so the headline announces once and normally.

**Contrast:** all text pairs pass AA after the `--faint` correction — ink 17.09:1, muted 7.92:1, faint 5.01:1 (void) / 4.59:1 (surface), accent 6.83:1, white-on-red CTA 5.01:1. **Non-text contrast fails** (H3): control boundaries at 1.54:1 against a 3:1 requirement.

**Forms:** none present, so labelling and error identification are not applicable.

**Focus states:** `:focus-visible` styled globally with a 2px `--accent-lift` outline at 3px offset — 10.18:1 against the ground, well clear of requirements.

**Motion preferences:** `prefers-reduced-motion` respected comprehensively — animations reduced to 0.001ms, smooth scrolling disabled, and both the reveal and typewriter systems skip arming entirely, so reduced-motion users see complete static content rather than hidden content.

**Image alternatives:** the only image is the emblem, correctly `alt=""` (decorative) with the brand name supplied as adjacent live text and an `aria-label` on the wrapping link.

**Touch targets:** hamburger 38×24px, footer links 24px tall — both exactly at the WCAG 2.2 AA 2.5.8 threshold with no margin (M6).

**Zoom/reflow:** `width=device-width, initial-scale=1` with no `user-scalable=no` or `maximum-scale`. 320px reflow is clean, satisfying 1.4.10.

**Major WCAG risks:** 1.4.11 Non-text Contrast (H3) is the one clear AA failure. 2.5.8 Target Size is borderline. Not verified: actual screen-reader announcement, and 1.4.12 Text Spacing under user stylesheet overrides.

## 10. Recommended changes

### Before launch

1. Set the real scheduling URL on the booking CTA (**B1**) — nothing else matters until this works.
2. Replace or remove the three placeholder testimonials and the footer "Clients" link (**B2**).
3. Set the domain; uncomment and populate canonical, `og:url`, `og:image` (**H1**).
4. Add `robots.txt` and `sitemap.xml` (**H2**).
5. Raise `--line` to meet 3:1 for control boundaries (**H3**).
6. Add a privacy policy and footer legal links; move to a domain email (**H4**).
7. Remove orphaned assets and `scripts/` from the deployable directory (**M3**).
8. Verify the whole funnel end-to-end on a real device once the booking link is live.

### Soon after launch

9. Self-host and subset the fonts; preload the display face (**M2**).
10. Add metric-matched `@font-face` fallbacks to eliminate swap reflow (**M1**).
11. Add analytics and conversion tracking (**M9**).
12. Introduce a spacing scale and an `--accent-rgb` channel token (**M4**, **M5**).
13. Increase footer link and hamburger target heights past the 24px minimum (**M6**).
14. Define a Content-Security-Policy at the host.
15. Constrain `.lede__sub` measure (**M7**).

### Optional polish

16. Add `:active` states (**L3**).
17. Remove orphan IDs `foot-contact`, `masthead` (**L1**).
18. Resolve the `<figure>` `aria-label`/`figcaption` conflict (**L2**).
19. Add a 404 page and web manifest (**L4**).
20. Consider real imagery, or commit deliberately to the type-only direction (**M8**).
21. Obfuscate the email address against harvesters.

## 11. Final checklist

| Item | Status |
|---|---|
| Production build succeeds | **Not verified** — no build system exists (static files) |
| No broken critical routes | **Pass** — single page, all 11 hash anchors resolve |
| No broken critical CTAs | **Fail** — primary booking CTA is `href="#"` |
| No exposed secrets | **Pass** — no keys, tokens, credentials, or env files |
| No critical console errors | **Pass** — zero errors, zero warnings captured |
| No major mobile layout failures | **Pass** — no overflow at 320/375/430/768px |
| Forms work correctly | **Not verified** — no forms exist |
| Error states are handled | **Not verified** — nothing asynchronous to fail |
| Keyboard navigation works | **Pass** — skip link, logical order, Escape closes drawer, no positive tabindex |
| Text and controls meet reasonable contrast | **Partial** — all text passes AA; control boundaries fail 1.4.11 at 1.54:1 |
| Images load and scale correctly | **Pass** — `srcset` serves 29 KB not 313 KB, dimensions set, correct alt |
| Page metadata is configured | **Partial** — title, description, JSON-LD, favicon, OG title/description present; canonical, `og:url`, `og:image` inert |
| Performance is acceptable | **Partial** — own payload small; 143 KB blocking third-party fonts and confirmed reflow |
| Security risks are acceptable | **Pass** — no attack surface; CSP recommended at host |
| Website is ready to go live | **Fail** |

## 12. Final conclusion

The website is not ready to go live because launch-blocking issues remain.

---

## Appendix — how to reproduce these measurements

| Check | Command / method |
|---|---|
| Render a page | `chrome.exe --headless --disable-gpu --hide-scrollbars --virtual-time-budget=10000 --window-size=W,H --screenshot=OUT.png "file:///…/index.html"` |
| Sub-500px viewport | Wrap in a fixed-width iframe; Chrome on Windows clamps windows to ~500px |
| Read post-JS DOM | Add `--dump-dom` (use direct rendering, not an iframe, for IntersectionObserver effects) |
| Disable JS | `--disable-javascript` |
| Force font fallback | `--host-resolver-rules="MAP fonts.gstatic.com 127.0.0.1, MAP fonts.googleapis.com 127.0.0.1"` |
| Cross-document measurement | `--allow-file-access-from-files` plus an iframe harness |
| Contrast | WCAG relative-luminance formula over the `:root` tokens in `styles.css` |
| Font payload | Fetch the Google Fonts CSS with a browser UA, split `@font-face` blocks by subset comment, `HEAD` each `woff2` |

Audit harnesses used for this report were written to the session scratchpad, not to this project.
