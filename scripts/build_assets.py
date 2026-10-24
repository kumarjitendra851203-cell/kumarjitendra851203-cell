"""Generates every SVG in /assets. Edit the CONFIG block, then run:  python scripts/build_assets.py
Optional: drop your photo at assets/photo.jpg and re-run - it is embedded automatically."""
import base64, math, random, pathlib, re

# ----------------------------- CONFIG (edit me) -----------------------------
NAME = "JITENDRA KUMAR"
NAME_TITLE = "Jitendra Kumar"
ROLE = "AI & DATA SCIENCE STUDENT"
DEGREE = "B.Tech CSE (AI & Data Science)"
COLLEGE = "SISTec, Bhopal"
INITIALS = "JK"
CHIPS = ["Python", "Machine Learning", "Data Science", "Artificial Intelligence",
         "Deep Learning", "NLP", "Data Visualization", "Neural Networks"]
CARD_STATS = [("3+", "Projects on GitHub"), ("AI & DS", "Specialization"), ("Python", "Primary language")]
# GitHub stats card - REPLACE with your real numbers (github.com/<you> -> contribution graph)
STATS = dict(total=0, since="Jan 1, 2026", streak=0, streak_range="-", longest=0, longest_range="-")
HOURS = [2,1,1,0,0,1,2,3,5,6,6,5,4,5,6,7,6,5,4,6,8,7,5,3]      # commits per hour 00..23 (sample)
LANG_REPO = [("Python", 42), ("C++", 22), ("HTML", 18), ("C", 10), ("Other", 8)]
LANG_COMMIT = [("Python", 55), ("C++", 25), ("HTML", 12), ("C", 5), ("Other", 3)]
MONTHS = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
TIME_SPLIT = (40, 25, 35)   # cleaning, preprocessing, visualization
# ----------------------------------------------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
SANS = "'Segoe UI','Trebuchet MS',Arial,sans-serif"
MONO = "'Courier New',Consolas,monospace"
rng = random.Random(7)

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{SANS}"><defs>{defs}</defs>{body}</svg>')

def save(name, s):
    (OUT / name).write_text(s, encoding="utf-8"); print("wrote", name)

def photo_href():
    p = OUT / "photo.jpg"
    if p.exists():
        return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()
    return None

def text(x, y, t, size=14, fill="#fff", weight="normal", anchor="start", font=None, extra=""):
    f = f' font-family="{font}"' if font else ""
    t = re.sub(r"&(?!amp;|quot;|lt;|gt;)", "&amp;", str(t))
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{f} {extra}>{t}</text>'

# ------------------------------- 1. BANNER ---------------------------------
def banner():
    W, H = 1000, 330
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#03120a"/><stop offset="1" stop-color="#062414"/></linearGradient>'
            '<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#04150c"/><stop offset="0.5" stop-color="#04150c" stop-opacity="0.35"/><stop offset="1" stop-color="#04150c" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="ph" cx="0.6" cy="0.4" r="0.8"><stop offset="0" stop-color="#14532d"/><stop offset="1" stop-color="#04150c"/></radialGradient>'
            '<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<clipPath id="clip"><rect x="2" y="2" width="996" height="326" rx="16"/></clipPath>')
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>', '<g clip-path="url(#clip)">']
    href = photo_href()
    if href:
        b.append(f'<image href="{href}" x="560" y="0" width="440" height="330" preserveAspectRatio="xMidYMid slice"/>')
    else:
        b.append('<rect x="560" y="0" width="440" height="330" fill="url(#ph)"/>')
        b.append(text(790, 205, INITIALS, 130, "#22c55e", "bold", "middle", extra='opacity="0.25"'))
    b.append('<rect x="480" y="0" width="520" height="330" fill="url(#fade)"/></g>')
    for i in range(46):  # stars
        b.append(f'<circle cx="{rng.randint(10,990)}" cy="{rng.randint(10,320)}" r="{rng.choice([0.8,1,1.4])}" fill="#4ade80" opacity="{rng.uniform(.2,.7):.2f}"/>')
    # mini network top-right
    pts = [(880,60),(930,85),(905,125),(955,50),(850,100),(940,150)]
    for a, c in [(0,1),(1,2),(1,3),(0,4),(2,5),(4,2)]:
        b.append(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[c][0]}" y2="{pts[c][1]}" stroke="#4ade80" stroke-width="1" opacity=".7"/>')
    for x, y in pts:
        b.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#052e16" stroke="#4ade80"/>')
    b.append(f'<g filter="url(#glow)">{text(40,135,NAME,66,"#eafff3","bold",extra="letter-spacing=\"2\"")}</g>')
    b.append(text(42, 190, ROLE, 24, "#4ade80", "bold", extra='letter-spacing="7" filter="url(#glow)"'))
    b.append('<line x1="42" y1="208" x2="640" y2="208" stroke="#22c55e" stroke-width="2"/>')
    for row, items in enumerate((CHIPS[:4], CHIPS[4:])):
        x = 42; y = 232 + row * 40
        for c in items:
            w = len(c) * 7.6 + 34
            if x + w > 650: break
            b.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="#06210f" stroke="#166534"/>')
            b.append(f'<circle cx="{x+14}" cy="{y+14}" r="3" fill="#4ade80"/>')
            b.append(text(x + 24, y + 19, c, 12.5, "#bbf7d0", font=MONO))
            x += w + 10
    for (x, y, sx, sy) in [(8,8,1,1),(992,8,-1,1),(8,322,1,-1),(992,322,-1,-1)]:
        b.append(f'<path d="M{x} {y+sy*34} V{y+sy*8} Q{x} {y} {x+sx*8} {y} H{x+sx*34}" fill="none" stroke="#22c55e" stroke-width="3.5"/>')
    save("banner.svg", svg(W, H, "".join(b), defs))

