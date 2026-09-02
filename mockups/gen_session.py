# -*- coding: utf-8 -*-
"""Emit every animation frame stacked vertically, so one screenshot captures
the whole sequence and Pillow can slice it into a GIF."""
import io, os

W, H = 1400, 612
QUERY = "Group Steering Committee — Q3 Review"
REPLY = ("<b>Granola note — Group-level check-in.</b> Kaine confirmed Phase 1 budget is on "
         "track; Ashford flagged interest in Hive OS as a template for Umbrella "
         "Pharmaceuticals’ and Consumer Health’s own legacy plant-ops systems, contingent "
         "on a clean Raccoon City cutover.")

# same four glyphs as the still image, so the pair reads as one product
ICONS = {
 'talk':   '<svg viewBox="0 0 24 24"><path d="M4 4h11a2 2 0 012 2v6a2 2 0 01-2 2H8l-4 4V4z"/></svg>',
 'people': '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9" r="2.6"/>'
           '<path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6H3zm13 0c0-2.2-.9-4.2-2.3-5.6 1-.3 2-.4 3.3-.4 2.8 0 5 2.2 5 5v1h-6z"/></svg>',
 'spark':  '<svg viewBox="0 0 24 24"><path d="M12 2l1.3 5.2L18 5.6l-2.4 4.6L21 12l-5.4 1.8L18 18.4'
           'l-4.7-1.6L12 22l-1.3-5.2L6 18.4l2.4-4.6L3 12l5.4-1.8L6 5.6l4.7 1.6L12 2z"/></svg>',
 'code':   '<svg viewBox="0 0 24 24"><path d="M9.4 6.6L3 12l6.4 5.4 1.5-1.8L6.1 12l4.8-3.6L9.4 6.6zm5.2 0'
           'l-1.5 1.8L17.9 12l-4.8 3.6 1.5 1.8L21 12l-6.4-5.4z"/></svg>',
}
SOURCES = [
    ("Meetings &amp; conversations", "48 transcripts", 'talk'),
    ("Client &amp; commercial context", "12 docs", 'people'),
    ("Design &amp; research", "31 files", 'spark'),
    ("Product, code &amp; delivery", "2 repos", 'code'),
]

SPARK = ('<svg viewBox="0 0 24 24"><path d="M12 1c1 6.6 5.4 11 12 12-6.6 1-11 5.4-12 12'
         '-1-6.6-5.4-11-12-12 6.6-1 11-5.4 12-12z"/></svg>')

def reply_upto(frac):
    """Reveal the reply a word at a time, keeping the bold lead intact."""
    if frac <= 0:
        return ''
    words = REPLY.split(' ')
    n = max(1, int(len(words) * frac))
    out = ' '.join(words[:n])
    if out.count('<b>') > out.count('</b>'):
        out += '</b>'
    return out

def frame(typed=None, sent=False, dots=0, reply=0.0, cited=False):
    src = ''.join(
        '<div class="grp"><span class="ic">%s</span>'
        '<span class="tx"><span class="nm">%s</span><span class="ct">%s</span></span>'
        '<span class="chk"><svg viewBox="0 0 24 24"><path d="M4 12l5 5L20 6"/></svg></span></div>'
        % (ICONS[i], n, c) for n, c, i in SOURCES)

    thread = ''
    if sent:
        thread += ('<div class="ask"><div class="who"><span class="av"></span>'
                   '<span class="nm2">Damon</span></div><p>%s</p></div>' % QUERY)
    if dots:
        thread += ('<div class="rep"><div class="who"><span class="av av--b">%s</span>'
                   '<span class="nm2">Project brain</span></div>'
                   '<div class="dots">%s</div></div>'
                   % (SPARK, ''.join('<i class="%s"></i>' % ('on' if k < dots else '')
                                     for k in range(3))))
    if reply > 0:
        cite = ('<div class="cite">Cited: <b>Meetings &amp; conversations</b> · '
                'Group Steering Committee, 12 Sept</div>') if cited else ''
        thread += ('<div class="rep"><div class="who"><span class="av av--b">%s</span>'
                   '<span class="nm2">Project brain</span></div>'
                   '<div class="card"><p>%s</p>%s</div></div>'
                   % (SPARK, reply_upto(reply), cite))

    caret = '<span class="caret"></span>' if typed is not None else ''
    itxt = (typed or '') if typed is not None else 'Ask the project brain…'
    icls = 'ph' if typed is None else ''

    return ('<div class="f"><div class="app">'
            '<div class="bar"><span class="mark">%s</span>'
            '<span class="proj">Client × Loomery</span></div>'
            '<div class="src"><h3>Sources</h3>%s</div>'
            '<div class="chat"><div class="thread">%s</div>'
            '<div class="input"><p class="%s">%s%s</p>'
            '<svg viewBox="0 0 24 24" class="send"><path d="M3 20l18-8L3 4l4 8-4 8z"/></svg>'
            '</div></div></div></div>'
            % (SPARK, src, thread, icls, itxt, caret))

# (frame, duration ms)
SEQ = [
    (frame(),                                              900),
    (frame(typed="Group Steering Comm"),                   140),
    (frame(typed=QUERY),                                   700),
    (frame(sent=True, typed=None),                         320),
    (frame(sent=True, dots=1),                             240),
    (frame(sent=True, dots=2),                             240),
    (frame(sent=True, dots=3),                             240),
    (frame(sent=True, reply=0.22),                         190),
    (frame(sent=True, reply=0.45),                         190),
    (frame(sent=True, reply=0.70),                         190),
    (frame(sent=True, reply=1.0),                          700),
    (frame(sent=True, reply=1.0, cited=True),             2600),
]

