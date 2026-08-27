# Sarran AI Solutions LLC — website

Dark, enterprise-futurist single page. Blue palette, Archivo / Public Sans / IBM Plex Mono,
built around one signature element: a live after-hours call log in the hero.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | All structure and copy, one commented block per section |
| `styles.css` | Tokens + layout. **All colour lives in the `:root` block** — a hue change is one edit there |
| `main.js` | Drawer, masthead tuck, call-log playback, scroll reveal, footer year |
| `assets/` | Brand logos and icon from `06_Brand_Assets/` |
| `privacy.html` | Privacy notice linked from the booking form and footer |
| `robots.txt` / `sitemap.xml` | Production crawler guidance and canonical URL discovery |
| `llms.txt` | Concise public business and service summary for compatible AI retrieval tools |
| `_headers` | Netlify-style security and cache headers; translate these rules for other hosts |

Open `index.html` directly, or serve: `python -m http.server 8000`.

## Section order

Header · **Hero** (headline + call log) · Founder pedigree strip · **Services** (4) ·
**How it works** (4 phases) · **Why it holds up** (production/governance) ·
FAQ · About · Booking · Footer

## Design decisions

**Palette — blue.** Ground is a blue-black (`#05101F`) rather than a neutral near-black, so every
surface carries the hue; accent is azure `#3B9EFF`. Red `#D62828` stays reserved exclusively for
booking CTAs, per the brand standard's rule that red is a single deliberate action colour.

**Type — one deviation from the brand standard.** The standard specifies Poppins for display and
Calibri for body. Calibri isn't a web font, and Poppins reads friendly-startup rather than
enterprise. Used instead:

- **Archivo** (display) — a grotesque built for high-performance UI; heavy weights at ~112% width
- **Public Sans** (body) — the US Web Design System face, chosen for institutional credibility
- **IBM Plex Mono** (data) — timestamps, phase labels, call metadata

The logo lockup keeps Poppins internally, since it's a fixed SVG. Reverting to Poppins is a
one-line change to `--display`.

**Signature element.** The hero leads with a working artifact instead of a headline-and-gradient:
a timestamped 2:47 AM inbound call that ends in a confirmed booking. The product is invisible —
a voice on a phone — so showing it beats asserting it. It plays once on first view.

**Numbering.** Only the process is numbered, because only the process is genuinely a sequence.
Service cards carry a role label (`Entry point`, `Always on`, `Front door`, `Back office`) rather
than decorative 01/02/03.

**Motion.** Two composed moments that bookend the page — the hero call log, and the closing
headline typing itself out — plus quiet scroll reveals and hover states. Both read as a machine
composing text, which is why the second one earns its place rather than being a stray effect.
No cursor-tracked effects anywhere, per your original instruction. `prefers-reduced-motion` is
honoured, and nothing is hidden until JS arms it — with JS off the page renders complete.

**Typewriter mechanics** (`.tw` in `styles.css`, `[data-typewriter]` in `main.js`). Two spans sit
on top of each other:

- `.tw__real` holds the actual sentence, stays in normal flow, and reserves the block's final
  height at every viewport width — so nothing below shifts as characters land. It's faded with
  `opacity` rather than `visibility`/`clip` specifically so it stays in the accessibility tree and
  screen readers announce the sentence once, normally.
- `.tw__type` is absolutely positioned over it, carries the animation and the caret, and is
  `aria-hidden`.

The fade only applies once JS adds `data-armed`, so with JS disabled the headline just renders.
Typing fires on scroll into view at 60% threshold, 38 ms per character, and the caret stops
blinking and clears on completion.

## Logo

Source: `02_Sales_Marketing/Sarran_AI_Solutions_LLC/SARRAN AI Solutions LLC_logo.png`
(2000×2000, 2.5 MB, circular emblem on an opaque brushed-metal plate).

Processed for web — the master file in OneDrive was not modified:

1. Cropped to the emblem's circular bezel, centred at r=782
2. Applied an antialiased circular alpha channel, so the metal plate is gone and the badge sits
   on the dark ground instead of appearing as a grey square
3. Exported at web sizes: `sarran_emblem.png` (512), `sarran_emblem@128/@192.png` (served to
   the header/footer via `srcset`)

Regenerate with `scripts/mklogo.py` if the source changes.

**Pairing.** The emblem contains its own set text, but at header scale that text is only a few
pixels tall, so it's paired with a CSS wordmark (`.brandmark`) that stays legible at any size.
The badge is the mark; the wordmark carries the name. This also resolves the earlier teal/blue
clash — the new emblem is cyan and sits naturally on the blue palette.

