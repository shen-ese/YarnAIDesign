# YarnAI — page design

An HTML prototype of the YarnAI page, built to be rebuilt in Webflow. Every
animation here is either something Webflow Interactions can do natively, or is
flagged in [`WEBFLOW.md`](WEBFLOW.md) as needing a custom-code embed, with the
native fallback written out.

This is a design artefact, not a production app. There is no build step and no
dependencies.

## Run it

```bash
python3 dev/serve.py
```

Then open http://localhost:8777.

`dev/serve.py` is a plain static server that sends `no-store` on everything. Use it
rather than `python3 -m http.server` — the browser will otherwise cache
`index.html` / `styles.css` / `motion.js` and edits silently won't appear, which
looks exactly like the animations being broken.

## What's here

| File | |
|---|---|
| `index.html` | The whole page — 13 sections |
| `styles.css` | All styling, including the animation timings |
| `tokens.css` | Design tokens, mirroring the Figma `semantic` collection |
| `motion.js` | Stands in for Webflow IX2 in this prototype |
| `dev/serve.py` | No-cache dev server |
| `WEBFLOW.md` | **Read this before rebuilding.** Section inventory, IX2 recipes, and the decisions that aren't obvious from the code |
| `docs/screens/` | Reference screenshots |
| `images/` | Case-study stills and product marks |

## Before this ships

- **Four media placeholders need real recordings** — Warp, Heddle, Bobbin and
  the Warp session. Each is a dashed box saying what belongs there. See
  `WEBFLOW.md` §5.
- **The Future loads from Loomery's Webflow CDN**, declared as `@font-face` at
  the top of `tokens.css`. The files are licensed, so they are referenced
  rather than committed. Jost and IBM Plex Mono stay in the stack as an
  offline fallback. In Webflow this block isn't needed — the fonts are already
  uploaded under Project Settings → Fonts.
- **The sticky sub-nav sits at `top: 0`.** If the main Loomery nav is also
  sticky, one of them has to give. Decide before build.
- **Mobile hasn't had a pass.** Breakpoints exist and the layout holds, but it
  hasn't been designed.
