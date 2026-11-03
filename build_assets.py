#!/usr/bin/env python3
"""ARCAENUX / SIGNAL — generative profile assets built from real GitHub activity.

Reads:
  data/contributions.json  367 days of contribution counts
  data/repos.json          repo + language metadata

Writes:
  assets/signal.svg        hero: a year in bloom (phyllotaxis of daily commits)
  assets/pulse.svg         daily contribution seismograph
  assets/spectrum.svg      language spectrum by bytes
  assets/layers.svg        the stack, layer by layer
  assets/divider.svg       signal rule
  assets/footer.svg        closing plate

Run:  python build_assets.py
"""
import datetime
import json
import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- palette
BG    = "#070709"
INK   = "#0E0E12"
RED   = "#FF2438"
EMBER = "#FF6B4A"
HOT   = "#FFD9D0"
BONE  = "#F4F0E8"
ASH   = "#8A8A8E"
DIM   = "#5A5A60"
FAINT = "#2A2A30"
LINE  = "#222228"

MONO  = "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SERIF = "Georgia, 'Times New Roman', serif"

NAME = "ARCAENUX"
TAGLINE = "A YEAR IN COMMITS"

# ---------------------------------------------------------------- data
with open(os.path.join(ROOT, "data", "contributions.json"), encoding="utf-8") as fh:
    CONTRIB = json.load(fh)
DAYS = CONTRIB["days"]
COUNTS = [d["count"] for d in DAYS]
N = len(DAYS)
TOTAL = CONTRIB["total"]
PEAK = max(COUNTS)
START = CONTRIB["start"]
END = CONTRIB["end"]

with open(os.path.join(ROOT, "data", "repos.json"), encoding="utf-8") as fh:
    REPOS = json.load(fh)


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, text, size, fill, weight="400", ls="0", anchor="start", family=MONO):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" letter-spacing="{ls}" fill="{fill}" '
        f'text-anchor="{anchor}">{esc(text)}</text>'
    )


def color_for(count):
    if count == 0:
        return "#2A1014", 0.55
    if count <= 2:
        return "#7A1622", 0.85
    if count <= 5:
        return RED, 0.92
    if count <= 9:
        return EMBER, 0.95
    return HOT, 1.0


def save(name, body):
    svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + body
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote {name:16s} {len(svg):>7,} bytes")


