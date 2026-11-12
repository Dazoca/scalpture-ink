# Scalpture Ink

Single-page site for Scalpture Ink — scalp micropigmentation studio, Johannesburg.

## Contents

- `index.html` — the production page (bundled; all assets embedded as base64 blobs)
- `scalpture-ink.html` — pristine original export, kept as the source of truth
- `scripts/responsive.py` — rebuilds `index.html` from the original with the mobile layer applied

## Responsive work

`index.html` is generated. Desktop styles are untouched; a responsive layer is appended to the
template's stylesheet plus a few structural `si-*` classes:

- **≤ 900px** — treatment cards go 2-up, footers collapse to 2 columns, spacing tightens
- **≤ 640px** — single-column layouts, hero stacks, proof strip 2×2, FAQ/process stack,
  chapter dock becomes a compact 5-cell control (About / Treat / Proof / Steps / Book),
  header drops the location tag and shows a short "Book" CTA
- **≤ 390px** — tighter type scale, brand wordmark hidden, one-column footer
- `prefers-reduced-motion` disables the parallax/reveal animation

Verified at 320 / 390 / 1440px: no horizontal overflow, no JS errors.

### Rebuilding after an export change

```sh
cp path/to/new-export.html scalpture-ink.html
python3 scripts/responsive.py
```

## Local preview

```sh
python3 -m http.server 8080
# http://localhost:8080
```

## Deploy

Static — ready for Vercel, GitHub Pages, Netlify or any bucket.