# --------------------------- 2. AI INFOGRAPHIC -----------------------------
CARDS_L = [("DATA LAYER", "PYTHON & DSA", ["Python fundamentals", "C / C++ basics", "Problem solving"]),
           ("DATA LAYER", "DATA HANDLING", ["NumPy and Pandas", "Cleaning messy data", "Feature preparation"]),
           ("DATA LAYER", "VISUALIZATION", ["Matplotlib and Seaborn", "Interactive dashboards", "Data storytelling"])]
CARDS_R = [("INTELLIGENCE LAYER", "MACHINE LEARNING", ["Supervised learning", "Model evaluation", "Scikit-learn"]),
           ("INTELLIGENCE LAYER", "DEEP LEARNING", ["Neural networks", "CNN basics", "PyTorch, TensorFlow"]),
           ("INTELLIGENCE LAYER", "NATURAL LANGUAGE", ["Text classification", "Embeddings", "LLM fundamentals"])]

def card(x, y, w, h, kicker, title, bullets):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#04140b" stroke="#14532d"/>',
         f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="#22c55e" stroke-width="3"/>',
         text(x+14, y+24, kicker, 8.5, "#4ade80", font=MONO, extra='letter-spacing="1.5"'),
         text(x+14, y+46, title, 15, "#fff", "bold"),
         f'<line x1="{x+14}" y1="{y+54}" x2="{x+w-80}" y2="{y+54}" stroke="#14532d"/>']
    for i, t in enumerate(bullets):
        s.append(f'<circle cx="{x+18}" cy="{y+72+i*18-4}" r="2.5" fill="#4ade80"/>')
        s.append(text(x+28, y+72+i*18, t, 12, "#d1fae5"))
    for i, hh in enumerate((14, 24, 18)):  # tiny bar icon
        s.append(f'<rect x="{x+w-52+i*13}" y="{y+52-hh}" width="9" height="{hh}" rx="2" fill="#22c55e" opacity="{.5+i*.25}"/>')
    return "".join(s)

