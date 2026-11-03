#!/usr/bin/env python3
"""Generates pure SVG + SMIL assets for the ARCAENUX profile README.
BIOS Setup Utility theme — no JS, no CSS, no external fonts.
Run:  python3 build_assets.py   ->  ./assets/*.svg
Edit the CONFIG block, rerun, commit."""
import os
import random

# ---------------- CONFIG ----------------
NAME = "ARCAENUX"
SUB = "COMPUTER SCIENCE  \u2022  SOFTWARE  \u2022  SYSTEMS  \u2022  AI"
PROMPT = "> think deep. build bold. understand more."
HOST = "joseph@arcaenux: ~"
BOOT = [  # (kind, text)  kind: cmd | out | ok
    ("cmd", "whoami"),
    ("out", "joseph boafo afful  //  arcaenux"),
    ("cmd", "cat education.txt"),
    ("out", "bsc computer science @ knust  \u00b7  ghana"),
    ("cmd", "cat focus.txt"),
    ("out", "software engineering \u00b7 algorithms \u00b7 ai \u00b7 backend systems"),
    ("cmd", "./loop.sh"),
    ("out", "learn \u2192 build \u2192 break \u2192 investigate \u2192 rebuild"),
    ("cmd", "status"),
    ("ok", "building in public"),
]
LAYERS = [  # (tag, label, chips)
    ("L7", "APPLICATION", ["react", "next.js", "django", "vite"]),
    ("L6", "LANGUAGES", ["java", "python", "c++", "typescript", "javascript"]),
    ("L5", "DATA", ["mongodb", "postgresql", "sqlite"]),
    ("L4", "RUNTIME / INFRA", ["node.js", "express", "vercel"]),
    ("L3", "OS & TOOLING", ["linux", "git", "github", "vscode"]),
]
BIOS_MENU = [" MAIN ", " ADVANCED ", " BOOT ", " SECURITY ", " EXIT "]
BIOS_VER = "2.06"
# ----------------------------------------

BG, RED, GRAY, DIM, OK, WHITE = "#0B0B0C", "#FF2438", "#8A8A8E", "#1B1B1E", "#3DD68C", "#FFFFFF"
FONT = "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)
random.seed(7)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(HEAD + svg)
    print("wrote", name)


# ---------------------------------------------------------------- HERO
def hero():
    W, H = 900, 280
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}">']
    p.append(f'''<defs>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="{DIM}" stroke-width="1"/></pattern>
<radialGradient id="glow" cx="82%" cy="50%" r="55%"><stop offset="0" stop-color="{RED}" stop-opacity=".38"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset=".5" stop-color="{RED}" stop-opacity=".22"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
</defs>''')
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#grid)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>')
    for i in range(20):
        x = 18 + i * 45 + random.randint(-6, 6)
        dur = random.uniform(7, 13)
        begin = -random.uniform(0, 12)
        tsp = "".join(
            f'<tspan x="{x}" dy="{0 if k == 0 else 14}">{random.choice("01")}</tspan>' for k in range(10)
        )
        p.append(
            f'<g opacity=".16"><text font-family="{FONT}" font-size="12" fill="{RED if i % 5 == 0 else GRAY}">{tsp}'
            f'<animateTransform attributeName="transform" type="translate" from="0 -150" to="0 {H + 20}" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></text></g>'
        )
    nodes = [(560, 70), (640, 150), (720, 60), (790, 140), (860, 80), (700, 225), (600, 235), (830, 235), (520, 165)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (5, 3), (6, 1), (8, 0), (8, 6), (5, 7), (3, 7), (0, 2)]
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        p.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED}" stroke-opacity=".45" stroke-width="1" stroke-dasharray="4 6">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1.4s" repeatCount="indefinite"/></line>'
        )
    for i, (x, y) in enumerate(nodes):
        b = f"{random.uniform(0, 2):.1f}s"
        p.append(
            f'<circle cx="{x}" cy="{y}" r="4" fill="none" stroke="{RED}"><animate attributeName="r" values="4;16" dur="2.4s" begin="{b}" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values=".8;0" dur="2.4s" begin="{b}" repeatCount="indefinite"/></circle>'
            f'<circle cx="{x}" cy="{y}" r="4" fill="{RED}"/>'
        )
    p.append(
        f'<text x="52" y="142" font-family="{FONT}" font-size="76" font-weight="800" letter-spacing="6" fill="{RED}" opacity=".55">{NAME}'
        f'<animate attributeName="x" values="52;52;46;58;52;52" keyTimes="0;.9;.92;.94;.96;1" dur="5s" repeatCount="indefinite"/></text>'
        f'<text x="50" y="140" font-family="{FONT}" font-size="76" font-weight="800" letter-spacing="6" fill="{WHITE}">{NAME}</text>'
    )
    p.append(f'<text x="52" y="182" font-family="{FONT}" font-size="15" letter-spacing="4" fill="{GRAY}" xml:space="preserve">{esc(SUB)}</text>')
    p.append(f'<text x="52" y="232" font-family="{FONT}" font-size="16" fill="{RED}">{esc(PROMPT)}</text>')
    cx = 52 + len(PROMPT) * 9.6 + 4
    p.append(
        f'<rect x="{cx:.0f}" y="219" width="9" height="16" fill="{RED}"><animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" calcMode="discrete" dur="1s" repeatCount="indefinite"/></rect>'
    )
    p.append(
        f'<rect x="0" y="-40" width="{W}" height="40" fill="url(#scan)"><animate attributeName="y" from="-40" to="{H}" dur="4.5s" repeatCount="indefinite"/></rect>'
    )
    p.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" fill="none" stroke="#2A0B0D"/></svg>')
    save("hero.svg", "".join(p))


