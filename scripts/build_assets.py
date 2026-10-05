#!/usr/bin/env python3
"""
Generates every custom SVG used by README.md into ../assets/.

    python3 scripts/build_assets.py

All SVGs are self-contained (system fonts only, no external requests) and ship
with their own dark panel, so they look right in GitHub light AND dark mode.
Edit the data blocks below (PROJECTS, SOCIALS, TERMINAL_BLOCKS) and re-run.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets"))
STATIC_PREVIEW = "--preview" in sys.argv  # static first frame, for rendering checks

# ───────────────────────────── design tokens ─────────────────────────────
BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
CYAN = "#38bdf8"
VIOLET = "#8b5cf6"
EMERALD = "#10b981"
TEXT = "#e6edf3"
MUTED = "#8b949e"
SOFT = "#9da7b3"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def esc(s):
    return html.escape(s, quote=False)


def tw(s, size, mono=False, bold=False):
    """Rough text width estimate in px (used to size pills / buttons)."""
    k = 0.602 if mono else (0.64 if bold else 0.56)
    return len(s) * size * k


def write(name, body):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name)


def svg_open(w, h, title, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n<defs>{extra_defs}</defs>\n'
    )


GRAD_DEFS = (
    f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">'
    f'<stop offset="0" stop-color="{CYAN}"/><stop offset="0.55" stop-color="{VIOLET}"/>'
    f'<stop offset="1" stop-color="{EMERALD}"/></linearGradient>'
)

# ───────────────────────────── tech pill colours ─────────────────────────────
PILL_COLORS = {
    # frontend → cyan
    "Next.js": CYAN, "Next.js 14": CYAN, "React": CYAN, "TypeScript": CYAN, "Tailwind CSS": CYAN,
    "Vite": CYAN, "ShadCN UI": CYAN, "Radix UI": CYAN, "ITCSS": CYAN,
    # backend / systems → violet
    "NestJS": VIOLET, "PostgreSQL": VIOLET, "Python": VIOLET, "CLI Architecture": VIOLET,
    "Systems Tooling": VIOLET,
    # platform / integrations → emerald
    "Telegram WebApp API": EMERALD, "Web3 / Payment Flow": EMERALD, "Glassmorphism": EMERALD,
}


def pill(x, y, label, color, h=24):
    w = tw(label, 11, bold=True) + 24
    return (
        f'<g transform="translate({x:.1f},{y})">'
        f'<rect width="{w:.1f}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity="0.10" '
        f'stroke="{color}" stroke-opacity="0.45"/>'
        f'<circle cx="11" cy="{h/2}" r="2.5" fill="{color}"/>'
        f'<text x="19" y="{h/2+4}" font-family="{SANS}" font-size="11" font-weight="600" fill="{TEXT}">{esc(label)}</text>'
        f"</g>",
        w,
    )


def flow_pills(tags, x0, y0, max_w, gap=8, row_h=24, row_gap=8):
    """Lay pills out in wrapping rows. Returns (svg, total_height)."""
    out, x, y = [], x0, y0
    for t in tags:
        w = tw(t, 11, bold=True) + 24
        if x + w > x0 + max_w:
            x, y = x0, y + row_h + row_gap
        s, w = pill(x, y, t, PILL_COLORS.get(t, CYAN), row_h)
        out.append(s)
        x += w + gap
    return "".join(out), (y + row_h) - y0


# ───────────────────────────── project icons (40×40 box) ─────────────────────────────
ICONS = {
    "pin": '<path d="M20 9c-4.7 0-8.5 3.6-8.5 8.1 0 5.9 8.5 13.4 8.5 13.4s8.5-7.5 8.5-13.4C28.5 12.6 24.7 9 20 9z"/>'
           '<circle cx="20" cy="17.2" r="3.2"/>',
    "briefcase": '<rect x="10" y="14" width="20" height="14" rx="2.5"/>'
                 '<path d="M16 14v-1.5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2V14M10 20.5h20"/>',
    "exchange": '<circle cx="20" cy="20" r="10"/>'
                '<path d="M14.5 17.5h11m-3-3 3 3-3 3M25.5 23.5h-11m3-3-3 3 3 3"/>',
    "cap": '<path d="M20 11 31 17 20 23 9 17z"/><path d="M14 20v5c0 1.7 2.7 3.5 6 3.5s6-1.8 6-3.5v-5M31 17v7"/>',
    "terminal": '<rect x="9.5" y="11.5" width="21" height="17" rx="3"/><path d="M14.5 17l4 3-4 3M21 24h5"/>',
}

# ───────────────────────────── project data ─────────────────────────────
PROJECTS = [
    dict(
        file="card-safaar.svg", icon="pin", accent=(CYAN, "#3b82f6"),
        title="Safaar Platform", sub="Full-Stack Hotel & Travel Booking Monorepo",
        status="In Development", status_color=CYAN,
        desc=["Booking hotels and trips is fragmented and slow;",
              "one scalable monorepo unifies search, booking and ops."],
        tags=["Next.js 14", "NestJS", "TypeScript", "Tailwind CSS", "PostgreSQL"],
        link="github.com/thefarrukhdev/safaar",
    ),
    dict(
        file="card-careerhub.svg", icon="briefcase", accent=(VIOLET, CYAN),
        title="School 21 CareerHub", sub="Talent Marketplace & Student Career Platform",
        status="Production", status_color=EMERALD,
        desc=["Students and employers lacked one place to connect;",
              "portfolios, vacancy filters and application tracking."],
        tags=["Next.js", "React", "TypeScript", "Tailwind CSS", "ShadCN UI"],
        link="careerhub.21-school.uz",
    ),
    dict(
        file="card-paymex.svg", icon="exchange", accent=(EMERALD, CYAN),
        title="PAYMEX", sub="Telegram Mini App · Fintech & Currency Exchange",
        status="Demo", status_color="#f59e0b",
        desc=["Currency exchange and cross-border payments are clunky;",
              "a mobile-first, glassmorphism flow inside Telegram."],
        tags=["React", "Telegram WebApp API", "ITCSS", "Web3 / Payment Flow"],
        link="Telegram Mini App · demo build",
    ),
    dict(
        file="card-kokand.svg", icon="cap", accent=(CYAN, VIOLET),
        title="Kokand University Platform", sub="University Portal & Alumni Community Platform",
        status="Live Platform", status_color=EMERALD,
        desc=["Admissions, programs and alumni were scattered;",
              "one modern portal for applicants, students and graduates."],
        tags=["React", "TypeScript", "Vite", "Tailwind CSS", "ShadCN UI", "Radix UI"],
        link="kualumni.uz",
    ),
]
WIDE_PROJECT = dict(
    file="card-agychat.svg", icon="terminal", accent=(EMERALD, VIOLET),
    title="agychat", sub="Developer CLI Tool for Antigravity Session Management",
    status="Active", status_color=EMERALD,
    desc=["Antigravity (AGY) sessions are hard to track from the terminal;",
          "a Python CLI to monitor, inspect and manage them in one place."],
    tags=["Python", "CLI Architecture", "Systems Tooling"],
    link="github.com/thefarrukhdev/agychat",
)


def status_pill(x_right, y, label, color):
    w = len(label) * (10 * 0.64 + 0.8) + 36
    x = x_right - w
    return (
        f'<g transform="translate({x:.1f},{y})">'
        f'<rect width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.5"/>'
        f'<circle cx="12" cy="11" r="3" fill="{color}"/>'
        f'<text x="22" y="14.7" font-family="{SANS}" font-size="10" font-weight="700" letter-spacing="0.8" fill="{color}">{esc(label.upper())}</text>'
        f"</g>"
    )


def card(p, W, H, wide=False):
    a1, a2 = p["accent"]
    cid = p["file"].replace(".svg", "").replace("-", "")
    defs = (
        GRAD_DEFS
        + f'<linearGradient id="tile{cid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>'
        + f'<radialGradient id="glow{cid}" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{a1}" stop-opacity="0.22"/><stop offset="1" stop-color="{a1}" stop-opacity="0"/></radialGradient>'
        + f'<linearGradient id="edge{cid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a1}" stop-opacity="0"/><stop offset="0.5" stop-color="{a1}" stop-opacity="0.9"/><stop offset="1" stop-color="{a2}" stop-opacity="0"/></linearGradient>'
        + f'<clipPath id="clip{cid}"><rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="16"/></clipPath>'
    )
    s = svg_open(W, H, f'{p["title"]} — {p["sub"]}', defs)
    s += f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="{BG}" stroke="url(#bd)" stroke-opacity="0.55" stroke-width="1.5"/>\n'
    s += f'<g clip-path="url(#clip{cid})"><rect width="{W}" height="{H}" fill="url(#glow{cid})"/>'
    s += f'<rect x="{W*0.12}" y="0.75" width="{W*0.76}" height="2" fill="url(#edge{cid})"/></g>\n'

    # icon tile
    s += (
        f'<rect x="24" y="24" width="40" height="40" rx="11" fill="url(#tile{cid})"/>'
        f'<g transform="translate(24,24)" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[p["icon"]]}</g>\n'
    )
    s += status_pill(W - 24, 33, p["status"], p["status_color"]) + "\n"

    if not wide:
        s += f'<text x="24" y="98" font-family="{SANS}" font-size="19" font-weight="700" fill="#ffffff">{esc(p["title"])}</text>\n'
        s += f'<text x="24" y="118" font-family="{SANS}" font-size="12" fill="{a1}" fill-opacity="0.95">{esc(p["sub"])}</text>\n'
        s += f'<text font-family="{SANS}" font-size="13" fill="{SOFT}"><tspan x="24" y="148">{esc(p["desc"][0])}</tspan><tspan x="24" y="167">{esc(p["desc"][1])}</tspan></text>\n'
        s += f'<line x1="24" y1="184" x2="{W-24}" y2="184" stroke="{BORDER}" stroke-dasharray="3 5"/>\n'
        tags_svg, _ = flow_pills(p["tags"], 24, 198, W - 48)
        s += tags_svg + "\n"
        s += f'<text x="24" y="{H-22}" font-family="{MONO}" font-size="11.5" fill="{CYAN}">↗ {esc(p["link"])}</text>\n'
    else:
        s += f'<text x="76" y="42" font-family="{SANS}" font-size="19" font-weight="700" fill="#ffffff">{esc(p["title"])}</text>\n'
        s += f'<text x="76" y="62" font-family="{SANS}" font-size="12" fill="{a1}" fill-opacity="0.95">{esc(p["sub"])}</text>\n'
        s += f'<text font-family="{SANS}" font-size="13" fill="{SOFT}"><tspan x="24" y="100">{esc(p["desc"][0])}</tspan><tspan x="24" y="119">{esc(p["desc"][1])}</tspan></text>\n'
        s += f'<line x1="24" y1="136" x2="{W-24}" y2="136" stroke="{BORDER}" stroke-dasharray="3 5"/>\n'
        tags_svg, _ = flow_pills(p["tags"], 24, 150, W - 300)
        s += tags_svg + "\n"
        s += f'<text x="{W-24}" y="167" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{CYAN}">↗ {esc(p["link"])}</text>\n'
    return s + "</svg>\n"


def build_cards():
    CW = 420
    # height shared by all half cards so rows line up
    need = 0
    for p in PROJECTS:
        _, th = flow_pills(p["tags"], 24, 198, CW - 48)
        need = max(need, 198 + th + 20 + 34)
    H = int(need)
    for p in PROJECTS:
        write(p["file"], card(p, CW, H))
    write(WIDE_PROJECT["file"], card(WIDE_PROJECT, 860, 200, wide=True))


# ───────────────────────────── section headers ─────────────────────────────
def section(file, idx, title, tag):
    W, H = 860, 56
    s = svg_open(W, H, title, GRAD_DEFS + f'<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{EMERALD}" stop-opacity="0"/></linearGradient>')
    s += f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>\n'
    s += f'<rect x="14" y="12" width="32" height="32" rx="9" fill="url(#bd)"/>\n'
    s += f'<text x="30" y="33" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{BG}">{idx}</text>\n'
    s += f'<text x="62" y="34.5" font-family="{SANS}" font-size="19" font-weight="700" fill="#ffffff" letter-spacing="0.2">{esc(title)}</text>\n'
    s += f'<text x="{W-20}" y="33" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">{esc(tag)}</text>\n'
    s += f'<rect x="14" y="{H-5}" width="{W-28}" height="2" rx="1" fill="url(#ln)" fill-opacity="0.75"/>\n'
    write(file, s + "</svg>\n")


def build_sections():
    section("section-about.svg", "01", "About", "// who i am")
    section("section-stack.svg", "02", "Skill Ecosystem", "// tools of the trade")
    section("section-metrics.svg", "03", "Live Metrics", "// github, in real time")
    section("section-projects.svg", "04", "Featured Projects", "// selected work")
    section("section-connect.svg", "05", "Connect", "// let's build something")


# ───────────────────────────── group labels + pill clouds ─────────────────────────────
def label(file, text, color):
    w = int(len(text) * (11 * 0.70 + 1.2) + 48)
    h = 30
    s = svg_open(w, h, text)
    s += f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="15" fill="{BG}" stroke="{color}" stroke-opacity="0.5" stroke-width="1.5"/>'
    s += f'<circle cx="16" cy="{h/2}" r="3.5" fill="{color}"/>'
    s += f'<text x="28" y="{h/2+4}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1" fill="{TEXT}">{esc(text)}</text>'
    write(file, s + "</svg>\n")


def build_labels():
    label("label-frontend.svg", "FRONTEND & UI ENGINEERING", CYAN)
    label("label-backend.svg", "BACKEND & SYSTEMS", VIOLET)
    label("label-devops.svg", "DEVOPS & TOOLING", EMERALD)
    label("label-paradigms.svg", "ARCHITECTURE & PARADIGMS", "#f59e0b")


def micro_pills():
    groups = [
        (CYAN, ["Monorepos", "Design Systems", "Glassmorphism", "Component Architecture", "REST APIs", "Responsive UI"]),
        (VIOLET, ["Zustand", "TanStack Query", "Redux Toolkit", "ShadCN UI", "Radix UI", "Axios", "ITCSS"]),
    ]
    W, MAXW, GAP, PH = 860, 800, 10, 32
    items = [(t, col) for col, ts in groups for t in ts]
    rows, cur, cur_w = [], [], 0
    for t, col in items:
        w = tw(t, 12, bold=True) + 36
        add = w + (GAP if cur else 0)
        if cur and cur_w + add > MAXW:
            rows.append(cur)
            cur, cur_w = [], 0
            add = w
        cur.append((t, col, w))
        cur_w += add
    rows.append(cur)
    H = len(rows) * (PH + 12) - 12 + 12
    s = svg_open(W, H, "Architecture paradigms and UI tooling", GRAD_DEFS)
    y = 6
    for row in rows:
        total = sum(w for _, _, w in row) + GAP * (len(row) - 1)
        x = (W - total) / 2
        for t, col, w in row:
            s += (
                f'<g transform="translate({x:.1f},{y})">'
                f'<rect x="0.75" y="0.75" width="{w-1.5:.1f}" height="{PH-1.5}" rx="{(PH-1.5)/2}" fill="{BG}" stroke="{col}" stroke-opacity="0.55" stroke-width="1.5"/>'
                f'<circle cx="15" cy="{PH/2}" r="3" fill="{col}"/>'
                f'<text x="25" y="{PH/2+4.2}" font-family="{SANS}" font-size="12" font-weight="600" fill="{TEXT}">{esc(t)}</text></g>'
            )
            x += w + GAP
        y += PH + 12
    write("pills.svg", s + "</svg>\n")


# ───────────────────────────── hero chips + socials ─────────────────────────────
def chip(file, text, color, dot_pulse=False):
    h = 34
    w = int(tw(text, 12.5, bold=True) + 46)
    s = svg_open(w, h, text)
    s += f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="{(h-1.5)/2}" fill="{BG}" stroke="{color}" stroke-opacity="0.55" stroke-width="1.5"/>'
    if dot_pulse:
        s += (
            f'<circle cx="19" cy="{h/2}" r="4" fill="{color}"/>'
            f'<circle cx="19" cy="{h/2}" r="4" fill="none" stroke="{color}" stroke-width="1.5">'
            f'<animate attributeName="r" values="4;10" dur="1.8s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.8;0" dur="1.8s" repeatCount="indefinite"/></circle>'
        )
    else:
        s += f'<circle cx="19" cy="{h/2}" r="4" fill="{color}"/>'
    s += f'<text x="32" y="{h/2+4.5}" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{TEXT}">{esc(text)}</text>'
    write(file, s + "</svg>\n")


def build_chips():
    chip("chip-location.svg", "Tashkent, Uzbekistan", CYAN)
    chip("chip-school.svg", "School 21 · 42 Network", VIOLET)
    chip("chip-portfolio.svg", "farrukh-dev.me", "#f59e0b")
    chip("chip-status.svg", "Open to new challenges", EMERALD, dot_pulse=True)


SOCIALS = [
    ("social-portfolio.svg", "PORTFOLIO", "farrukh-dev.me", "P", CYAN),
    ("social-telegram.svg", "TELEGRAM", "@Farrukh_Djumayev", "T", "#26a5e4"),
    ("social-x.svg", "X / TWITTER", "@FarrukhDjumayev", "X", "#e6edf3"),
    ("social-instagram.svg", "INSTAGRAM", "farrukh.djumayev", "I", "#e4405f"),
    ("social-email.svg", "EMAIL", "farrukh.front.dev@gmail.com", "@", EMERALD),
]


def build_socials():
    for file, lab, handle, glyph, col in SOCIALS:
        h = 52
        w = int(max(tw(lab, 10, mono=True, bold=True) + 6, tw(handle, 13.5, bold=True)) + 82)
        s = svg_open(w, h, f"{lab} {handle}", GRAD_DEFS)
        s += f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="14" fill="{BG}" stroke="{col}" stroke-opacity="0.5" stroke-width="1.5"/>'
        s += f'<circle cx="28" cy="{h/2}" r="14" fill="{col}"/>'
        s += f'<text x="28" y="{h/2+5}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="800" fill="{BG}">{esc(glyph)}</text>'
        s += f'<text x="54" y="{h/2-4}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.2" fill="{MUTED}">{esc(lab)}</text>'
        s += f'<text x="54" y="{h/2+14}" font-family="{SANS}" font-size="13.5" font-weight="700" fill="#ffffff">{esc(handle)}</text>'
        write(file, s + "</svg>\n")


# ───────────────────────────── macOS terminal hero ─────────────────────────────
T = 27.0                 # total loop length in seconds
SLOT = 9.0               # seconds per command block
CW = 9.03                # monospace char width at 15px
FS = 15
TERMINAL_BLOCKS = [
    ("farrukh", ".currentFocus()", "Architecting Scalable Web & Telegram Mini Apps"),
    ("farrukh", ".education()", "School 21 (42 Network) — Systems & Algorithms"),
    ("farrukh", ".status()", "Available for exciting engineering challenges"),
]


def pct(t):
    return f"{min(max(t / T * 100, 0), 100):.3f}%"


def keyframes(name, points):
    pts = []
    for t, css in points:
        if pts and abs(pts[-1][0] - t) < 1e-6:
            pts[-1] = (t, css)
        else:
            pts.append((t, css))
    if pts[0][0] > 0:
        pts.insert(0, (0, pts[0][1].split(";animation-timing-function")[0]))
    if pts[-1][0] < T:
        pts.append((T, pts[-1][1].split(";animation-timing-function")[0]))
    body = "".join(f"{pct(t)}{{{css}}}" for t, css in pts)
    return f"@keyframes {name}{{{body}}}"


def terminal():
    W, H = 860, 330
    wx, wy, ww, wh = 14, 14, 832, 302
    css, groups = [], []
    css.append("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}")
    css.append(".blink{animation:blink 1s steps(1) infinite}")

    cmd_y, out_y, x0 = 206, 238, 40

    for i, (obj, method, out) in enumerate(TERMINAL_BLOCKS[:1] if STATIC_PREVIEW else TERMINAL_BLOCKS):
        o = i * SLOT
        cmd = f"> {obj}{method}"
        n_cmd, n_out = len(cmd), len(f'=> "{out}"')
        t_cmd0 = 0.5
        t_cmd1 = t_cmd0 + n_cmd * 0.07
        t_out0 = t_cmd1 + 0.7
        t_out1 = t_out0 + n_out * 0.04
        t_end = SLOT - 0.4

        # block visibility
        css.append(keyframes(f"g{i}", [(0, "opacity:0"), (o, "opacity:0"), (o + 0.2, "opacity:1"),
                                       (o + t_end, "opacity:1"), (o + t_end + 0.3, "opacity:0"), (T, "opacity:0")]))
        # curtains (cover rect slides right to reveal text)
        css.append(keyframes(f"cc{i}", [(0, "transform:translateX(0)"),
                                        (o + t_cmd0, f"transform:translateX(0);animation-timing-function:steps({n_cmd},end)"),
                                        (o + t_cmd1, f"transform:translateX({n_cmd*CW:.2f}px)"),
                                        (o + t_end + 0.3, f"transform:translateX({n_cmd*CW:.2f}px)"),
                                        (o + t_end + 0.31, "transform:translateX(0)"), (T, "transform:translateX(0)")]))
        css.append(keyframes(f"co{i}", [(0, "transform:translateX(0)"),
                                        (o + t_out0, f"transform:translateX(0);animation-timing-function:steps({n_out},end)"),
                                        (o + t_out1, f"transform:translateX({n_out*CW:.2f}px)"),
                                        (o + t_end + 0.3, f"transform:translateX({n_out*CW:.2f}px)"),
                                        (o + t_end + 0.31, "transform:translateX(0)"), (T, "transform:translateX(0)")]))
        # cursors
        css.append(keyframes(f"kc{i}", [(0, "opacity:0"), (o + 0.2, "opacity:1"), (o + t_out0, "opacity:0"), (T, "opacity:0")]))
        css.append(keyframes(f"ko{i}", [(0, "opacity:0"), (o + t_out0, "opacity:1"), (o + t_end, "opacity:1"),
                                        (o + t_end + 0.3, "opacity:0"), (T, "opacity:0")]))
        css.append(
            f".g{i}{{animation:g{i} {T}s linear infinite}}"
            f".cc{i}{{animation:cc{i} {T}s linear infinite}}"
            f".co{i}{{animation:co{i} {T}s linear infinite}}"
            f".kc{i}{{animation:kc{i} {T}s linear infinite;animation-name:kc{i}}}"
            f".ko{i}{{animation:ko{i} {T}s linear infinite}}"
            f".kcm{i}{{animation:cc{i} {T}s linear infinite}}"
            f".kom{i}{{animation:co{i} {T}s linear infinite}}"
        )

        g = f'<g class="g{i}">'
        g += (
            f'<text x="{x0}" y="{cmd_y}" font-family="{MONO}" font-size="{FS}" xml:space="preserve">'
            f'<tspan fill="{VIOLET}" font-weight="700">&gt;</tspan><tspan fill="{TEXT}"> </tspan>'
            f'<tspan fill="{CYAN}">{esc(obj)}</tspan><tspan fill="{TEXT}">{esc(method)}</tspan></text>'
            f'<text x="{x0}" y="{out_y}" font-family="{MONO}" font-size="{FS}" xml:space="preserve">'
            f'<tspan fill="{MUTED}">=&gt;</tspan><tspan fill="{EMERALD}"> "{esc(out)}"</tspan></text>'
        )
        if not STATIC_PREVIEW:
            # curtains
            g += f'<rect class="cc{i}" x="{x0-2}" y="{cmd_y-17}" width="640" height="24" fill="{BG}"/>'
            g += f'<rect class="co{i}" x="{x0-2}" y="{out_y-17}" width="640" height="24" fill="{BG}"/>'
            # cursors (translate with curtain, fade by phase)
            g += (f'<g class="kc{i}"><g class="kcm{i}"><rect class="blink" x="{x0}" y="{cmd_y-14}" width="8" height="18" fill="{CYAN}"/></g></g>')
            g += (f'<g class="ko{i}"><g class="kom{i}"><rect class="blink" x="{x0}" y="{out_y-14}" width="8" height="18" fill="{EMERALD}"/></g></g>')
        g += "</g>"
        groups.append(g)

    css.append("@media (prefers-reduced-motion: reduce){.g0,.g1,.g2,.cc0,.cc1,.cc2,.co0,.co1,.co2,.kc0,.kc1,.kc2,.ko0,.ko1,.ko2,.kcm0,.kcm1,.kcm2,.kom0,.kom1,.kom2,.blink{animation:none!important}"
               ".g1,.g2,.kc0,.ko0,.kc1,.ko1,.kc2,.ko2{display:none}.cc0,.co0{display:none}}")

    defs = (
        GRAD_DEFS
        + f'<clipPath id="win"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14"/></clipPath>'
        + '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>'
        + f'<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
    )
    s = svg_open(W, H, "Terminal: farrukh.currentFocus(), farrukh.education(), farrukh.status()", defs)
    if not STATIC_PREVIEW:
        s += f"<style>{''.join(css)}</style>\n"
    # ambient glow
    s += (f'<circle cx="150" cy="300" r="90" fill="{VIOLET}" opacity="0.35" filter="url(#blur)"/>'
          f'<circle cx="720" cy="40" r="90" fill="{CYAN}" opacity="0.30" filter="url(#blur)"/>\n')
    # window
    s += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" fill="{BG}"/>\n'
    s += f'<g clip-path="url(#win)"><rect x="{wx}" y="{wy}" width="{ww}" height="38" fill="{PANEL}"/>'
    s += f'<line x1="{wx}" y1="{wy+38}" x2="{wx+ww}" y2="{wy+38}" stroke="{BORDER}"/></g>\n'
    s += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" fill="none" stroke="url(#bd)" stroke-opacity="0.7" stroke-width="1.5"/>\n'
    # traffic lights
    for cx, col, st in ((38, "#ff5f56", "#e0443e"), (60, "#ffbd2e", "#dea123"), (82, "#27c93f", "#1aab29")):
        s += f'<circle cx="{cx}" cy="{wy+19}" r="6.5" fill="{col}" stroke="{st}" stroke-width="0.8"/>'
    s += (f'<text x="{W/2}" y="{wy+24}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">'
          f'farrukh@thefarrukhdev — ~/portfolio — zsh</text>\n')
    # static header lines
    s += (f'<text x="{x0}" y="92" font-family="{MONO}" font-size="{FS}" xml:space="preserve">'
          f'<tspan fill="{EMERALD}">farrukh@tashkent</tspan> <tspan fill="{CYAN}">~/portfolio</tspan> <tspan fill="{MUTED}">%</tspan> <tspan fill="{TEXT}">whoami</tspan></text>\n')
    s += (f'<text x="{x0}" y="120" font-family="{MONO}" font-size="{FS+1}" font-weight="700">'
          f'<tspan fill="url(#nm)">Farrukh Djumayev</tspan><tspan fill="{MUTED}" font-weight="400"> — </tspan>'
          f'<tspan fill="{TEXT}">Frontend Engineer &amp; Software Architect</tspan></text>\n')
    s += (f'<text x="{x0}" y="152" font-family="{MONO}" font-size="12.5" fill="{MUTED}">'
          f'# React · Next.js · TypeScript · Scalable Component Architecture</text>\n')
    s += (f'<text x="{x0}" y="172" font-family="{MONO}" font-size="12.5" fill="{MUTED}">'
          f'# Systems engineering @ School 21 / 42 Network — C/C++ · Algorithms · System Programming</text>\n')
    s += f'<line x1="{x0}" y1="186" x2="{wx+ww-26}" y2="186" stroke="{BORDER}" stroke-dasharray="3 5"/>\n'
    # animated blocks
    s += "\n".join(groups) + "\n"
    # status bar
    s += f'<g clip-path="url(#win)"><rect x="{wx}" y="{wy+wh-28}" width="{ww}" height="28" fill="{PANEL}"/>'
    s += f'<line x1="{wx}" y1="{wy+wh-28}" x2="{wx+ww}" y2="{wy+wh-28}" stroke="{BORDER}"/></g>\n'
    s += (f'<circle cx="{wx+22}" cy="{wy+wh-14}" r="3.5" fill="{EMERALD}"/>'
          f'<text x="{wx+34}" y="{wy+wh-10}" font-family="{MONO}" font-size="11" fill="{MUTED}">online · Tashkent, UZ · UTC+5</text>'
          f'<text x="{wx+ww-22}" y="{wy+wh-10}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{CYAN}">farrukh-dev.me</text>\n')
    out = "terminal.preview.svg" if STATIC_PREVIEW else "terminal.svg"
    write(out, s + "</svg>\n")


if __name__ == "__main__":
    terminal()
    if not STATIC_PREVIEW:
        build_cards()
        build_sections()
        build_labels()
        micro_pills()
        build_chips()
        build_socials()
