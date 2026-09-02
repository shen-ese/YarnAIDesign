# Building this page in Webflow

Everything here is limited to what Webflow can do natively. No animation
library. Two small custom-code embeds, both optional.

Run locally: `python3 dev/serve.py` — not `python3 -m http.server`, which
lets the browser cache your edits away.

---

## 1 · Setup

**Tokens.** Paste `tokens.css` into **Project Settings → Custom Code → Head**
inside `<style>`. Webflow reads custom properties; in the Designer you type
`var(--surface-inverse)` into any colour field.

**Fonts.** The prototype loads **The Future** and **The Future Mono** from
Loomery's own Webflow CDN, declared as `@font-face` at the top of `tokens.css`.
Jost and IBM Plex Mono remain in the stack as an offline fallback.

**Delete that `@font-face` block when you build in Webflow** — the fonts are
already uploaded under Project Settings → Fonts, and a second declaration
pointing at raw CDN URLs will only fight it.

One gotcha: The Future has no 600 weight. The bold face is declared across the
`600 700` range so the page's `font-weight: 600` headings resolve to it rather
than to a synthesised bold. In Webflow, set headings to **Bold (700)** — a 600
in the Designer will render as faux-bold.

**Reduced motion.** Webflow does **not** respect `prefers-reduced-motion` by
default. The media query at the bottom of `tokens.css` handles it — keep it.

---

## 2 · Section inventory

| # | Section | Class | Ground | Ranked |
|---|---|---|---|---|
| 1 | Nav | `.nav` | page | — |
| 2 | Hero | `.hero` | inverse | — |
| 3 | Sub-nav (sticky) | `.subnav` | page | — |
| 4 | The Gap | `#gap` | inverse | — |
| 5 | Where the time goes | `#lifecycle` | page | ● |
| 6 | The stack | `#stack` | sunk | — |
| 7 | Warp deep dive | `#warp` | page | — |
| 8 | Principles | `#principles` | sunk | — |
| 9 | Evidence | `#evidence` | page | ● |
| 10 | Team shape | `#team` | sunk | — |
| 11 | Maturity | `#maturity` | inverse | — |
| 12 | How clients engage | `#engage` | sunk | ● |
| 13 | CTA + footer | `.cta` / `.footer` | inverse | — |

**Ranked** sections get `.section--ranked` (176px top padding), a `.rank-rule`
and an indigo eyebrow. That is the whole ranking device — no type-size change.
No two adjacent sections share a ground.

---

## 3 · Animations, as IX2 recipes

Every animated property below is **width, flex-grow, opacity or transform** —
what IX2 drives natively.

### 3.1 · Reveal on scroll — `.reveal`

**Trigger:** Element → **Scroll into view**, offset 15%, play **once**.
**Animation:** Opacity `0 → 100%`, Move Y `18px → 0`, 0.42s, ease-out.
Stagger with `data-d="1..4"` → delays 80 / 160 / 240 / 320ms.

Apply to one element and use **"Apply to class"** so every `.reveal` inherits it.

### 3.2 · Where the time goes — `#cycle`

The lifecycle diagram runs on a timer and has its own section — see **7**.

### 3.3 · Team shape — `#teamA`

Same pattern, different properties. Easing ease-in-out, 0.9s.

| Target | Action | From | To |
|---|---|---|---|
| `.role--core` (×2) | Flex grow | 1 | 2.4 |
| `.role--core` | Background | page | inverse |
| `.role--absorbed` (×5) | Opacity | 1 | 0.28 |
| `.role--absorbed` | Flex grow | 1 | 0.35 |
| `.role--agents` | Opacity + Move Y | 0 / 10px | 1 / 0 |
| `.role--counsel` | Opacity + Move Y | 0 / 10px | 1 / 0 |

IX2 can animate flex-grow via the **Size** action on a flex child. If it fights
you, swap `flex-grow` for explicit `width` percentages — the effect is identical.

### 3.4 · Maturity meters — `.level__meter i`

**Trigger:** Scroll into view on `.levels`, once.
**Animation:** width `0 → 25 / 50 / 75 / 100%`, 0.9s ease-out, delays 0 / 120 /
240 / 360ms.

### 3.5 · Hero — digital yarn

The hero is one inline SVG in three layers:

