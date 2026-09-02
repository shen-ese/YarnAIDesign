# -*- coding: utf-8 -*-
"""Emit every animation frame stacked vertically, so one screenshot captures
the whole sequence and Pillow can slice it into a GIF.

Sequence: connect a Slack channel as a source, then ask the project brain a
question and watch it answer from that source.
"""
import os

W, H = 1400, 612
COLS = 3            # frames laid out in a grid, not one tall column
QUERY = "Group Steering Committee — Q3 Review"
REPLY = ("<b>Granola note — Group-level check-in.</b> Kaine confirmed Phase 1 budget is on "
         "track; Ashford flagged interest in Hive OS as a template for Umbrella "
         "Pharmaceuticals’ and Consumer Health’s own legacy plant-ops systems, contingent "
         "on a clean Raccoon City cutover.")

ICONS = {
 'talk':   '<svg viewBox="0 0 24 24"><path d="M4 4h11a2 2 0 012 2v6a2 2 0 01-2 2H8l-4 4V4z"/></svg>',
 'people': '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9" r="2.6"/>'
           '<path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6H3zm13 0c0-2.2-.9-4.2-2.3-5.6 1-.3 2-.4 3.3-.4 2.8 0 5 2.2 5 5v1h-6z"/></svg>',
 'spark':  '<svg viewBox="0 0 24 24"><path d="M12 2l1.3 5.2L18 5.6l-2.4 4.6L21 12l-5.4 1.8L18 18.4'
           'l-4.7-1.6L12 22l-1.3-5.2L6 18.4l2.4-4.6L3 12l5.4-1.8L6 5.6l4.7 1.6L12 2z"/></svg>',
 'code':   '<svg viewBox="0 0 24 24"><path d="M9.4 6.6L3 12l6.4 5.4 1.5-1.8L6.1 12l4.8-3.6L9.4 6.6zm5.2 0'
           'l-1.5 1.8L17.9 12l-4.8 3.6 1.5 1.8L21 12l-6.4-5.4z"/></svg>',
 'hash':   '<svg viewBox="0 0 24 24"><path d="M9 3L7.5 21h2L11 3H9zm5.5 0L13 21h2L16.5 3h-2zM4 8v2h16V8H4zm0 6v2h16v-2H4z"/></svg>',
}
SPARK = ICONS['spark']

BASE_SOURCES = [
    ("Meetings &amp; conversations", "48 transcripts", 'talk'),
    ("Client &amp; commercial context", "12 docs", 'people'),
    ("Design &amp; research", "31 files", 'spark'),
    ("Product, code &amp; delivery", "2 repos", 'code'),
]
SLACK_SOURCE = ("Slack · #umbrella-loomery", "live channel", 'hash')