def infographic():
    W, H = 1000, 540
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03120a"/><stop offset="1" stop-color="#021008"/></linearGradient>'
            '<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)" stroke="#14532d"/>']
    b.append(f'<g filter="url(#glow)">{text(500,62,"ARTIFICIAL INTELLIGENCE",44,"#eafff3","bold","middle",extra="letter-spacing=\"6\"")}</g>')
    b.append(text(500, 92, "MACHINE LEARNING / DEEP LEARNING / NLP / DATA VISUALIZATION / PYTHON", 12, "#4ade80", anchor="middle", font=MONO, extra='letter-spacing="3" opacity=".8"'))
    ys = [120, 255, 390]
    for i, (k, t, bl) in enumerate(CARDS_L): b.append(card(30, ys[i], 250, 125, k, t, bl))
    for i, (k, t, bl) in enumerate(CARDS_R): b.append(card(720, ys[i], 250, 125, k, t, bl))
    cx, cy = 500, 305
    b.append(f'<circle cx="{cx}" cy="{cy}" r="165" fill="none" stroke="#22c55e" stroke-dasharray="2 7" opacity=".5"/>')
    layers, xs = [5, 7, 7, 5], [405, 468, 532, 595]
    nodes = [[(xs[i], cy + (j - (n - 1) / 2) * 38) for j in range(n)] for i, n in enumerate(layers)]
    for i in range(3):
        for a in nodes[i]:
            for c in nodes[i + 1]:
                b.append(f'<line x1="{a[0]}" y1="{a[1]:.0f}" x2="{c[0]}" y2="{c[1]:.0f}" stroke="#22c55e" stroke-width=".7" opacity=".28"/>')
    for layer in nodes:
        for x, y in layer:
            b.append(f'<circle cx="{x}" cy="{y:.0f}" r="9" fill="#03120a" stroke="#4ade80" stroke-width="1.6"/><circle cx="{x}" cy="{y:.0f}" r="3.5" fill="#4ade80"/>')
    b.append('<rect x="440" y="130" width="120" height="24" rx="12" fill="#04140b" stroke="#22c55e"/>')
    b.append(text(500, 146, "NEURAL NETWORK", 10, "#eafff3", "bold", "middle", MONO, 'letter-spacing="2"'))
    for i, y in enumerate([182, 317, 452]):  # connectors
        ny = nodes[0][[0, 2, 4][i]][1]; nr = nodes[3][[0, 2, 4][i]][1]
        b.append(f'<path d="M280 {y} C340 {y}, 340 {ny:.0f}, 396 {ny:.0f}" fill="none" stroke="#4ade80" stroke-dasharray="5 4"/>')
        b.append(f'<path d="M720 {y} C660 {y}, 660 {nr:.0f}, 604 {nr:.0f}" fill="none" stroke="#4ade80" stroke-dasharray="5 4"/>')
        b.append(f'<circle cx="280" cy="{y}" r="4" fill="#4ade80"/><circle cx="720" cy="{y}" r="4" fill="#4ade80"/>')
    for x, t in [(405, "INPUT"), (500, "HIDDEN LAYERS"), (595, "OUTPUT")]:
        b.append(text(x, 505, t, 9.5, "#4ade80", anchor="middle", font=MONO, extra='letter-spacing="2"'))
    save("ai-infographic.svg", svg(W, H, "".join(b), defs))