1. **The dot field** — a 30×30 lattice of 1.6px white dots (`<pattern id="dots">`),
   masked by a left-to-right gradient so it sits at roughly 5% behind the copy and
   30% out on the right. Same visual language as the product marks.
2. **The sparkle** — a handful of dots in that same lattice, lit indigo and mint,
   arranged as a four-point burst. It is not a separate icon: it is the grid,
   turned on. Sits in the pocket the routing leaves clear, bottom-centre-right.
3. **The yarn** — seven orthogonal traces, three travelling pulses and eight
   glowing junction nodes.

**The fade.** The traces run the full 1440 width and start *behind* the copy at
zero opacity, reaching full by the right edge. One mask (`yarnMask`) does it,
and its gradient is deliberately eased rather than linear — a straight ramp
would already be at 60% where the headline ends, which is unreadable. The stops
hold under 12% across the whole copy column, then climb hard from 62% onward.

If the headline ever gets longer, move the `fadeYarn` stops right — don't move
the paths. The paths are supposed to run the full width; the mask is the only
thing that decides where they are visible.

In Webflow it goes in as a single **Embed** containing the `<svg>` plus the
`.weave-*` block from the bottom of `styles.css`.

`stroke-dashoffset` is **not** an IX2 property, so the trace draw and the pulses
have to be CSS. That's the one place worth spending an embed — it's the hero and
the pulses are the thing that makes it feel alive rather than decorative.

**Native fallback if you'd rather not embed:** export the SVG static, drop the
pulses, and fade the whole thing in with opacity on page load. You lose the
signal travelling through the weave, which is most of the impact.

**Editing it later:** the traces are plain `H`/`V` path commands — horizontal
and vertical moves only, no curves. Anyone can nudge a route by changing two
numbers. Node positions are `translate(x y)` on the outer `<g>`; the inner `<g>`
carries the animation, so never move the transform onto the animated element or
the node jumps to the top-left corner.

---

## 4 · The two things Webflow can't do

1. **Counting numbers.** IX2 cannot animate text content. Either embed the
   `countTo` function from `motion.js` (~20 lines) or use static numbers.
   Honest recommendation: **static.** It's the least valuable animation here.
2. **The hero thread draw.** See 3.5.

Everything else is native.

---

## 5 · Media

The three product images in the Built by Loomery section are **mockups**, not
real screenshots: `images/product-warp.png`, `product-heddle.png`,
`product-bobbin.png`. They are rendered from HTML in `mockups/`, so they can be
edited and re-rendered rather than redrawn — see `mockups/README.md`.

Swap them for real screen recordings when those exist. The `.media` box already
sets `object-fit: cover` and a 16:10 ratio, so nothing needs resizing first.

**If you use video:** always `muted` + `playsinline` or iOS won't autoplay, and
add a `poster` so there's something to look at before it loads.

One still outstanding: the `warp-session` slot in the Warp deep dive.

## 6 · Gotchas

- **Percentages, not pixels** on the before/after widths. Converting them to px
  in the Designer breaks the diagram below 1240.
- **`overflow: hidden` on `.lb`** stops labels spilling as bars narrow.
- **10,000 character limit** on per-page custom code for some plans. Tokens are
  well under; watch it as embeds accumulate.
- **`* { border-radius: 0 }`** in tokens is a blunt instrument that suits a
  prototype. In Webflow set radius 0 on base classes instead, or it will fight
  any component that later needs a radius.
- **The sticky sub-nav** sits at `top: 0`. If the main Loomery nav is also
  sticky, one of them has to give — decide before build.

---

## 7 · The lifecycle walkthrough

`#lifecycle` now carries one treatment: `.lc` — four steps on a timer, with
buttons that jump the reader to a step without stopping the cycle. v1 (morph
with toggle) and v6 (button-driven stepper) were removed, along with the
`.ba-track` / `.ba-stage` / `.ba-reclaimed` CSS only v1 used. The `.ba-toggle`,
`.ba-btn` and `.ba-metric` rules stay — the team section and this readout still
use them.

### 7.1 · Timing

`--dwell: 3400ms` per step, `--dwell-last: 5200ms` on step 4 so the end state —
the whole point of the section — holds before it loops back. Both live on `.lc`
in CSS and the script reads them back, so retiming is a one-line CSS change.