CSS = """
*{box-sizing:border-box;margin:0}
body{width:%(W)spx;background:#e9e9f2;font-family:"The Future",Jost,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased}
.f{width:%(W)spx;height:%(H)spx;padding:26px;background:#e9e9f2}
.app{height:100%%;background:#fff;border:1px solid #dcdce8;border-radius:12px;overflow:hidden;
  box-shadow:0 14px 34px rgba(24,24,37,.10);display:grid;
  grid-template-rows:50px 1fr;grid-template-columns:310px 1fr}
.bar{grid-column:1/-1;display:flex;align-items:center;gap:12px;padding:0 18px;
  border-bottom:1px solid #ececf4;background:#fafaff}
.mark{width:24px;height:24px;border-radius:7px;background:#5b4ee9;display:grid;place-items:center;flex:none}
.mark svg{width:14px;height:14px;fill:#fff}
.proj{font-size:17px;font-weight:600;color:#181825}
.src{border-right:1px solid #ececf4;padding:16px 14px;background:#fafaff}
.src h3{font-size:15px;font-weight:600;color:#181825;margin-bottom:12px}
.grp{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:8px;margin-bottom:7px;
  background:#f6f5ff;box-shadow:inset 0 0 0 1px #e0dcfb}
.ic{width:22px;height:22px;border-radius:6px;background:#eae8fd;display:grid;place-items:center;flex:none}
.ic svg{width:13px;height:13px;fill:#5b4ee9}
.tx{min-width:0;display:flex;flex-direction:column}
.nm{font-size:13.5px;font-weight:600;color:#181825;line-height:1.25}
.ct{font-size:12px;color:#8484a4}
.chk{margin-left:auto;width:15px;height:15px;border-radius:4px;border:1.4px solid #b9b2f5;
  display:grid;place-items:center;flex:none}
.chk svg{width:9px;height:9px;fill:none;stroke:#5b4ee9;stroke-width:3}
.chat{display:flex;flex-direction:column;padding:16px 20px;overflow:hidden}
.thread{flex:1;display:flex;flex-direction:column;gap:12px;overflow:hidden}
.who{display:flex;align-items:center;gap:9px;margin-bottom:8px}
.av{width:22px;height:22px;border-radius:6px;background:#d8d8e8;flex:none}
.av--b{background:#181825;display:grid;place-items:center}
.av--b svg{width:13px;height:13px;fill:#3fffc5}
.nm2{font-size:14px;font-weight:600;color:#181825}
.ask{align-self:flex-end;max-width:76%%;background:#f2f2f8;border-radius:12px 12px 3px 12px;padding:13px 16px}
.ask p{font-size:15px;line-height:1.4;color:#181825}
.rep{max-width:94%%;background:#eae8fd;border-radius:12px 12px 12px 3px;padding:13px}
.rep .card{background:#fff;border-radius:9px;padding:13px 15px}
.rep p{font-size:15px;line-height:1.5;color:#181825}
.rep p b{font-weight:600}
.dots{display:flex;gap:6px;padding:6px 4px 2px}
.dots i{width:8px;height:8px;border-radius:50%%;background:#c9c4f7}
.dots i.on{background:#5b4ee9}
.cite{margin-top:10px;padding-top:9px;border-top:1px solid #ececf4;
  font-size:12.5px;color:#545472}
.cite b{color:#5b4ee9;font-weight:600}
.input{margin-top:14px;border:1px solid #dcdce8;border-radius:11px;padding:13px 16px;
  display:flex;align-items:center;gap:14px}
.input p{font-size:15px;line-height:1.4;color:#181825}
.input p.ph{color:#a3a3ba}
.send{width:20px;height:20px;fill:none;stroke:#5b4ee9;stroke-width:1.8;flex:none}
.caret{display:inline-block;width:2px;height:15px;background:#181825;vertical-align:-2px;margin-left:1px}
""" % {'W': W, 'H': H}

FONTS = """
@font-face{font-family:"The Future";font-weight:400;src:url("https://cdn.prod.website-files.com/5f4d0bcb4cc4d2b9e0b3005d/66d0793c6f7b8627595515dd_the-future-regular.woff2") format("woff2")}
@font-face{font-family:"The Future";font-weight:500;src:url("https://cdn.prod.website-files.com/5f4d0bcb4cc4d2b9e0b3005d/66d0793c8d5fc3a693e0c1f4_the-future-medium.woff2") format("woff2")}
@font-face{font-family:"The Future";font-weight:600 700;src:url("https://cdn.prod.website-files.com/5f4d0bcb4cc4d2b9e0b3005d/66d0793cd205f1234adef23b_the-future-bold.woff2") format("woff2")}
"""

html = ('<meta charset="utf-8"><style>%s%s</style>%s'
        % (FONTS, CSS, ''.join(f for f, _ in SEQ)))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'session.html')
open(out, 'w', encoding='utf-8').write(html)
open(out.replace('.html', '.durations'), 'w').write(','.join(str(d) for _, d in SEQ))
print('frames:', len(SEQ), '| strip height:', len(SEQ) * H, '| ->', out)