# ---------------------------------------------------------------- BOOT TERMINAL
def boot():
    W, LH, TOP, T = 900, 28, 84, 17.0
    H = TOP + LH * (len(BOOT) + 1) + 24
    CW = 9.9
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="terminal">']
    p.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="#2A0B0D"/>')
    p.append(f'<rect width="{W}" height="36" rx="10" fill="#141416"/><rect y="26" width="{W}" height="10" fill="#141416"/>')
    for i, c in enumerate([RED, "#F5A524", OK]):
        p.append(f'<circle cx="{24 + i * 20}" cy="18" r="6" fill="{c}"/>')
    p.append(f'<text x="{W // 2}" y="23" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{GRAY}">{HOST}</text>')
    clips, lines = [], []
    s = 0.6
    for i, (kind, text) in enumerate(BOOT):
        y = TOP + i * LH
        prefix = "$ " if kind == "cmd" else ("[ OK ] " if kind == "ok" else "")
        full = prefix + text
        n = len(full)
        d = min(1.4, max(0.5, n * 0.045)) if kind == "cmd" else 0.5
        times = [0, s / T] + [(s + d * k / n) / T for k in range(1, n + 1)] + [0.97, 1]
        widths = [0, 0] + [round(CW * k, 1) for k in range(1, n + 1)] + [0, 0]
        kt = ";".join(f"{t:.4f}" for t in times)
        vs = ";".join(str(w) for w in widths)
        clips.append(
            f'<clipPath id="c{i}"><rect x="30" y="{y - 20}" height="26" width="0">'
            f'<animate attributeName="width" values="{vs}" keyTimes="{kt}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>'
        )
        if kind == "cmd":
            body = f'<tspan fill="{RED}">$ </tspan><tspan fill="{WHITE}">{esc(text)}</tspan>'
        elif kind == "ok":
            body = f'<tspan fill="{OK}">[ OK ] </tspan><tspan fill="{WHITE}">{esc(text)}</tspan>'
        else:
            body = f'<tspan fill="{GRAY}">{esc(text)}</tspan>'
        lines.append(
            f'<text clip-path="url(#c{i})" x="30" y="{y}" font-family="{FONT}" font-size="15.5" xml:space="preserve">{body}</text>'
        )
        s += d + 0.9
    yl = TOP + len(BOOT) * LH
    fa = s / T
    p.append("<defs>" + "".join(clips) + "</defs>")
    p.extend(lines)
    p.append(
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{fa:.4f};{fa + 0.001:.4f};0.97;0.971;1" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>'
        f'<text x="30" y="{yl}" font-family="{FONT}" font-size="15.5" fill="{RED}">$ </text>'
        f'<rect x="{30 + 2 * CW:.0f}" y="{yl - 14}" width="9" height="17" fill="{RED}"><animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" calcMode="discrete" dur="1s" repeatCount="indefinite"/></rect></g>'
    )
    p.append("</svg>")
    save("boot.svg", "".join(p))