# ---------------------------------------------------------------- hero
def signal():
    W, H = 900, 600
    cx, cy, R = 300, 300, 238
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="{NAME} — {TAGLINE}: a generative bloom of {N} days and {TOTAL} contributions">'
    ]
    p.append(
        f'<defs>'
        f'<radialGradient id="glow" cx="33%" cy="50%" r="58%">'
        f'<stop offset="0" stop-color="{RED}" stop-opacity=".17"/>'
        f'<stop offset=".55" stop-color="{RED}" stop-opacity=".04"/>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="vig" cx="50%" cy="50%" r="72%">'
        f'<stop offset=".55" stop-color="#000" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient>'
        f'<radialGradient id="coreglow" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0" stop-color="{HOT}" stop-opacity=".9"/>'
        f'<stop offset=".4" stop-color="{RED}" stop-opacity=".5"/>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>'
        f'</defs>'
    )
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    grid = []
    for x in range(0, W + 1, 36):
        grid.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
    for y in range(0, H + 1, 36):
        grid.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    p.append(f'<g stroke="#FFFFFF" stroke-opacity=".022" stroke-width="1">{"".join(grid)}</g>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')

    for d in (
        "M24 40 V24 H40",
        "M876 24 V40 M876 24 H860",
        "M24 560 V576 H40",
        "M876 576 V560 M876 576 H860",
    ):
        p.append(f'<path d="{d}" fill="none" stroke="{FAINT}" stroke-width="1"/>')

    p.append(txt(30, 30, f"{NAME} / SIGNAL", 9, ASH, "700", "3"))
    p.append(txt(30, 45, f"ISSUE 001  ·  {START[:4]}—{END[:4]}", 8, DIM, "400", "2"))

    bloom = [
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="180s" repeatCount="indefinite"/>'
    ]

    seen_months = set()
    for i, day in enumerate(DAYS):
        key = day["date"][:7]
        if key in seen_months:
            continue
        seen_months.add(key)
        rr = 16 + R * math.sqrt(i / (N - 1))
        bloom.append(
            f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" '
            f'stroke="#FFFFFF" stroke-opacity=".035" stroke-width=".8"/>'
        )

    for arm in range(3):
        pts = []
        for j in range(151):
            angle = (j / 150) * 4 * math.pi + arm * 2 * math.pi / 3
            rr = 16 + R * (j / 150)
            pts.append(f"{cx + rr * math.cos(angle):.1f},{cy + rr * math.sin(angle):.1f}")
        bloom.append(
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="{RED}" '
            f'stroke-opacity=".045" stroke-width="1"/>'
        )

    top_days = set(sorted(range(N), key=lambda i: COUNTS[i], reverse=True)[:8])
    for i, day in enumerate(DAYS):
        count = day["count"]
        t = i / (N - 1)
        angle = i * math.radians(137.507764) - math.pi / 2
        rr = 16 + R * math.sqrt(t)
        x = cx + rr * math.cos(angle)
        y = cy + rr * math.sin(angle)
        size = 1.2 + min(count, 20) * 0.22
        fill, opacity = color_for(count)
        if count >= 5:
            bloom.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size * 2.6:.1f}" '
                f'fill="{RED}" opacity="{0.05 + min(count, 20) / 20 * 0.09:.2f}"/>'
            )
        bloom.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size:.1f}" fill="{fill}" opacity="{opacity}"/>'
        )
        if i in top_days:
            bloom.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size + 5:.1f}" fill="none" '
                f'stroke="{HOT}" stroke-opacity=".35" stroke-width=".8">'
                f'<animate attributeName="r" values="{size + 4:.1f};{size + 11:.1f}" '
                f'dur="2.8s" repeatCount="indefinite"/>'
                f'<animate attributeName="stroke-opacity" values=".45;0" '
                f'dur="2.8s" repeatCount="indefinite"/></circle>'
            )

    bloom.append(
        f'<circle cx="{cx}" cy="{cy}" r="252" fill="none" stroke="{RED}" '
        f'stroke-opacity=".16" stroke-width="1" stroke-dasharray="1 7"/>'
    )
    bloom.append(
        f'<circle cx="{cx}" cy="{cy}" r="260" fill="none" stroke="{RED}" '
        f'stroke-opacity=".35" stroke-width="1.6" stroke-dasharray="40 1230">'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    for k in range(24):
        angle = k * math.pi / 12
        is_long = k % 2 == 0
        r1, r2 = 256, (264 if is_long else 261)
        bloom.append(
            f'<line x1="{cx + r1 * math.cos(angle):.1f}" y1="{cy + r1 * math.sin(angle):.1f}" '
            f'x2="{cx + r2 * math.cos(angle):.1f}" y2="{cy + r2 * math.sin(angle):.1f}" '
            f'stroke="{ASH}" stroke-opacity="{0.55 if is_long else 0.28}" stroke-width="1"/>'
        )
    bloom.append("</g>")
    p.extend(bloom)

    p.append(f'<rect width="{W}" height="{H}" fill="url(#vig)" pointer-events="none"/>')

    p.append(
        f'<circle cx="{cx}" cy="{cy}" r="30" fill="url(#coreglow)" opacity=".65">'
        f'<animate attributeName="opacity" values=".45;.8;.45" dur="3.6s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    p.append(
        f'<circle cx="{cx}" cy="{cy}" r="4" fill="{HOT}">'
        f'<animate attributeName="r" values="3.5;6;3.5" dur="3.6s" repeatCount="indefinite"/>'
        f'</circle>'
    )

    p.append(f'<line x1="570" y1="80" x2="570" y2="520" stroke="{LINE}" stroke-width="1"/>')
    for yy in range(80, 521, 40):
        p.append(f'<line x1="570" y1="{yy}" x2="576" y2="{yy}" stroke="{FAINT}" stroke-width="1"/>')

    x = 602
    p.append(txt(x, 112, "SIGNAL / 001", 10, RED, "700", "3"))
    p.append(txt(x, 166, NAME, 48, BONE, "800", "1"))
    p.append(f'<line x1="{x}" y1="186" x2="870" y2="186" stroke="{RED}" stroke-width="1"/>')
    p.append(txt(x, 212, TAGLINE, 11, ASH, "400", "4"))
    p.append(txt(x, 320, str(TOTAL), 104, RED, "800", "-2"))
    p.append(txt(x, 348, "CONTRIBUTIONS", 10, ASH, "400", "3"))
    p.append(txt(x, 380, f"{N} DAYS   ·   PEAK {PEAK}   ·   {START[:4]}—{END[:4]}", 9.5, ASH, "400", ".5"))
    p.append(f'<line x1="{x}" y1="404" x2="870" y2="404" stroke="{LINE}" stroke-width="1"/>')
    p.append(txt(x, 434, "JOSEPH BOAFO AFFUL", 11, BONE, "700", "2"))
    p.append(txt(x, 454, "COMPUTER SCIENCE · KNUST", 9.5, ASH, "400", "1"))
    p.append(txt(x, 472, "GHANA · 6.6885° N, 1.6244° W", 9.5, ASH, "400", ".5"))
    p.append(txt(x, 500, "GENERATED FROM REAL ACTIVITY", 8, DIM, "400", "1.5"))
    p.append(txt(x, 514, f"LAST SYNC {datetime.date.today().isoformat()}", 8, DIM, "400", "1.5"))

    p.append(
        f'<circle cx="{x + 4}" cy="548" r="3.5" fill="{RED}">'
        f'<animate attributeName="opacity" values="1;.15;1" dur="1.8s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    p.append(txt(x + 16, 552, "LIVE SIGNAL", 9, RED, "700", "2.5"))

    p.append(txt(30, 560, "FIG. 01 — A YEAR IN BLOOM", 9, ASH, "700", "2"))
    p.append(txt(30, 575, "EACH SEED IS A DAY. BRIGHTNESS IS CONTRIBUTIONS.", 8, DIM, "400", "1.5"))

    p.append("</svg>")
    save("signal.svg", "".join(p))


# ---------------------------------------------------------------- pulse
def pulse():
    W, H = 900, 190
    bar_w = 840 / N
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="Daily contribution signal">'
    ]
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    for y in (70, 105, 140):
        p.append(f'<line x1="30" y1="{y}" x2="870" y2="{y}" stroke="#FFFFFF" stroke-opacity=".035" stroke-width="1"/>')

    p.append(txt(30, 28, "DAILY SIGNAL", 12, RED, "700", "3"))
    p.append(txt(30, 45, f"{N} DAYS  ·  {TOTAL} CONTRIBUTIONS  ·  PEAK {PEAK}", 9, ASH, "400", "1.5"))

    for i, count in enumerate(COUNTS):
        x = 30 + i * bar_w
        height = 2 + (count / PEAK) * 68
        y = 140 - height
        fill, opacity = color_for(count)
        p.append(
            f'<rect x="{x:.2f}" y="{y:.1f}" width="{bar_w - 0.45:.2f}" '
            f'height="{height:.1f}" fill="{fill}" opacity="{opacity}"/>'
        )

    tops = " ".join(
        f"{30 + i * bar_w + bar_w / 2:.1f},{140 - (2 + (count / PEAK) * 68):.1f}"
        for i, count in enumerate(COUNTS)
    )
    p.append(f'<polyline points="{tops}" fill="none" stroke="{RED}" stroke-opacity=".22" stroke-width=".8"/>')

    seen = set()
    for i, day in enumerate(DAYS):
        key = day["date"][:7]
        if key in seen:
            continue
        seen.add(key)
        if i > N - 20:
            continue
        month = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                 "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][int(day["date"][5:7]) - 1]
        p.append(txt(30 + i * bar_w, 162, month, 7.5, DIM, "400", "1", "middle"))

    peak_i = max(range(N), key=lambda i: COUNTS[i])
    peak_x = 30 + peak_i * bar_w + bar_w / 2
    peak_y = 140 - (2 + (COUNTS[peak_i] / PEAK) * 68)
    p.append(f'<circle cx="{peak_x:.1f}" cy="{peak_y:.1f}" r="2.6" fill="{HOT}"/>')
    p.append(txt(peak_x, peak_y - 8, str(PEAK), 8, HOT, "700", "0", "middle"))

    p.append(f'<circle cx="869" cy="140" r="3" fill="{HOT}"/>')
    p.append(txt(869, 162, "NOW", 7.5, HOT, "700", "1", "end"))

    p.append(
        f'<g><rect x="0" y="55" width="2" height="90" fill="{RED}" opacity=".28"/>'
        f'<rect x="-6" y="55" width="14" height="90" fill="{RED}" opacity=".05"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="30 0" to="870 0" dur="7s" repeatCount="indefinite"/></g>'
    )
    p.append("</svg>")
    save("pulse.svg", "".join(p))


# ---------------------------------------------------------------- spectrum
def spectrum():
    W, H = 900, 250
    languages = REPOS["languages"]
    total = sum(languages.values())
    items = sorted(languages.items(), key=lambda kv: kv[1], reverse=True)
    top = items[:6]
    other = sum(v for _, v in items[6:])
    if other:
        top.append(("other", other))
    colors = [RED, "#FF4A55", EMBER, "#C81E2E", "#8A1620", "#5A1018", "#3A3A40"]

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="Language spectrum by bytes">'
    ]
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(txt(30, 30, "LANGUAGE SPECTRUM", 12, RED, "700", "3"))
    p.append(txt(30, 47, f"BY BYTES ACROSS {len(REPOS['repos'])} PUBLIC REPOSITORIES", 9, ASH, "400", "1.5"))
    p.append(
        f'<defs><clipPath id="barclip"><rect x="30" y="80" width="840" height="34">'
        f'<animate attributeName="width" from="0" to="840" dur="1.6s" fill="freeze"/>'
        f'</rect></clipPath></defs>'
    )
    p.append('<g clip-path="url(#barclip)">')
    x = 30
    for i, (name, value) in enumerate(top):
        width = 840 * value / total
        p.append(
            f'<rect x="{x:.2f}" y="80" width="{width:.2f}" height="34" '
            f'fill="{colors[i]}" stroke="{BG}" stroke-width="1"/>'
        )
        if width > 70:
            p.append(txt(x + 10, 102, name.upper(), 9, BONE, "700", "1.5"))
            p.append(txt(x + width - 10, 102, f"{value / total * 100:.1f}%", 9, BONE, "400", "1", "end"))
        x += width
    p.append("</g>")

    for i, (name, value) in enumerate(top):
        col, row = i % 4, i // 4
        lx = 30 + col * 210
        ly = 155 + row * 34
        p.append(f'<rect x="{lx}" y="{ly - 8}" width="8" height="8" fill="{colors[i]}"/>')
        p.append(txt(lx + 16, ly, name.upper(), 9, BONE, "700", "1"))
        p.append(txt(lx + 16, ly + 13, f"{value / total * 100:.1f}%  ·  {value:,} bytes", 8, ASH, "400", ".5"))

    p.append(txt(870, 44, f"TOTAL {total / 1_000_000:.2f} MB", 9, ASH, "400", "1.5", "end"))
    p.append("</svg>")
    save("spectrum.svg", "".join(p))