Each step marker carries a 2px `.lc__tick` that scales 0 → 1 over the dwell, so
it is visible that this is on a timer and roughly how long is left. It runs on
the current marker only, via `[aria-current="true"]`, so advancing restarts it
for free.

### 7.2 · What stops it, and what doesn't

One function (`sync`) owns the timer, so the reasons it can stop cannot fight:

| Event | Pauses? | Why |
|---|---|---|
| Not wholly on screen | Yes | See below. |
| Hovered | Yes | A step must not move under someone reading it. Resumes where it left off, not from the top of the step. |
| Focused **by keyboard** | Yes | Same reason, for anyone tabbing through. |
| Focused **by mouse click** | **No** | See the focus trap below. |
| Step button clicked | No | Jumps to that step and carries on with a full dwell. |

**Starting on scroll — get the gate right.** The obvious version, "start at 35%
visible", fires while the diagram is still clipping the bottom edge: measured,
only 143px of its 302px height was on screen, top edge at 757px in a 900px
viewport. The reader then spends another second or two scrolling it into a
comfortable position, by which point it is a step or two in — which reads as
*"it didn't start on scroll, it was already running."*

The gate is therefore the **whole block being on screen** (`intersectionRatio
>= 0.99`), with a fallback for the case where the block is taller than the
viewport and can never satisfy that. Measured after the fix: it starts at top
577 / bottom 878 in a 900px viewport, wholly visible, on step 1.

**Coming back to it.** A second observer at threshold 0 tracks whether the block
has *fully* left the viewport. If it has, the next arrival replays from step 1
rather than resuming mid-sequence. A small scroll that only dips it below the
ready line does not reset it — verified: nudged 180px and back, still on step 3.

**Reduced motion.** No cycling — it lands on step 4 and the buttons still work.

### 7.3 · The transition itself

A click can be blunt, because the reader caused it. An unattended transition
cannot — nobody is expecting it, so it has to explain itself:

| Problem | Fix |
|---|---|
| The caption hard-cut ~120ms *before* the bars moved, so the words changed and the picture caught up | `.lc__cap` cross-fades: 150ms out, swap, 280ms in |
| Counters finished in 600ms while the bars ran 900ms, then sat dead | `go(n, dur)` passes the bar duration to the counter |
| Every bar moved in lockstep, so the eye had nowhere to land | Stagger by **distance from Build**: 0 / 60 / 120 / 180ms, gain block last at 260ms |

The stagger direction matters. Build is the bottleneck and its collapse is the
argument; leading with it and letting the other five follow makes the diagram
read as cause and effect rather than as six bars resizing. Left-to-right would
put Discover first, which is the least interesting bar on the chart.

**The loop.** Step 4 back to step 1 is not a fifth step. `.is-rewind` gives it
one slower, unstaggered 1150ms move so it reads as a deliberate reset. The class
is removed afterwards so the next forward step re-staggers.

### 7.4 · Building it in Webflow

The four bar-width sets are four click-triggered interactions, same as any
stepper. What IX2 cannot do is the *timer*. Options, best first:

1. **Loop an animation on scroll-into-view.** One IX2 animation with all four
   states on a single timeline (widths at 0s / 3.4s / 6.8s / 10.2s), trigger
   "Scroll into view", **Loop** on. You lose hover-pause, the countdown ticks,
   and the ability to hand control to the buttons.
2. **Embed the `.lc` block from `motion.js`** (~120 lines) and keep everything.
   This is what the prototype does.

Option 2 is worth the embed. Pause-on-hover is what stops an auto-rotating
diagram being annoying, and it is precisely the part IX2 cannot express.

### 7.5 · The metric row

`.ba-metric` markup, driven by a four-value list (`data-steps="12,11,7,6"`).
The numbers are derived from the bar widths, so if you retime the diagram,
retime these too:

| Step | Weeks, kick-off to live | Weeks reclaimed | Stages with agents |
|---|---|---|---|
| 1 | 12 | 0 | 0/6 |
| 2 | 11 | 1 | 2/6 |
| 3 | 7 | 5 | 3/6 |
| 4 | 6 | 6 | 6/6 |

Counting numbers is the one thing IX2 cannot do (see section 4). Static numbers
per step are a fine fallback — swap the text with a click interaction.

v1–v6 (morph toggle, reveal slider, stacked pair, scroll scrub, ghost overlay,
button stepper) were built, compared and removed. They are in git history.