**Sizing.** `--badge` (58px header, 64px in `.brandmark--lg` for the footer) and `--bar` (86px)
are tokens — resize the emblem by editing `--badge` alone. Note the two move together: the badge
was raised from 48→58px and the bar from 72→86px in the same pass, because a larger emblem in the
original 72px bar reads as cramped rather than confident. Everything geared off `--bar`
(`scroll-padding-top`, the hero's top padding) follows automatically.

The previous teal lockups (`Sarran_AI_logo_*.svg`, `Sarran_AI_icon.svg`) are still in `assets/`
but no longer referenced. Left in place in case you want the horizontal lockup later.

## Booking form

Every "Book" button on the page opens the same panel at `#book` — header, mobile drawer, hero,
trust section, and the panel's own toggle. It is rendered open in the HTML and collapsed by
`main.js` on load, so with JavaScript disabled the form is still visible and posts natively.

**Delivery: FormSubmit.** A static page cannot send mail, so the form posts to
`formsubmit.co`, which relays to `robertgangasarran@gmail.com`. No account — the endpoint is the
address. `main.js` posts to the `/ajax/` variant so the visitor stays on the page; the plain
`action` on the `<form>` is the no-JavaScript fallback.

### Two things that will waste your time if you forget them

**1. Activation is per origin, not per email address.** Every host must be activated separately,
and the first submission from a new one triggers a confirmation email you have to click.
Already activated: `http://localhost:8000`, `http://localhost:8123`. **Your live domain will need
its own activation** — expect the first real submission not to arrive until you click that link.

**2. `localhost` and `127.0.0.1` are different origins.** `http://127.0.0.1:8000` is *not*
activated and returns "This form needs Activation". Always test at `http://localhost:8000`.
FormSubmit also rejects `file://` outright, so opening `index.html` by double-clicking will never
work — serve it: `python -m http.server 8000`.

### Diagnosing a failure

FormSubmit answers **HTTP 200 even when it rejects a submission** — the real verdict is the
`success` field in the body, which arrives as the string `"true"`/`"false"`. `main.js` checks that
field (checking `res.ok` alone reports false success), shows activation failures and other technical
details directly on the form, and logs the relay's own reason as `[booking form] <message>` in the
browser console. It also
sends the current page as `_url`, which lets FormSubmit identify the site when the browser's
referrer policy omits the full form URL.

### Before launch

- [ ] **Owner required:** activate the final HTTPS production origin. Submit once from the live
      site, open the FormSubmit activation email (including Spam), and click its activation link.
- [ ] **Owner required:** after activation, make a second controlled submission from the live site
      and confirm the complete message arrives in `robertgangasarran@gmail.com`. A successful UI
      message alone is not sufficient evidence of inbox delivery.
- [x] Set `_subject` to the production site name (`sarranai.com`).
- [x] Publish and link the privacy notice from the form and footer.
- [ ] Clear activation and test submissions from the inbox after verification.

Swapping providers is two attributes on the `<form>` (`action` and `data-endpoint`). Web3Forms and
Formspree key on an account token rather than the origin, which removes the activation dance.
PHPMailer is the better option if the host runs PHP — it keeps lead data in-house entirely — but
would need a JSON response to match the contract `main.js` expects.

## Open items before launch

- [ ] Voice-agent and web-development service copy is written from your brief, not from existing
      case material — review for accuracy before publishing.
- [ ] Confirm the LinkedIn URL and phone number.
- [x] Set canonical and Open Graph production URLs and image metadata.
- [x] Add `robots.txt` and `sitemap.xml` for `https://sarranai.com/`.
- [x] Add visible FAQ answers with matching FAQPage structured data.
- [x] Add WebSite, Organization, ProfessionalService, and Service entity relationships.
- [x] Publish `llms.txt` as a supplementary machine-readable business summary.
- [ ] Verify the production property in Google Search Console and Bing Webmaster Tools, submit the
      sitemap, and request initial indexing after deployment.
- [ ] Create or verify the Google Business Profile and keep the business name, Orlando location,
      phone number, website, and service descriptions consistent with this site.
- [ ] Confirm the production host applies `_headers` (or equivalent host configuration) and inspect
      the deployed response headers. Python's local development server does not apply this file.

## Verified

Rendered headless at 1440px and at a true 390px viewport (via fixed-width iframe — Chrome on
Windows enforces a ~500px minimum window, so a plain `--window-size=390` screenshot crops rather
than reflows). No horizontal overflow at either width: `scrollWidth === clientWidth`.