# name, brand colour, official mark (simple-icons, CC0)
CONNECTORS = [
    ("Slack", "#4A154B",
     "M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312zM15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z"),
    ("Drive", "#4285F4",
     "M12.01 1.485c-2.082 0-3.754.02-3.743.047.01.02 1.708 3.001 3.774 6.62l3.76 6.574h3.76c2.081 0 3.753-.02 3.742-.047-.005-.02-1.708-3.001-3.775-6.62l-3.76-6.574zm-4.76 1.73a789.828 789.861 0 0 0-3.63 6.319L0 15.868l1.89 3.298 1.885 3.297 3.62-6.335 3.618-6.33-1.88-3.287C8.1 4.704 7.255 3.22 7.25 3.214zm2.259 12.653-.203.348c-.114.198-.96 1.672-1.88 3.287a423.93 423.948 0 0 1-1.698 2.97c-.01.026 3.24.042 7.222.042h7.244l1.796-3.157c.992-1.734 1.85-3.23 1.906-3.323l.104-.167h-7.249z"),
    ("Notion", "#181825",
     "M4.459 4.208c.746.606 1.026.56 2.428.466l13.215-.793c.28 0 .047-.28-.046-.326L17.86 1.968c-.42-.326-.981-.7-2.055-.607L3.01 2.295c-.466.046-.56.28-.374.466zm.793 3.08v13.904c0 .747.373 1.027 1.214.98l14.523-.84c.841-.046.935-.56.935-1.167V6.354c0-.606-.233-.933-.748-.887l-15.177.887c-.56.047-.747.327-.747.933zm14.337.745c.093.42 0 .84-.42.888l-.7.14v10.264c-.608.327-1.168.514-1.635.514-.748 0-.935-.234-1.495-.933l-4.577-7.186v6.952L12.21 19s0 .84-1.168.84l-3.222.186c-.093-.186 0-.653.327-.746l.84-.233V9.854L7.822 9.76c-.094-.42.14-1.026.793-1.073l3.456-.233 4.764 7.279v-6.44l-1.215-.139c-.093-.514.28-.887.747-.933zM1.936 1.035l13.31-.98c1.634-.14 2.055-.047 3.082.7l4.249 2.986c.7.513.934.653.934 1.213v16.378c0 1.026-.373 1.634-1.68 1.726l-15.458.934c-.98.047-1.448-.093-1.962-.747l-3.129-4.06c-.56-.747-.793-1.306-.793-1.96V2.667c0-.839.374-1.54 1.447-1.632z"),
    ("Jira", "#0052CC",
     "M11.571 11.513H0a5.218 5.218 0 0 0 5.232 5.215h2.13v2.057A5.215 5.215 0 0 0 12.575 24V12.518a1.005 1.005 0 0 0-1.005-1.005zm5.723-5.756H5.736a5.215 5.215 0 0 0 5.215 5.214h2.129v2.058a5.218 5.218 0 0 0 5.215 5.214V6.758a1.001 1.001 0 0 0-1.001-1.001zM23.013 0H11.455a5.215 5.215 0 0 0 5.215 5.215h2.129v2.057A5.215 5.215 0 0 0 24 12.483V1.005A1.001 1.001 0 0 0 23.013 0Z"),
    ("Figma", "#F24E1E",
     "M15.852 8.981h-4.588V0h4.588c2.476 0 4.49 2.014 4.49 4.49s-2.014 4.491-4.49 4.491zM12.735 7.51h3.117c1.665 0 3.019-1.355 3.019-3.019s-1.355-3.019-3.019-3.019h-3.117V7.51zm0 1.471H8.148c-2.476 0-4.49-2.014-4.49-4.49S5.672 0 8.148 0h4.588v8.981zm-4.587-7.51c-1.665 0-3.019 1.355-3.019 3.019s1.354 3.02 3.019 3.02h3.117V1.471H8.148zm4.587 15.019H8.148c-2.476 0-4.49-2.014-4.49-4.49s2.014-4.49 4.49-4.49h4.588v8.98zM8.148 8.981c-1.665 0-3.019 1.355-3.019 3.019s1.355 3.019 3.019 3.019h3.117V8.981H8.148zM8.172 24c-2.489 0-4.515-2.014-4.515-4.49s2.014-4.49 4.49-4.49h4.588v4.441c0 2.503-2.047 4.539-4.563 4.539zm-.024-7.51a3.023 3.023 0 0 0-3.019 3.019c0 1.665 1.365 3.019 3.044 3.019 1.705 0 3.093-1.376 3.093-3.068v-2.97H8.148zm7.704 0h-.098c-2.476 0-4.49-2.014-4.49-4.49s2.014-4.49 4.49-4.49h.098c2.476 0 4.49 2.014 4.49 4.49s-2.014 4.49-4.49 4.49zm-.097-7.509c-1.665 0-3.019 1.355-3.019 3.019s1.355 3.019 3.019 3.019h.098c1.665 0 3.019-1.355 3.019-3.019s-1.355-3.019-3.019-3.019h-.098z"),
    ("Linear", "#5E6AD2",
     "M2.886 4.18A11.982 11.982 0 0 1 11.99 0C18.624 0 24 5.376 24 12.009c0 3.64-1.62 6.903-4.18 9.105L2.887 4.18ZM1.817 5.626l16.556 16.556c-.524.33-1.075.62-1.65.866L.951 7.277c.247-.575.537-1.126.866-1.65ZM.322 9.163l14.515 14.515c-.71.172-1.443.282-2.195.322L0 11.358a12 12 0 0 1 .322-2.195Zm-.17 4.862 9.823 9.824a12.02 12.02 0 0 1-9.824-9.824Z"),
]
CHANNELS = ["#umbrella-loomery", "#steering-committee", "#hive-os-build"]


def reply_upto(frac):
    if frac <= 0:
        return ''
    words = REPLY.split(' ')
    n = max(1, int(len(words) * frac))
    out = ' '.join(words[:n])
    if out.count('<b>') > out.count('</b>'):
        out += '</b>'
    return out