# ---------------------------------------------------------------- layers
def layers():
    rows = [
        ("L7", "APPLICATION", ["react", "next.js", "django", "vite"]),
        ("L6", "LANGUAGES", ["typescript", "javascript", "python", "java", "c++"]),
        ("L5", "DATA", ["mongodb", "postgresql", "sqlite"]),
        ("L4", "RUNTIME", ["node.js", "express", "vercel"]),
        ("L3", "SYSTEM", ["linux", "git", "github", "vscode"]),
    ]
    W = 900
    row_h, gap, top = 56, 12, 84
    H = top + len(rows) * (row_h + gap) + 40
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="The stack, layer by layer">'
    ]
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    grid = []
    for x in range(0, W + 1, 36):
        grid.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
    for y in range(0, H + 1, 36):
        grid.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    p.append(f'<g stroke="#FFFFFF" stroke-opacity=".02" stroke-width="1">{"".join(grid)}</g>')

    p.append(txt(30, 32, "INSTRUMENTS / LAYER BY LAYER", 12, RED, "700", "2"))
    p.append(txt(30, 49, "THE STACK, FROM APPLICATION TO SYSTEM", 9, ASH, "400", "1.5"))

    axis_x = 24
    p.append(f'<line x1="{axis_x}" y1="{top - 6}" x2="{axis_x}" y2="{H - 42}" stroke="{LINE}" stroke-dasharray="2 5"/>')

    for i, (tag, label, chips) in enumerate(rows):
        y = top + i * (row_h + gap)
        p.append(f'<rect x="42" y="{y}" width="828" height="{row_h}" rx="6" fill="{INK}" stroke="{LINE}"/>')
        p.append(txt(60, y + 23, tag, 14, RED, "800", "1"))
        p.append(txt(60, y + 40, label, 8, ASH, "400", "1.5"))
        x = 150
        for chip in chips:
            width = len(chip) * 7.2 + 22
            p.append(f'<rect x="{x:.1f}" y="{y + 14}" width="{width:.1f}" height="28" rx="4" fill="#151519" stroke="{FAINT}"/>')
            p.append(txt(x + width / 2, y + 33, chip, 11, BONE, "400", "0", "middle"))
            x += width + 8
        p.append(txt(856, y + 33, f"0{i + 1}", 8, DIM, "400", "1", "end"))

    p.append(
        f'<circle cx="{axis_x}" cy="{top}" r="3.5" fill="{RED}">'
        f'<animate attributeName="cy" values="{top};{H - 46};{top}" dur="6s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    p.append(
        f'<circle cx="{axis_x}" cy="{top}" r="3.5" fill="none" stroke="{RED}">'
        f'<animate attributeName="cy" values="{top};{H - 46};{top}" dur="6s" repeatCount="indefinite"/>'
        f'<animate attributeName="r" values="3.5;12" dur=".9s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke-opacity" values=".8;0" dur=".9s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    p.append(txt(450, H - 14, "I DON'T COLLECT TOOLS. I USE THEM TO ANSWER QUESTIONS.", 9, ASH, "400", "2", "middle"))
    p.append("</svg>")
    save("layers.svg", "".join(p))


# ---------------------------------------------------------------- divider
def divider():
    W, H = 900, 28
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="presentation">'
    ]
    p.append(
        f'<defs><linearGradient id="dgrad" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{RED}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{RED}"/>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient></defs>'
    )
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(f'<line x1="0" y1="14" x2="{W}" y2="14" stroke="{LINE}" stroke-width="1"/>')
    for x in range(30, W, 60):
        p.append(f'<line x1="{x}" y1="11" x2="{x}" y2="17" stroke="{FAINT}" stroke-width="1"/>')
    for i, x in enumerate((441, 450, 459)):
        p.append(f'<rect x="{x}" y="12" width="3" height="3" fill="{RED}" opacity="{0.5 + i * 0.25}"/>')
    p.append(
        f'<rect x="0" y="13" width="130" height="2" fill="url(#dgrad)">'
        f'<animate attributeName="x" from="-130" to="{W}" dur="4.5s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    p.append("</svg>")
    save("divider.svg", "".join(p))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 900, 200
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="The signal continues">'
    ]
    p.append(
        f'<defs>'
        f'<linearGradient id="fgrad" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{RED}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{RED}"/>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="fglow" cx="50%" cy="120%" r="70%">'
        f'<stop offset="0" stop-color="{RED}" stop-opacity=".14"/>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>'
        f'</defs>'
    )
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#fglow)"/>')
    p.append(f'<rect y="0" width="{W}" height="1" fill="url(#fgrad)"/>')

    for bx, by in ((90, 100), (810, 100)):
        for i in range(40):
            angle = i * math.radians(137.5)
            rr = 4 + 26 * math.sqrt(i / 39)
            p.append(
                f'<circle cx="{bx + rr * math.cos(angle):.1f}" cy="{by + rr * math.sin(angle):.1f}" '
                f'r="{0.8 + (i % 4) * 0.4:.1f}" fill="{RED}" opacity=".35"/>'
            )

    p.append(
        f'<text x="{W / 2}" y="86" text-anchor="middle" font-family="{SERIF}" '
        f'font-size="36" fill="{BONE}">THE SIGNAL CONTINUES'
        f'<tspan fill="{RED}"><animate attributeName="opacity" values="1;0;1" '
        f'keyTimes="0;.5;1" calcMode="discrete" dur="1s" repeatCount="indefinite"/>.</tspan></text>'
    )
    p.append(txt(W / 2, 120, "LEARN  ·  BUILD  ·  BREAK  ·  REBUILD", 11, ASH, "400", "4", "middle"))
    p.append(
        txt(
            W / 2,
            168,
            f"{NAME} / {datetime.date.today().year} / BUILT WITH CURIOSITY AND A LITTLE BIT OF OBSESSION",
            8,
            DIM,
            "400",
            "2",
            "middle",
        )
    )
    p.append("</svg>")
    save("footer.svg", "".join(p))


if __name__ == "__main__":
    signal()
    pulse()
    spectrum()
    layers()
    divider()
    footer()
