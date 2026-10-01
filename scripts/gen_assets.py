#!/usr/bin/env python3
"""Generate profile SVG assets (banner + 2 architecture diagrams) in dark and light themes.

Only facts already public in the profile README are drawn. Run: python3 scripts/gen_assets.py (writes assets/*.svg, prints contrast check)
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0D1117", card="#161B22", border="#30363D", fg="#F0F6FC", muted="#9198A1",
                 accent="#3FB6E0", accent2="#F0A040", line="#6E7681"),
    "light": dict(bg="#FFFFFF", card="#F6F8FA", border="#D1D9E0", fg="#1F2328", muted="#59636E",
                  accent="#0A6E8F", accent2="#A3530A", line="#818B98"),
}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def banner(t: dict) -> str:
    stats = [("1.6M+", "metered customers"), ("5+ yrs", "shipping to production"),
             ("s → ms", "search latency"), ("50", "EV pilot fleet")]
    tiles = []
    x0, y, w, h, gap = 40, 190, 215, 84, 20
    for i, (num, label) in enumerate(stats):
        x = x0 + i * (w + gap)
        tiles.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<text x="{x+18}" y="{y+40}" font-family="{FONT}" font-size="30" font-weight="700" fill="{t["accent"]}">{esc(num)}</text>'
            f'<text x="{x+18}" y="{y+66}" font-family="{FONT}" font-size="16" fill="{t["muted"]}">{esc(label)}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300" role="img" aria-labelledby="t d">
<title id="t">Đỗ Quốc Hoàng, Senior Backend Engineer</title>
<desc id="d">Java, Go, distributed systems. 1.6M+ metered customers, 5+ years in production, search latency from seconds to milliseconds, 50-vehicle EV pilot.</desc>
<rect width="1000" height="300" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>
<rect x="40" y="44" width="6" height="104" rx="3" fill="{t["accent"]}"/>
<text x="66" y="92" font-family="{FONT}" font-size="46" font-weight="700" fill="{t["fg"]}">Đỗ Quốc Hoàng</text>
<text x="66" y="132" font-family="{FONT}" font-size="22" fill="{t["fg"]}">Senior Backend Engineer · Java · Go · Distributed Systems</text>
<text x="960" y="70" text-anchor="end" font-family="{MONO}" font-size="15" fill="{t["muted"]}">Ho Chi Minh City · UTC+7</text>
<text x="960" y="96" text-anchor="end" font-family="{MONO}" font-size="15" fill="{t["accent2"]}">● open to remote &amp; freelance</text>
{"".join(tiles)}
</svg>
'''


def box(t, x, y, w, h, title, sub="", strong=False):
    stroke = t["accent"] if strong else t["border"]
    sw = 2 if strong else 1
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["card"]}" stroke="{stroke}" stroke-width="{sw}"/>'
         f'<text x="{x+w/2}" y="{y+(h/2 - (8 if sub else -6))}" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="600" fill="{t["fg"]}">{esc(title)}</text>')
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{esc(sub)}</text>'
    return s


def arrow(t, x1, y1, x2, y2, label="", place="above"):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["line"]}" stroke-width="2" marker-end="url(#a)"/>'
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if place == "above":  # horizontal arrow: centered above the line
            x, y, anchor = mx, my - 8, "middle"
        elif place == "wedge-up":  # rising diagonal: label in the gap below it
            x, y, anchor = x1 + 52, my + 16, "start"
        else:  # "wedge-down": falling diagonal, label in the gap above it
            x, y, anchor = x1 + 52, my - 12, "start"
        s += f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(label)}</text>'
    return s


def frame(t, title, desc, body, h=260):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc)}</desc>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{t["line"]}"/></marker></defs>
<rect width="1000" height="{h}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>
{body}
</svg>
'''


def billing(t):
    b = []
    b.append(box(t, 30, 95, 190, 70, "Utility subsidiaries", "multiple tenants"))
    b.append(arrow(t, 220, 130, 290, 130))
    b.append(box(t, 290, 85, 230, 90, "Billing core", "multi-tenant · Java", strong=True))
    b.append(arrow(t, 520, 130, 590, 130, "events"))
    b.append(box(t, 590, 95, 150, 70, "Kafka", "event pipelines"))
    b.append(arrow(t, 740, 130, 800, 70))
    b.append(box(t, 800, 30, 170, 76, "Elasticsearch", "search: s → ms"))
    b.append(arrow(t, 740, 130, 800, 190))
    b.append(box(t, 800, 154, 170, 76, "Fintech gateway", "VietQR · JWE/JWS"))
    b.append(f'<text x="30" y="40" font-family="{FONT}" font-size="15" font-weight="600" fill="{t["accent"]}">1.6M+ metered customers</text>')
    return frame(t, "Multi-tenant water-utility billing architecture",
                 "Utility subsidiaries feed a multi-tenant billing core, which publishes events to Kafka pipelines that feed an Elasticsearch search layer and a secure VietQR payment gateway.",
                 "".join(b))


def fleet(t):
    b = []
    b.append(box(t, 30, 95, 170, 70, "EV fleet", "IoT devices"))
    b.append(arrow(t, 200, 130, 270, 130, "MQTT"))
    b.append(box(t, 270, 95, 150, 70, "EMQX", "broker"))
    b.append(arrow(t, 420, 130, 480, 130))
    b.append(box(t, 480, 85, 220, 90, "Go / Gin backend", "feature-based clean arch", strong=True))
    b.append(arrow(t, 700, 130, 790, 70, "WebSocket", "wedge-up"))
    b.append(box(t, 790, 30, 180, 76, "Ops dashboards", "React · Vue"))
    b.append(arrow(t, 700, 130, 790, 190, "REST", "wedge-down"))
    b.append(box(t, 790, 154, 180, 76, "Rider app", "Flutter"))
    b.append(f'<text x="30" y="40" font-family="{FONT}" font-size="15" font-weight="600" fill="{t["accent"]}">Real-time tracking · 50-vehicle pilot</text>')
    return frame(t, "EV-rental CRM and IoT fleet platform architecture",
                 "EV fleet devices publish over MQTT to an EMQX broker consumed by a Go Gin backend, which streams live vehicle state to React and Vue dashboards over WebSockets and serves a Flutter app.",
                 "".join(b))


for name, t in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(banner(t), encoding="utf-8")
    (OUT / f"billing-{name}.svg").write_text(billing(t), encoding="utf-8")
    (OUT / f"fleet-{name}.svg").write_text(fleet(t), encoding="utf-8")
print("written:", sorted(p.name for p in OUT.iterdir()))


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def cr(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)


worst = 99
for name, t in THEMES.items():
    for fgk in ("fg", "muted", "accent", "accent2"):
        for bgk in ("bg", "card"):
            r = cr(t[fgk], t[bgk])
            worst = min(worst, r)
            print(f"{name:5} {fgk:7} on {bgk:4}: {r:5.2f}:1 {'OK' if r >= 4.5 else 'FAIL'}")
print(f"worst contrast: {worst:.2f}:1")