# ---------------------------- 3. PROFILE CARD ------------------------------
def profile_card():
    W, H = 1000, 400
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1b2e"/><stop offset="1" stop-color="#0f1126"/></linearGradient>'
            '<linearGradient id="nm" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#99f6e4"/></linearGradient>'
            '<clipPath id="c"><circle cx="800" cy="195" r="118"/></clipPath>')
    b = [f'<rect width="{W}" height="{H}" rx="20" fill="url(#bg)" stroke="#1e2a44"/>']
    for i in range(24):
        x, y = rng.randint(560, 980), rng.randint(20, 380)
        b.append(f'<circle cx="{x}" cy="{y}" r="{rng.choice([2,3,4])}" fill="{rng.choice(["#818cf8","#a78bfa","#f59e0b","#2dd4bf"])}" opacity=".6"/>')
    b.append('<circle cx="800" cy="195" r="142" fill="none" stroke="#2dd4bf" stroke-opacity=".25" stroke-dasharray="2 6"/>')
    b.append('<path d="M668 270 A140 140 0 0 1 700 120" fill="none" stroke="#a78bfa" stroke-width="5" stroke-linecap="round"/>')
    href = photo_href()
    if href:
        b.append(f'<image href="{href}" x="682" y="77" width="236" height="236" clip-path="url(#c)" preserveAspectRatio="xMidYMid slice"/>')
    else:
        b.append('<circle cx="800" cy="195" r="118" fill="#1e293b"/>' + text(800, 228, INITIALS, 84, "#64748b", "bold", "middle"))
    b.append('<rect x="715" y="300" width="190" height="34" rx="17" fill="#0b1626" stroke="#2dd4bf"/>')
    b.append('<circle cx="735" cy="317" r="4" fill="#2dd4bf"/>' + text(748, 322, "Artificial Intelligence", 13, "#fff", "bold"))
    b.append('<rect x="44" y="38" width="130" height="30" rx="15" fill="#0f3b3a" stroke="#14756f"/><circle cx="64" cy="53" r="5" fill="none" stroke="#2dd4bf"/>' + text(78, 58, "Data Science", 12.5, "#5eead4", "bold"))
    b.append(text(44, 135, NAME_TITLE, 70, "url(#nm)", "bold"))
    b.append(text(46, 175, DEGREE, 19, "#e2e8f0", "bold"))
    b.append(text(46, 203, COLLEGE, 15, "#64748b"))
    x = 46
    for i, c in enumerate(CHIPS[:7]):
        w = len(c) * 7.2 + 32; yy = 228 + (0 if i < 4 else 38)
        if i == 4: x = 46
        b.append(f'<rect x="{x}" y="{yy}" width="{w:.0f}" height="30" rx="10" fill="#111b30" stroke="#22304d"/><circle cx="{x+14}" cy="{yy+15}" r="3.5" fill="{["#2dd4bf","#a78bfa","#f59e0b"][i%3]}"/>')
        b.append(text(x + 25, yy + 20, c, 12.5, "#e2e8f0", "bold")); x += w + 10
    b.append('<line x1="46" y1="318" x2="640" y2="318" stroke="#22304d"/>')
    for i, (big, small) in enumerate(CARD_STATS):
        x = 46 + i * 205
        b.append(f'<rect x="{x}" y="338" width="44" height="44" rx="10" fill="#0f2a2a" stroke="#2dd4bf"/>' + text(x + 22, 367, ["★", "AI", "Py"][i], 15, "#2dd4bf", "bold", "middle"))
        b.append(text(x + 56, 361, big, 25, "#fff", "bold") + text(x + 56, 379, small, 11.5, "#64748b"))
    save("profile-card.svg", svg(W, H, "".join(b), defs))

# ----------------------------- 4. GITHUB STATS -----------------------------
def donut(cx, cy, data, colors):
    r, circ, off, s = 42, 2 * math.pi * 42, 0, []
    tot = sum(v for _, v in data)
    for (n, v), c in zip(data, colors):
        L = circ * v / tot
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="16" stroke-dasharray="{L:.1f} {circ-L:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 {cx} {cy})"/>')
        off += L
    s.append(text(cx, cy + 4, f"{data[0][1]}%", 17, "#fff", "bold", "middle") + text(cx, cy + 18, data[0][0], 9, "#94a3b8", anchor="middle"))
    return "".join(s)