def modal_html(stage):
    """stage: grid | slack | dd | ddopen | chosen | confirm"""
    tiles = ''
    for name, col, d in CONNECTORS:
        on = ' on' if (name == 'Slack' and stage != 'grid') else ''
        tiles += ('<div class="ct%s"><span class="cl">'
                  '<svg viewBox="0 0 24 24" style="fill:%s"><path d="%s"/></svg></span>'
                  '<span class="cn">%s</span></div>' % (on, col, d, name))

    picker = ''
    if stage in ('dd', 'ddopen', 'chosen', 'confirm'):
        chosen = stage in ('chosen', 'confirm')
        label = CHANNELS[0] if chosen else 'Select a channel'
        opts = ''
        if stage == 'ddopen':
            opts = '<div class="opts">%s</div>' % ''.join(
                '<div class="opt%s">%s</div>' % (' on' if i == 0 else '', c)
                for i, c in enumerate(CHANNELS))
        picker = ('<div class="pk"><span class="pkl">Channel</span>'
                  '<div class="sel%s">%s<span class="cv">▾</span></div>%s</div>'
                  % ('' if chosen else ' ph', label, opts))

    ready = stage in ('chosen', 'confirm')
    btn = ('<div class="cta%s">Confirm connection</div>'
           % ('' if ready else ' off'))
    press = ' pressed' if stage == 'confirm' else ''
    return ('<div class="veil"><div class="modal%s"><h4>Connect a source</h4>'
            '<div class="grid">%s</div>%s%s</div></div>'
            % (press, tiles, picker, btn))


def frame(typed=None, sent=False, dots=0, reply=0.0, cited=False,
          modal=None, slack=False, act=None):
    srcs = list(BASE_SOURCES) + ([SLACK_SOURCE] if slack else [])
    rows = ''
    for i, (n, c, ic) in enumerate(srcs):
        fresh = ' fresh' if (slack and i == len(srcs) - 1) else ''
        rows += ('<div class="grp%s"><span class="ic">%s</span>'
                 '<span class="tx"><span class="nm">%s</span><span class="ct2">%s</span></span>'
                 '<span class="chk"><svg viewBox="0 0 24 24"><path d="M4 12l5 5L20 6"/></svg></span></div>'
                 % (fresh, ICONS[ic], n, c))

    thread = ''
    if sent:
        thread += ('<div class="ask"><div class="who"><span class="av">D</span>'
                   '<span class="nm2">Damon</span></div><p>%s</p></div>' % QUERY)
    if dots:
        thread += ('<div class="rep"><div class="who"><span class="av av--b">%s</span>'
                   '<span class="nm2">Project brain</span></div>'
                   '<div class="dots">%s</div></div>'
                   % (SPARK, ''.join('<i class="%s"></i>' % ('on' if k < dots else '')
                                     for k in range(3))))
    if reply > 0:
        cite = ('<div class="cite">Cited: <b>Slack · #umbrella-loomery</b> · '
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
            '<div class="src"><h3>Sources</h3>'
            '<div class="acts"><div class="add">＋ Add source</div>'
            '<div class="add add--alt%s">⇄ Connect source</div></div>'
            '%s<div class="conn%s">Connectors</div></div>'
            '<div class="chat"><div class="thread">%s</div>'
            '<div class="input"><p class="%s">%s%s</p>'
            '<svg viewBox="0 0 24 24" class="send"><path d="M3 20l18-8L3 4l4 8-4 8z"/></svg>'
            '</div></div>%s</div></div>'
            % (SPARK,
               ' hot' if act == 'connect' else '',
               rows,
               ' hot' if act == 'connectors' else '',
               thread, icls, itxt, caret,
               modal_html(modal) if modal else ''))


# typed a few characters at a time rather than in three jumps
TYPE_STEPS = [QUERY[:n] for n in range(4, len(QUERY), 4)] + [QUERY]

SEQ = [
    (frame(),                                              800),
    (frame(act='connect'),                                 380),
    (frame(modal='grid'),                                  520),
    (frame(modal='slack'),                                 480),
    (frame(modal='dd'),                                    420),
    (frame(modal='ddopen'),                                620),
    (frame(modal='chosen'),                                480),
    (frame(modal='confirm'),                               400),
    (frame(slack=True),                                    900),
] + [
    (frame(slack=True, typed=t), 70 if i < len(TYPE_STEPS) - 1 else 560)
    for i, t in enumerate(TYPE_STEPS)
] + [
    (frame(slack=True, sent=True, typed=None),             300),
    (frame(slack=True, sent=True, dots=1),                 150),
    (frame(slack=True, sent=True, dots=2),                 150),
    (frame(slack=True, sent=True, dots=3),                 150),
    (frame(slack=True, sent=True, dots=1),                 150),
    (frame(slack=True, sent=True, dots=2),                 150),
    (frame(slack=True, sent=True, dots=3),                 150),
] + [
    (frame(slack=True, sent=True, reply=f), 95)
    for f in (.10,.20,.30,.40,.50,.60,.70,.80,.90)
] + [
    (frame(slack=True, sent=True, reply=1.0),              560),
    (frame(slack=True, sent=True, reply=1.0, cited=True), 2500),
]

