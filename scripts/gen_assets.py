#!/usr/bin/env python3
"""Generate the profile terminal hero (desktop + mobile SVG).

Only facts already public on the profile are drawn. Run: python3 scripts/gen_assets.py
(writes assets/terminal*.svg, prints a contrast check).

The terminal is always dark: it reads as a terminal window on both GitHub themes, so one file per size.
Typing uses SMIL (runs inside <img>, scripts do not). Every animated element keeps its finished state as
the base value, so renderers without SMIL show the complete terminal. Animation plays once, then freezes.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

T = dict(win="#0D1117", bar="#161B22", border="#3D444D", fg="#E6EDF3", muted="#9198A1",
         green="#3FB950", orange="#F0A040", cyan="#3FB6E0")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
TITLE = "Đỗ Quốc Hoàng, Senior Backend Engineer"
DESC = ("Terminal: Đỗ Quốc Hoàng, Senior Backend Engineer, Java and Go. 1.6M+ metered customers on a multi-tenant "
        "billing core. Search latency from seconds to milliseconds with Kafka and Elasticsearch. 50-vehicle EV pilot "
        "with real-time IoT tracking in Go. 5+ years shipping to production. Open to remote and freelance backend roles.")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def terminal(lines, w, fs, lh, prompt, pad=24, step=0.06, pause=0.35, gap=0.12, start=0.5):
    """lines: ("cmd", text) typed after the prompt, or ("out", [(text, color, bold), ...]) printed at once."""
    cw, bar_h = fs * 0.6, 36
    top = bar_h + lh + 2
    h = top + lh * (len(lines) - 1) + 18
    t, sched = start, []
    for kind, body in lines:
        if kind == "cmd":
            sched.append((t, t + step * len(body)))
            t += step * len(body) + pause
        else:
            sched.append((t, t))
            t += gap
    total = t
    kt = lambda x: f"{x / total:.4f}"
    anim = f'calcMode="discrete" dur="{total:.2f}s" fill="freeze"'
    out = []
    for i, ((kind, body), (t0, t1)) in enumerate(zip(lines, sched)):
        y = top + i * lh
        base = f'x="{pad}" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve"'
        if kind == "cmd":
            pw = pad + (len(prompt) + 1) * cw
            vals = [0] + [pw + k * cw for k in range(len(body) + 1)] + [w]
            keys = [0] + [t0 + k * step for k in range(len(body) + 1)] + [t1 + 0.01]
            out.append(
                f'<clipPath id="c{i}"><rect x="0" y="{y - lh + 4}" width="{w}" height="{lh + 4}">'
                f'<animate attributeName="width" values="{";".join(f"{v:.1f}" for v in vals)}" '
                f'keyTimes="{";".join(kt(k) for k in keys)}" {anim}/></rect></clipPath>'
                f'<text {base} clip-path="url(#c{i})"><tspan fill="{T["green"]}" font-weight="700">{esc(prompt)}</tspan>'
                f' <tspan fill="{T["fg"]}">{esc(body)}</tspan></text>')
        else:
            spans = "".join(f'<tspan fill="{T[c]}"' + (' font-weight="700"' if b else "") + f'>{esc(s)}</tspan>'
                            for s, c, b in body)
            out.append(f'<text {base}><animate attributeName="opacity" values="0;1" keyTimes="0;{kt(t0)}" {anim}/>'
                       f'{spans}</text>')
    cy = top + (len(lines) - 1) * lh
    cx = pad + (len(prompt) + 1) * cw
    cursor = (f'<rect x="{cx:.1f}" y="{cy - fs + 2}" width="{cw:.1f}" height="{fs + 3}" fill="{T["fg"]}">'
              f'<set attributeName="opacity" to="0" begin="0s" dur="{total:.2f}s"/>'
              f'<animate attributeName="opacity" values="1;0" dur="1.1s" calcMode="discrete" '
              f'begin="{total:.2f}s" repeatCount="indefinite"/></rect>')
    dots = "".join(f'<circle cx="{20 + k * 20}" cy="{bar_h / 2}" r="6" fill="{c}"/>'
                   for k, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(TITLE)}</title>
<desc id="d">{esc(DESC)}</desc>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{T["win"]}" stroke="{T["border"]}"/>
<path d="M1 {bar_h}V13A12 12 0 0 1 13 1H{w - 13}A12 12 0 0 1 {w - 1} 13V{bar_h}Z" fill="{T["bar"]}"/>
<line x1="1" y1="{bar_h + 0.5}" x2="{w - 1}" y2="{bar_h + 0.5}" stroke="{T["border"]}"/>
{dots}
<text x="{w / 2}" y="{bar_h / 2 + 5}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{T["muted"]}">hoang@hcmc: ~</text>
{"".join(out)}
{cursor}
</svg>
'''


def ok(tag, num, rest):
    seg = [("[", "muted", False), ("OK", "green", True), ("] ", "muted", False)]
    if tag:
        seg.append((tag, "cyan", False))
    return ("out", seg + [(num, "orange", True), (rest, "fg", False)])


DESKTOP = [
    ("cmd", "whoami"),
    ("out", [("Đỗ Quốc Hoàng", "fg", True), ("  Senior Backend Engineer · Java · Go · distributed systems", "muted", False)]),
    ("cmd", "cat impact.log"),
    ok("billing  ", "1.6M+", " metered customers on a multi-tenant billing core"),
    ok("search   ", "seconds → ms", " search latency with Kafka + Elasticsearch"),
    ok("fleet    ", "50", "-vehicle EV pilot, real-time IoT tracking in Go"),
    ok("prod     ", "5+", " years shipping systems to production"),
    ("cmd", "echo $STATUS"),
    ("out", [("● ", "orange", False), ("open to remote & freelance backend roles", "fg", False),
             ("  Ho Chi Minh City, UTC+7", "muted", False)]),
    ("cmd", ""),
]

# Mobile: 400 units wide, GitHub scales it to ~358px on a 390px phone, so 13-unit text renders at ~11.6px.
MOBILE = [
    ("cmd", "whoami"),
    ("out", [("Đỗ Quốc Hoàng", "fg", True)]),
    ("out", [("Senior Backend Engineer · Java · Go", "muted", False)]),
    ("cmd", "cat impact.log"),
    ok("", "1.6M+", " metered customers, billing"),
    ok("", "s → ms", " search latency, Kafka + ES"),
    ok("", "50", "-vehicle EV pilot, IoT in Go"),
    ok("", "5+", " years in production"),
    ("cmd", "echo $STATUS"),
    ("out", [("● ", "orange", False), ("open to remote & freelance", "fg", False)]),
    ("cmd", ""),
]

(OUT / "terminal.svg").write_text(terminal(DESKTOP, 1000, 18, 30, "hoang@hcmc:~$"), encoding="utf-8")
(OUT / "terminal-mobile.svg").write_text(terminal(MOBILE, 400, 13, 22, "~$", pad=16), encoding="utf-8")
print("written:", sorted(p.name for p in OUT.iterdir()))


def lum(hx):
    c = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def cr(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)


worst = min(cr(T[k], T["win"]) for k in ("fg", "muted", "green", "orange", "cyan"))
for k in ("fg", "muted", "green", "orange", "cyan"):
    print(f"{k:6} on win: {cr(T[k], T['win']):5.2f}:1")
print(f"worst contrast: {worst:.2f}:1 {'OK' if worst >= 4.5 else 'FAIL'}")