def stats():
    W, H = 1000, 580
    LC = ["#3b82f6", "#ec4899", "#eab308", "#14b8a6", "#f97316"]
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b1a4a"/><stop offset="1" stop-color="#0f1b36"/></linearGradient>'
            '<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#818cf8"/><stop offset="1" stop-color="#4338ca"/></linearGradient>'
            '<linearGradient id="peak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#6366f1"/></linearGradient>'
            '<linearGradient id="ring" x1="0" x2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#2dd4bf"/></linearGradient>')
    P = '#ffffff0d'
    b = [f'<rect width="{W}" height="{H}" rx="26" fill="url(#bg)"/>',
         text(40, 62, "GitHub stats", 30, "#e0e7ff", "bold") + text(40, 84, f"{NAME_TITLE}, AI & DS Student", 12, "#94a3b8")]
    b.append(f'<rect x="30" y="100" width="290" height="130" rx="18" fill="{P}" stroke="#ffffff18"/>' + text(52, 130, "Total contributions", 13, "#a5b4fc") + text(52, 187, str(STATS["total"]), 54, "#e0e7ff", "bold") + text(52, 214, f'{STATS["since"]} to present', 11, "#5eead4", "bold"))
    b.append(f'<rect x="335" y="100" width="330" height="130" rx="18" fill="{P}" stroke="#818cf8"/>')
    frac = min(STATS["streak"] / 60, 1) or .02
    b.append('<circle cx="405" cy="165" r="42" fill="none" stroke="#ffffff1a" stroke-width="9"/>')
    b.append(f'<circle cx="405" cy="165" r="42" fill="none" stroke="url(#ring)" stroke-width="9" stroke-linecap="round" stroke-dasharray="{264*frac:.0f} 264" transform="rotate(-90 405 165)"/>')
    b.append(text(405, 172, str(STATS["streak"]), 28, "#fff", "bold", "middle") + text(405, 188, "days", 10, "#94a3b8", anchor="middle"))
    b.append(text(475, 152, "Current streak", 17, "#e0e7ff", "bold") + text(475, 174, STATS["streak_range"], 12, "#5eead4", "bold") + text(475, 194, "Keep the chain going", 11, "#94a3b8"))
    b.append(f'<rect x="680" y="100" width="290" height="130" rx="18" fill="{P}" stroke="#ffffff18"/>' + text(702, 130, "Longest streak", 13, "#a5b4fc") + text(702, 187, f'{STATS["longest"]}', 54, "#e0e7ff", "bold") + text(780, 187, "days", 17, "#94a3b8") + text(702, 214, STATS["longest_range"], 11, "#5eead4", "bold"))
    b.append(f'<rect x="30" y="245" width="940" height="170" rx="18" fill="{P}" stroke="#ffffff18"/>' + text(52, 275, "Commits by hour", 15, "#e0e7ff", "bold") + text(948, 275, "UTC+5:30", 10, "#94a3b8", anchor="end"))
    mx = max(HOURS) or 1; top3 = sorted(range(24), key=lambda i: -HOURS[i])[:3]
    for i, v in enumerate(HOURS):
        h = max(4, 85 * v / mx); x = 78 + i * 37
        b.append(f'<rect x="{x}" y="{385-h:.0f}" width="22" height="{h:.0f}" rx="5" fill="url(#{"peak" if i in top3 else "bar"})"/>')
        if i % 3 == 0: b.append(text(x + 11, 405, f"{i:02d}", 10, "#94a3b8", anchor="middle"))
    for k, (title, data, x0) in enumerate([("Top languages by repository", LANG_REPO, 30), ("Top languages by commit", LANG_COMMIT, 515)]):
        b.append(f'<rect x="{x0}" y="430" width="455" height="135" rx="18" fill="{P}" stroke="#ffffff18"/>' + text(x0 + 22, 458, title, 14, "#e0e7ff", "bold"))
        for i, (n, v) in enumerate(data):
            y = 482 + i * 16
            b.append(f'<circle cx="{x0+28}" cy="{y-4}" r="4" fill="{LC[i]}"/>' + text(x0 + 42, y, n, 11.5, "#e2e8f0") + text(x0 + 215, y, f"{v}%", 11.5, "#94a3b8", anchor="end"))
        b.append(donut(x0 + 345, 505, data, LC))
    save("github-stats.svg", svg(W, H, "".join(b), defs))