CSS = """
*{box-sizing:border-box;margin:0}
body{width:%(GW)spx;background:#e9e9f2;font-family:"The Future",Jost,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;display:grid;
  grid-template-columns:repeat(%(COLS)s,%(W)spx);gap:0}
.f{width:%(W)spx;height:%(H)spx;padding:26px;background:#e9e9f2}
.app{position:relative;height:100%%;background:#fff;border:1px solid #dcdce8;border-radius:8.4px;
  overflow:hidden;box-shadow:0 14px 34px rgba(24,24,37,.10);display:grid;
  grid-template-rows:50px 1fr;grid-template-columns:250px 1fr}
.bar{grid-column:1/-1;display:flex;align-items:center;gap:12px;padding:0 18px;
  border-bottom:1px solid #ececf4;background:#fafaff}
.mark{width:24px;height:24px;border-radius:4.9px;background:#5b4ee9;display:grid;place-items:center;flex:none}
.mark svg{width:14px;height:14px;fill:#fff}
.proj{font-size:17px;font-weight:600;color:#181825}
.src{border-right:1px solid #ececf4;padding:15px 11px;background:#fafaff;
  display:flex;flex-direction:column}
.src h3{font-size:15px;font-weight:600;color:#181825;margin-bottom:12px}
.acts{display:flex;flex-direction:column;gap:6px;margin-bottom:12px}
.add{border:1px solid #dcdce8;border-radius:3.5px;padding:8px;text-align:center;
  font-size:12px;color:#545472;background:#fff}
.add--alt{border-color:#d5d1fb;color:#5b4ee9}
.add--alt.hot{background:#eae8fd;border-color:#5b4ee9}
.conn{margin-top:auto;border-radius:3.5px;padding:9px;text-align:center;
  font-size:12px;font-weight:500;color:#fff;background:#5b4ee9}
.conn.hot{background:#4438c9}
.grp{display:flex;align-items:center;gap:9px;padding:8px 9px;border-radius:4.9px;margin-bottom:6px;
  background:#f6f5ff;box-shadow:inset 0 0 0 1px #e0dcfb}
.grp.fresh{background:#eae8fd;box-shadow:inset 0 0 0 1.5px #5b4ee9}
.ic{width:22px;height:22px;border-radius:4.2px;background:#eae8fd;display:grid;place-items:center;flex:none}
.ic svg{width:13px;height:13px;fill:#5b4ee9}
.tx{min-width:0;display:flex;flex-direction:column}
.nm{font-size:12.5px;font-weight:600;color:#181825;line-height:1.25}
.ct2{font-size:11px;color:#8484a4}
.chk{margin-left:auto;width:15px;height:15px;border-radius:2.8px;border:1.4px solid #b9b2f5;
  display:grid;place-items:center;flex:none}
.chk svg{width:9px;height:9px;fill:none;stroke:#5b4ee9;stroke-width:3}
.chat{display:flex;flex-direction:column;padding:16px 20px;overflow:hidden}
.thread{flex:1;display:flex;flex-direction:column;gap:12px;overflow:hidden}
.who{display:flex;align-items:center;gap:9px;margin-bottom:8px}
.av{width:22px;height:22px;border-radius:4.2px;background:#d5d1fb;flex:none;
  display:grid;place-items:center;font-size:11px;font-weight:600;color:#5b4ee9}
.av--b{background:#181825}
.av--b svg{width:13px;height:13px;fill:#3fffc5}
.nm2{font-size:14px;font-weight:600;color:#181825}
.ask{align-self:flex-end;max-width:76%%;background:#fff;border:1px solid #d5d1fb;
  border-radius:5.9px 5.9px 1.5px 5.9px;padding:13px 16px;box-shadow:0 5px 13px rgba(91,78,233,.06)}
.ask p{font-size:15px;line-height:1.4;color:#181825}
.rep{max-width:94%%;background:#fff;border:1px solid #d5d1fb;
  border-radius:5.9px 5.9px 5.9px 1.5px;padding:14px 16px;box-shadow:0 5px 13px rgba(91,78,233,.06)}
.rep .card{background:transparent;padding:0}
.rep p{font-size:15px;line-height:1.5;color:#181825}
.rep p b{font-weight:600}
.dots{display:flex;gap:6px;padding:6px 4px 2px}
.dots i{width:8px;height:8px;border-radius:50%%;background:#c9c4f7}
.dots i.on{background:#5b4ee9}
.cite{margin-top:10px;padding-top:9px;border-top:1px solid #ececf4;font-size:12.5px;color:#545472}
.cite b{color:#5b4ee9;font-weight:600}
.input{margin-top:14px;border:1px solid #dcdce8;border-radius:7.7px;padding:13px 16px;
  display:flex;align-items:center;gap:14px}
.input p{font-size:15px;line-height:1.4;color:#181825}
.input p.ph{color:#a3a3ba}
.send{width:20px;height:20px;fill:none;stroke:#5b4ee9;stroke-width:1.8;flex:none}
.caret{display:inline-block;width:2px;height:15px;background:#181825;vertical-align:-2px;margin-left:1px}

/* ---- connector modal ---- */
.veil{position:absolute;inset:0;background:rgba(24,24,37,.34);display:grid;place-items:center}
.modal{width:520px;background:#fff;border-radius:8.4px;padding:22px;
  box-shadow:0 24px 60px rgba(24,24,37,.30)}
.modal.pressed{box-shadow:0 12px 30px rgba(24,24,37,.24)}
.modal h4{font-size:17px;font-weight:600;color:#181825;margin-bottom:16px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.ct{border:1px solid #ececf4;border-radius:4.9px;padding:12px 10px;display:flex;
  flex-direction:column;align-items:center;gap:7px}
.ct.on{border-color:#5b4ee9;background:#f6f5ff;box-shadow:inset 0 0 0 1px #5b4ee9}
.cl{width:26px;height:26px;display:grid;place-items:center}
.cl svg{width:24px;height:24px}
.cn{font-size:12px;color:#181825}
.pk{margin-top:16px}
.pkl{display:block;font-size:11.5px;color:#8484a4;margin-bottom:5px}
.sel{border:1px solid #dcdce8;border-radius:4.9px;padding:10px 12px;font-size:13.5px;
  color:#181825;display:flex;align-items:center;justify-content:space-between}
.sel.ph{color:#a3a3ba}
.cv{color:#8484a4;font-size:12px}
.opts{margin-top:5px;background:#fff;border:1px solid #dcdce8;border-radius:4.9px;
  box-shadow:0 8px 20px rgba(24,24,37,.10);padding:4px}
.opt{padding:8px 10px;border-radius:3.5px;font-size:13.5px;color:#181825}
.opt.on{background:#eae8fd;color:#5b4ee9;font-weight:500}
.cta{margin-top:16px;border-radius:4.9px;padding:11px;text-align:center;
  font-size:13.5px;font-weight:500;color:#fff;background:#5b4ee9}
.cta.off{background:#e0dcfb;color:#a9a1ee}
.modal.pressed .cta{background:#4438c9}
""" % {'W': W, 'H': H, 'COLS': COLS, 'GW': W * COLS}

