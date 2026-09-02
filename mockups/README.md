# Product mockup sources

The three product images in `images/product-*.png` are rendered from these
files, not painted by hand — so they can be edited and re-rendered rather
than redrawn.

```bash
cd mockups && python3 -m http.server 8899
```

Then screenshot each at **1600×1000** (2.6× the size it renders at on the
page, which keeps it crisp) and save over the matching `images/product-*.png`.

They pull The Future from Loomery's Webflow CDN, so they match the page.

Replace them with real screen recordings when those exist — see WEBFLOW.md §5.