# ---------------------------------------------------------------- STACK LAYERS
def layers():
    W, X0, BH, GAP, TOP = 900, 70, 54, 12, 56
    H = TOP + len(LAYERS) * (BH + GAP) + 10
    PX = 30
    DUR = 6
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="stack by layer">']
    p.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="#2A0B0D"/>')
    p.append(f'<text x="30" y="32" font-family="{FONT}" font-size="13" letter-spacing="2" fill="{RED}">// THE STACK \u2014 LAYER BY LAYER</text>')
    y0, y1 = TOP - 8, H - 14
    p.append(f'<line x1="{PX}" y1="{y0}" x2="{PX}" y2="{y1}" stroke="{GRAY}" stroke-opacity=".5" stroke-dasharray="3 5"/>')
    for i, (tag, label, chips) in enumerate(LAYERS):
        y = TOP + i * (BH + GAP)
        cy = y + BH / 2
        f = (cy - y0) / (y1 - y0)
        k0, k1, k2 = max(f - 0.07, 0.001), f, min(f + 0.09, 0.999)
        p.append(
            f'<rect x="{X0}" y="{y}" width="{W - X0 - 30}" height="{BH}" rx="8" fill="#101012" stroke="{RED}" stroke-opacity=".25">'
            f'<animate attributeName="stroke-opacity" values=".25;.25;1;.25;.25" keyTimes="0;{k0:.3f};{k1:.3f};{k2:.3f};1" dur="{DUR}s" repeatCount="indefinite"/></rect>'
        )
        p.append(f'<text x="{X0 + 16}" y="{cy - 3:.0f}" font-family="{FONT}" font-size="13" font-weight="700" fill="{RED}">{tag}</text>')
        p.append(f'<text x="{X0 + 16}" y="{cy + 14:.0f}" font-family="{FONT}" font-size="11" letter-spacing="1" fill="{GRAY}">{esc(label)}</text>')
        x = X0 + 200
        for c in chips:
            w = int(len(c) * 8.6 + 22)
            p.append(
                f'<rect x="{x}" y="{cy - 14:.0f}" width="{w}" height="28" rx="6" fill="#18181B" stroke="#2C2C31"/>'
                f'<text x="{x + w / 2:.0f}" y="{cy + 5:.0f}" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{WHITE}">{esc(c)}</text>'
            )
            x += w + 10
    p.append(
        f'<circle r="6" fill="{RED}"><animateMotion dur="{DUR}s" repeatCount="indefinite" path="M{PX} {y0} V{y1}"/></circle>'
        f'<circle r="6" fill="none" stroke="{RED}"><animateMotion dur="{DUR}s" repeatCount="indefinite" path="M{PX} {y0} V{y1}"/>'
        f'<animate attributeName="r" values="6;16" dur="0.9s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".9;0" dur="0.9s" repeatCount="indefinite"/></circle>'
    )
    p.append("</svg>")
    save("layers.svg", "".join(p))


# ---------------------------------------------------------------- DIVIDER
def divider():
    W, H = 900, 20
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation">']
    p.append(
        f'<defs><linearGradient id="p"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset=".5" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient></defs>'
    )
    p.append(f'<line x1="0" y1="10" x2="{W}" y2="10" stroke="#2A2A2E"/>')
    for x in range(30, W, 90):
        p.append(f'<rect x="{x - 3}" y="7" width="6" height="6" fill="{BG}" stroke="#3A3A40"/>')
    p.append(
        f'<rect y="9" width="140" height="2" fill="url(#p)"><animate attributeName="x" from="-140" to="{W}" dur="3.5s" repeatCount="indefinite"/></rect></svg>'
    )
    save("divider.svg", "".join(p))