FONTS = """
@font-face{font-family:"The Future";font-weight:400;src:url("https://cdn.prod.website-files.com/5f4d0bcb4cc4d2b9e0b3005d/66d0793c6f7b8627595515dd_the-future-regular.woff2") format("woff2")}
@font-face{font-family:"The Future";font-weight:500;src:url("https://cdn.prod.website-files.com/5f4d0bcb4cc4d2b9e0b3005d/66d0793c8d5fc3a693e0c1f4_the-future-medium.woff2") format("woff2")}
@font-face{font-family:"The Future";font-weight:600 700;src:url("https://cdn.prod.website-files.com/5f4d0bcb4cc4d2b9e0b3005d/66d0793cd205f1234adef23b_the-future-bold.woff2") format("woff2")}
"""

html = ('<meta charset="utf-8"><style>%s%s</style>%s'
        % (FONTS, CSS, ''.join(f for f, _ in SEQ)))
here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, 'session.html'), 'w', encoding='utf-8').write(html)
open(os.path.join(here, 'session.durations'), 'w').write(','.join(str(d) for _, d in SEQ))
rows = -(-len(SEQ) // COLS)
open(os.path.join(here, 'session.grid'), 'w').write('%d,%d,%d,%d,%d' % (W, H, COLS, rows, len(SEQ)))
print('frames: %d | grid %dx%d = %dx%d px | run: %.1fs'
      % (len(SEQ), COLS, rows, W * COLS, H * rows, sum(d for _, d in SEQ) / 1000))
