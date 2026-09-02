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

`gen_session.py` writes `session.html`: all 36 animation frames laid out in a
**3-wide grid**, so one screenshot captures the whole sequence rather than one
per frame. It writes `session.grid` alongside it with `W,H,cols,rows,count`.

Do not go back to a single tall column: Chrome's full-page screenshot drifts
vertically past roughly 20,000px, and the late frames come out offset. The grid
keeps both dimensions modest (4200 x 7344).

```bash
python3 gen_session.py     # writes session.html, session.durations, session.grid
# screenshot session.html full-page at viewport width 4200 -> sheet.png
python3 - <<'EOF'
from PIL import Image
W, H, COLS, ROWS, N = [int(x) for x in open('session.grid').read().split(',')]
durs = [int(x) for x in open('session.durations').read().split(',')]
sheet = Image.open('sheet.png')
assert sheet.size == (W*COLS, H*ROWS), sheet.size      # catches a drifted capture
frames = []
for i in range(N):
    r, c = divmod(i, COLS)
    frames.append(sheet.crop((c*W, r*H, (c+1)*W, (r+1)*H)).convert('RGB'))
merged = Image.new('RGB', (W, H*N))
for i, f in enumerate(frames): merged.paste(f, (0, i*H))
ref = merged.quantize(colors=96)           # one palette for all frames, or the
q = [f.quantize(palette=ref, dither=Image.NONE) for f in frames]   # greys shimmer
q[0].save('../images/warp-session.gif', save_all=True, append_images=q[1:],
          duration=durs, loop=0, optimize=True, disposal=1)
EOF
```

Edit the copy, the frame list or the per-frame durations in `gen_session.py`
and re-run. 16:7 to match the `.media--wide` box.

The sequence: connect a Slack channel as a source, then ask the project brain
a question and watch it answer, citing that channel.

Two things about file size, both counterintuitive:

- **`disposal=1`, not `2`.** Disposal 2 forces every frame to be a full image;
  disposal 1 lets Pillow crop each frame to just the changed region. On this
  clip that is 1061KB versus 273KB — the same 36 frames.
- **Do not downscale the frames.** Resampling softens the edges and the noise
  defeats run-length compression, so the GIF gets *larger*. Cut frames instead.

Always play the result back and diff it against the source frames before
shipping — a bad capture or a disposal mistake looks fine frame-by-frame and
only shows up in playback.

Replace all of these with real screen recordings when those exist.