# --------------------------- 5. SPENT MY TIME -------------------------------
def spent():
    W, H = 1000, 620
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1a2b"/><stop offset="1" stop-color="#0c0f24"/></linearGradient>')
    T, O, V = "#2dd4bf", "#f59e0b", "#a78bfa"
    b = [f'<rect width="{W}" height="{H}" rx="26" fill="url(#bg)" stroke="#1e2a44"/>',
         text(44, 82, "Spent My Time", 40, "#fff", "bold") + text(44, 112, "Cleaning, preprocessing and visualizing data, every day I code.", 14, "#94a3b8")]
    for i, (n, c) in enumerate([("Cleaning", T), ("Preprocessing", O), ("Visualization", V)]):
        x = 640 + [0, 90, 215][i]
        b.append(f'<circle cx="{x}" cy="76" r="6" fill="{c}"/>' + text(x + 14, 81, n, 14, "#e2e8f0", "bold"))
    # laptop
    b.append('<rect x="60" y="150" width="300" height="190" rx="12" fill="#0b1324" stroke="#334155" stroke-width="3"/><path d="M30 352 H390 L370 340 H50 Z" fill="#1e293b"/>')
    b.append('<circle cx="80" cy="170" r="4" fill="#2dd4bf"/><circle cx="94" cy="170" r="4" fill="#f59e0b"/><circle cx="108" cy="170" r="4" fill="#a78bfa"/>')
    b.append(text(125, 175, "visualize.py", 12, "#e2e8f0", font=MONO) + '<line x1="122" y1="181" x2="200" y2="181" stroke="#a78bfa" stroke-width="2"/>')
    code = [("import ", "#f472b6", "seaborn as sns", "#e2e8f0"), ("sns.", "#e2e8f0", "heatmap(df.corr())", "#86efac"),
            ("fig = ", "#e2e8f0", "px.line(df, y=\"sales\")", "#fcd34d"), ("fig.", "#e2e8f0", "write_html(\"report.html\")", "#86efac"),
            ("plt.", "#e2e8f0", "savefig(\"eda.png\")", "#93c5fd")]
    for i, (a, ca, c2, cb) in enumerate(code):
        y = 208 + i * 22
        b.append(f'<text x="76" y="{y}" font-size="12.5" font-family="{MONO}"><tspan fill="{ca}">{a}</tspan><tspan fill="{cb}">{c2.replace(chr(34), "&quot;")}</tspan></text>')
    b.append('<rect x="62" y="318" width="296" height="20" fill="#0f1a30"/>' + text(80, 332, "Charts exported", 11, "#cbd5e1"))
    # heatmap
    b.append(text(500, 160, "Daily contributions", 17, "#fff", "bold"))
    cols, step, x0, y0 = 22, 22, 500, 200
    for i, m in enumerate(MONTHS): b.append(text(x0 + i * (cols / len(MONTHS)) * step, 190, m, 11, "#94a3b8"))
    for c in range(cols):
        for r in range(7):
            roll = rng.random()
            if roll < .30: col, op = "#1b2440", 1
            else:
                col = rng.choices([T, O, V], [.45, .3, .25])[0]; op = rng.choice([.35, .55, .8, 1])
            b.append(f'<rect x="{x0+c*step}" y="{y0+r*step}" width="18" height="18" rx="5" fill="{col}" opacity="{op}"/>')
    for i, d in enumerate(["Mon", "Wed", "Fri"]): b.append(text(468, y0 + i * 2 * step + 14, d, 10.5, "#94a3b8", anchor="end"))
    # split bar
    b.append(text(500, 392, "Coding time by stage", 15, "#fff", "bold"))
    tot = sum(TIME_SPLIT); x = 500; wtot = 484
    for (n, c), v in zip([("Cleaning", T), ("Preprocessing", O), ("Visualization", V)], TIME_SPLIT):
        w = wtot * v / tot
        b.append(f'<rect x="{x:.0f}" y="404" width="{w:.0f}" height="20" fill="{c}"/>' + text(x, 448, f'{n} <tspan fill="{c}" font-weight="bold">{v}%</tspan>', 12.5, "#94a3b8"))
        x += w
    b.append('<line x1="44" y1="490" x2="956" y2="490" stroke="#2dd4bf" stroke-opacity=".6"/>')
    for i, c in enumerate([T, O, V]): b.append(f'<circle cx="{[330,630,925][i]}" cy="490" r="7" fill="#0b1324" stroke="{c}" stroke-width="2.5"/>')
    items = [("Data cleaning", ["Missing values, duplicates,", "outliers, inconsistent types"], T), ("Data preprocessing", ["Encoding, scaling and feature", "engineering for modelling"], O), ("Data visualization", ["EDA plots, Matplotlib, Seaborn", "and interactive Plotly reports"], V)]
    for i, (t, ls, c) in enumerate(items):
        x = 44 + i * 306
        b.append(f'<rect x="{x}" y="510" width="294" height="90" rx="14" fill="#0f1830" stroke="{c if i==2 else "#1e2a44"}"/>' + text(x + 24, 540, t, 17, "#fff", "bold") + text(x + 24, 564, ls[0], 12.5, "#94a3b8") + text(x + 24, 582, ls[1], 12.5, "#94a3b8"))
    save("spent-time.svg", svg(W, H, "".join(b), defs))

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    banner(); infographic(); profile_card(); stats(); spent()
