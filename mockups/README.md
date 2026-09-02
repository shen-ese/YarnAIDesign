# Product mockup sources

The product images are rendered from these files, not painted by hand — so
they can be edited and re-rendered rather than redrawn. They pull The Future
from Loomery's Webflow CDN, so they match the page.

```bash
cd mockups && python3 -m http.server 8899
```

## Stills — `images/product-*.png`

`warp.html`, `heddle.html`, `bobbin.html`. Screenshot each at **1600×1000**
(2.6× the size it renders at on the page, which keeps it crisp) and save over
the matching `images/product-*.png`.

## The Warp session GIF — `images/warp-session.gif`

`gen_session.py` writes `session.html`: every animation frame stacked
vertically as one tall page. That means **one** screenshot captures the whole
sequence, rather than one per frame.

```bash
python3 gen_session.py          # writes session.html + session.durations
# screenshot session.html full-page at width 1400 -> strip.png
python3 - <<'EOF'
from PIL import Image
strip = Image.open('strip.png')
durs = [int(x) for x in open('session.durations').read().split(',')]
W, H = 1400, 612
frames = [strip.crop((0, i*H, W, (i+1)*H)).convert('RGB') for i in range(len(durs))]
merged = Image.new('RGB', (W, H*len(frames)))
for i, f in enumerate(frames): merged.paste(f, (0, i*H))
ref = merged.quantize(colors=128)          # one palette for all frames, or the
q = [f.quantize(palette=ref, dither=Image.NONE) for f in frames]   # greys shimmer
q[0].save('../images/warp-session.gif', save_all=True, append_images=q[1:],
          duration=durs, loop=0, optimize=True, disposal=2)
EOF
```

Edit the copy, the frame list or the per-frame durations in `gen_session.py`
and re-run. 16:7 to match the `.media--wide` box.

Replace all of these with real screen recordings when those exist.