# ---------------------------------------------------------------- BIOS HEADER
def bios_header():
    """BIOS setup utility header: title bar + menu bar."""
    W, H = 900, 108
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="ARCAENUX BIOS Setup Utility v{BIOS_VER}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(f'<rect y="0" width="{W}" height="2" fill="{RED}"/>')
    p.append(f'<rect y="{H - 2}" width="{W}" height="2" fill="{RED}"/>')
    # Title
    p.append(f'<text x="30" y="30" font-family="{FONT}" font-size="15" font-weight="700" letter-spacing="1" fill="{WHITE}">ARCAENUX BIOS SETUP UTILITY</text>')
    p.append(f'<text x="30" y="48" font-family="{FONT}" font-size="10.5" fill="{GRAY}">(C) 2026 ARCAENUX  \u00b7  JOSEPH BOAFO AFFUL  \u00b7  KNUST, GHANA  \u00b7  v{BIOS_VER}</text>')
    # Menu bar
    my = 78
    x = 30
    for i, item in enumerate(BIOS_MENU):
        active = (i == 0)
        fill = RED if active else "#121216"
        tcol = WHITE if active else GRAY
        wdt = len(item) * 8.4 + 10
        p.append(f'<rect x="{x}" y="{my - 13}" width="{wdt}" height="18" rx="2" fill="{fill}"/>')
        p.append(f'<text x="{x + 6}" y="{my + 2}" font-family="{FONT}" font-size="12" font-weight="700" fill="{tcol}">{item}</text>')
        x += wdt + 8
    # Key hints
    p.append(f'<text x="{W - 30}" y="{H - 8}" text-anchor="end" font-family="{FONT}" font-size="10" fill="#5A5A60">[\u2191\u2193] Navigate   [Enter] Select   [Esc] Exit   [F1] Help</text>')
    p.append("</svg>")
    save("bios-header.svg", "".join(p))


# ---------------------------------------------------------------- BIOS KEYBAR
def bios_keybar():
    """Bottom BIOS key hint bar."""
    W, H = 900, 26
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(f'<rect y="0" width="{W}" height="1" fill="#2A2A2E"/>')
    p.append(f'<text x="30" y="18" font-family="{FONT}" font-size="10" fill="#5A5A60">[Tab] Switch panel   [Enter] Open   [Esc] Back   [F10] Save &amp; Exit</text>')
    p.append(f'<text x="{W - 30}" y="18" text-anchor="end" font-family="{FONT}" font-size="10" fill="#5A5A60">ARCAENUX v{BIOS_VER}</text>')
    p.append("</svg>")
    save("bios-keybar.svg", "".join(p))


# ---------------------------------------------------------------- CURSOR
def cursor():
    """Blinking block cursor."""
    W, H = 16, 20
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="cursor">']
    p.append(f'<rect width="{W}" height="{H}" fill="{RED}"><animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" calcMode="discrete" dur="1s" repeatCount="indefinite"/></rect>')
    p.append("</svg>")
    save("cursor.svg", "".join(p))


# ---------------------------------------------------------------- FOOTER
def footer():
    W, H = 900, 150
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="ARCAENUX footer">']
    p.append(f'''<defs>
<pattern id="fgrid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="{DIM}" stroke-width="1"/></pattern>
<radialGradient id="fglow" cx="50%" cy="115%" r="70%"><stop offset="0" stop-color="{RED}" stop-opacity=".30"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<linearGradient id="fline" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset=".5" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
</defs>''')
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#fgrid)" opacity=".55"/><rect width="{W}" height="{H}" fill="url(#fglow)"/>')
    p.append(f'<rect y="0" width="{W}" height="1" fill="url(#fline)"/>')
    p.append(f'<text x="{W / 2}" y="64" text-anchor="middle" font-family="{FONT}" font-size="27" font-weight="700" letter-spacing="5" fill="{WHITE}">THINK BEYOND THE OBVIOUS.</text>')
    p.append(f'<text x="{W / 2}" y="94" text-anchor="middle" font-family="{FONT}" font-size="12" letter-spacing="4" fill="{GRAY}">LEARN IT  \u00b7  BUILD IT  \u00b7  UNDERSTAND IT</text>')
    p.append(
        f'<text x="{W / 2}" y="126" text-anchor="middle" font-family="{FONT}" font-size="10" letter-spacing="3" fill="#5A5A60">\u00a9 2026 ARCAENUX'
        f'<tspan fill="{RED}">_<animate attributeName="opacity" values="1;0" keyTimes="0;.5" calcMode="discrete" dur="1.1s" repeatCount="indefinite"/></tspan></text>'
    )
    p.append("</svg>")
    save("footer.svg", "".join(p))


if __name__ == "__main__":
    hero()
    boot()
    layers()
    divider()
    bios_header()
    bios_keybar()
    cursor()
    footer()
