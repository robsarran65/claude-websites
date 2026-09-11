# Sarran AI Connect — test results

Date: September 11, 2026

## Passed

- All 11 HTML pages contain one H1 and no duplicate IDs.
- Every local page, image, stylesheet, script, contact file, and internal destination referenced by the site exists.
- JavaScript syntax is valid.
- The stylesheet is structurally balanced.
- The shared CSS and JavaScript filenames match their content hashes, and all 11 pages reference the current files.
- JSON, JSON-LD, sitemap XML, and `vercel.json` parse successfully.
- The Vercel `/connect` to `/connect.html` rewrite is present.
- The four challenge choices have matching JavaScript recommendations and valid service destinations.
- The cinematic introduction has a visible skip control, clears without JavaScript, hands focus to the hero when needed, and is bypassed for reduced motion.
- All four illustrative workflows support completion, skip, and replay without allowing the progress indicator to move backward.
- The time-savings control is clamped to valid values, uses 48 working weeks, keeps its painted track aligned to the range thumb, and records the illustrative scenario in the inquiry form.
- The page includes keyboard focus handling, dedicated live announcements, 44 pixel minimum controls, reduced-motion support, and 860, 680, and 380 pixel responsive breakpoints.
- The PNG and SVG QR matrices match the encoded address `https://www.sarranai.com/connect`.
- The QR has high error correction, a four-module quiet zone, two high-contrast colors, and a 1640 × 1640 PNG.
- Robert’s vCard contains the expected business, phone, email, website, and LinkedIn information and uses vCard-compatible CRLF line endings.
- Local HTTP checks returned the Connect page, homepage, and downloadable contact card successfully.
- An independent read-only review checked interaction order, motion resilience, estimator math, progress state, links, fragments, assets, structured data, and content hashes.

## Deferred until Robert’s local review

- Visual browser review on Robert’s Windows computer and iPhone.
- Actual FormSubmit delivery. The form was not submitted during automated testing, so no test lead was emailed.
- Contact import confirmation on Robert’s iPhone.

## Deferred until Vercel deployment

- The clean public `/connect` route and production security headers.
- Activation and second inbox-delivery verification for FormSubmit on the production origin.
- Analytics collection. The page exposes privacy-safe interaction events, but no external analytics collector was added during the local-only build.
- Live scanning of the production QR destination. The QR already contains the final URL and will begin resolving when the route is deployed.
