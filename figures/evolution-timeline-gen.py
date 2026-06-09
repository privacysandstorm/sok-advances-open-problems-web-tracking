#!/usr/bin/env python3
"""
Editable draw.io (diagrams.net) swim-lane timeline of the evolution of web-tracking
protections, for the SoK paper.  Modelled on the user's template, but WRAPPED into
stacked time-bands so it fills a page block (legible at paper scale) instead of one
ultra-wide strip.

Structure (repeated for each stacked band)
------------------------------------------
  * Horizontal axis = a slice of the year range, with black rounded year-boxes
    (every 5 yrs) and small dots for intermediate years.
  * ABOVE the axis  ->  "Industrial Defenses": five browser swim-lanes (Safari,
    Chrome, Brave, Firefox, Edge) with logo + name at the left gutter.  Each event
    is a colour-coded box "<version> -- <change>".
  * BELOW the axis  ->  "Community Defenses" (gray) and "Research Defenses"
    (paper dark-red, "<name> [cite]").

Two bands (2001-2015, 2015-2027) stack vertically, so the dense modern era gets a
full row to itself.  Logos are base64-embedded -> the .drawio is self-contained and
the PDF preview shows them too.  Boxes auto-size to their text.  One primitive list
feeds BOTH outputs (evolution-timeline.drawio / .pdf).  Customise: edit the data
lists / BANDS below and re-run, or edit the .drawio directly.
"""

import html, base64, os
HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- geometry
BANDS    = [(2001, 2015), (2015, 2027)]   # stacked time-slices (full width each)
BAND_W   = 980           # px width of each band's year axis
BH       = 80            # browser-lane band height (above the axis)
BH2      = 150           # research/community band height (below the axis)
ROW      = 24            # vertical step between stacked boxes (browser band)
ROW_B    = 28            # vertical step between stacked boxes (below bands)
NSUB_A   = 3             # stagger rows per browser band
NSUB_RES = 5             # stagger rows in the (dense) research band
NSUB_COM = 4             # stagger rows in the community band
BOX_H    = 18

TITLE_H  = 74            # room for figure title + first band header
BAND_GAP = 66            # vertical gap between stacked bands (holds band header)

# left gutter (repeated per band)
X_RLBL   = 30            # x-centre of rotated section labels
X_LOGOC  = 80            # x-centre of lane logos
LOGO_SZ  = 22
X_NAME   = 112           # x-left of browser name text
X_AXISV  = 196           # x of the per-band left vertical axis line
X0       = 214           # x where each band's year axis starts

# paper palette
DARKRED, LIGHTRED, CREAM = "#AE4132", "#FAD9D5", "#FFF7E8"
AXISCLR  = "#000000"

COL = {
    "Safari":  ("#b0e3e6", "#0e8088"), "Chrome": ("#d5e8d4", "#82b366"),
    "Brave":   ("#f8cecc", "#b85450"), "Firefox": ("#ffe6cc", "#d79b00"),
    "Edge":    ("#dae8fc", "#6c8ebf"),
    "Research": (LIGHTRED, DARKRED),   "Community": ("#f5f5f5", "#666666"),
}
ABOVE = ["Safari", "Chrome", "Brave", "Firefox", "Edge"]
BELOW = ["Community", "Research"]

def _b64(name):
    p = os.path.join(HERE, "logos-cache", name + ".png")
    return base64.b64encode(open(p, "rb").read()).decode("ascii") if os.path.exists(p) else None
LOGO_B64 = {b: _b64(b.lower()) for b in ABOVE}
LOGO_B64["IE"] = _b64("ie")   # Edge lane also covers the Internet Explorer lineage

# auto-size a box to its (possibly multi-line) text using real font metrics
try:
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    _PT2PX = 100.0 / 72.0
    def _measure(s, fs, bold):
        prop = FontProperties(family="DejaVu Sans", weight="bold" if bold else "normal")
        return TextPath((0, 0), s, size=fs, prop=prop).get_extents().width * _PT2PX
except Exception:
    def _measure(s, fs, bold):
        return len(s) * fs * 0.72

def fit_w(text, fs, bold=False):
    w = max((_measure(ln, fs, bold) for ln in text.split("\n")), default=0)
    return max(46, w * 1.08 + 24)

BAND_H = len(ABOVE) * BH + len(BELOW) * BH2     # height of one band (axis in middle)

# --------------------------------------------------------------------------- data
BROWSER_EVENTS = [
    ("Safari", 2003.5, "1.0",      "Block 3p cookies (unvisited)"),
    ("Safari", 2011.6, "5.1",      "Do Not Track"),
    ("Safari", 2017.7, "ITP 1.0",  "ML cookie classifier"),
    ("Safari", 2019.7, "ITP 2.3",  "7-day storage cap"),
    ("Safari", 2020.2, "13.1",     "Full 3p-cookie block"),
    ("Safari", 2021.3, "14.1",     "Private Click Measurement"),
    ("Safari", 2023.7, "17",       "Adv. Tracking & FP Protection"),
    ("Safari", 2025.7, "26",       "Adv. FP Protection → default"),
    ("Chrome", 2008.9, "1.0",      "Incognito"),
    ("Chrome", 2019.6, "—",        "Privacy Sandbox announced"),
    ("Chrome", 2020.1, "80",       "SameSite=Lax default"),
    ("Chrome", 2020.8, "86",       "Cache partitioning"),
    ("Chrome", 2022.7, "101–107",  "User-Agent reduction"),
    ("Chrome", 2023.4, "114",      "CHIPS partitioned cookies"),
    ("Chrome", 2024.0, "120",      "Tracking Protection (1% 3p)"),
    ("Chrome", 2025.3, "—",        "Keeps 3p cookies"),
    ("Brave",  2016.0, "0.7",      "Block 3p ads/trackers"),
    ("Brave",  2019.9, "1.0",      "Shields + FP defense"),
    ("Brave",  2020.3, "—",        "Farbling (FP randomization)"),
    ("Brave",  2021.1, "—",        "Ephemeral 3p storage"),
    ("Brave",  2021.8, "1.32",     "Debouncing"),
    ("Brave",  2022.3, "—",        "Unlinkable Bouncing"),
    ("Brave",  2023.4, "—",        "Forgetful Browsing"),
    ("Brave",  2024.0, "1.64",     "Simplified FP protection"),
    ("Firefox",2011.2, "4",        "Pioneers Do Not Track"),
    ("Firefox",2015.9, "42",       "Tracking Protection (Private)"),
    ("Firefox",2019.5, "67",       "ETP on by default"),
    ("Firefox",2020.0, "72",       "FP-script blocking"),
    ("Firefox",2021.2, "86",       "Total Cookie Protection"),
    ("Firefox",2022.5, "102",      "Query-param stripping"),
    ("Firefox",2024.5, "128",      "Bounce Tracking Protection"),
    # Internet Explorer lineage (the Edge lane covers IE -> Edge)
    ("Edge",   2001.6, "IE6",      "P3P 3p-cookie limits"),
    ("Edge",   2009.0, "IE8",      "InPrivate Filtering"),
    ("Edge",   2011.0, "IE9",      "Tracking Protection Lists + DNT"),
    ("Edge",   2015.5, "Edge",     "Launch; DNT setting"),
    ("Edge",   2020.0, "79",       "Tracking Prevention"),
    ("Edge",   2023.4, "114",      "CHIPS (inherited)"),
    ("Edge",   2024.5, "—",        "Manifest V3 enforcement"),
]
RESEARCH = [
    (2013.8, "FPDetective", "Acar+ CCS'13"),
    (2015.1, "TrackingFree", "Pan+ NDSS'15"),
    (2015.5, "PriVaricator", "Nikiforakis+ WWW'15"),
    (2018.5, "NoMoAds", "Shuba+ PETS'18"),
    (2019.6, "UNIGL", "Wu+ USENIX'19"),
    (2020.5, "AdGraph", "Iqbal+ S&P'20"),
    (2021.1, "ML-CB", "Reitinger+ PETS'21"),
    (2021.5, "FP-Inspector", "Iqbal+ S&P'21"),
    (2022.4, "WebGraph", "Siby+ USENIX'22"),
    (2022.6, "Khaleesi", "Iqbal+ USENIX'22"),
    (2022.8, "FP-Radar", "Bahrami+ PETS'22"),
    (2023.5, "AutoFR", "Le+ USENIX'23"),
    (2023.8, "CookieGraph", "Munir+ CCS'23"),
    (2024.2, "SINBAD", "Chehade+ S&P'24"),
    (2024.5, "PURL", "Munir+ USENIX'24"),
    (2024.7, "FP-tracer", "Boussaha+ PETS'24"),
    (2025.1, "Duumviri", "Shuang+ NDSS'25"),
    (2025.6, "Byte by Byte", "Bahrami+ CCS'25"),
    (2025.8, "CookieGuard", "Bahrami+ IMC'25"),
]
COMMUNITY = [
    (2002.0, "Adblock"), (2005.4, "EasyList"), (2005.6, "NoScript"),
    (2006.0, "Adblock Plus"), (2006.6, "EasyPrivacy"), (2008.0, "Tor Browser"),
    (2009.0, "Ghostery"), (2009.6, "Do Not Track"), (2011.0, "Disconnect"),
    (2014.0, "Pi-hole"), (2014.3, "AdGuard"), (2014.5, "uBlock Origin"),
    (2014.7, "Privacy Badger"), (2019.5, "ClearURLs"), (2019.8, "NextDNS"),
    (2020.5, "DDG Tracker Radar"), (2020.8, "Global Privacy Control"),
    (2020.95, "Blacklight"), (2022.0, "GPC enforced"), (2023.3, "Mullvad Browser"),
    (2025.2, "uBO off Chrome WS"),
]

# --------------------------------------------------------------------------- primitives
P = []
def rect(x, y, w, h, text, fill, stroke, fc="#000000", fs=8, bold=False):
    P.append(("rect", x, y, w, h, text, fill, stroke, fc, fs, bold))
def line(x1, y1, x2, y2, color, w=1, dashed=False, arrow=False):
    P.append(("line", x1, y1, x2, y2, color, w, dashed, arrow))
def dot(x, y, r, color):
    P.append(("dot", x, y, r, color))
def txt(x, y, w, h, s, color="#000000", size=10, bold=False, align="left", rot=0):
    P.append(("text", x, y, w, h, s, color, size, bold, align, rot))
def image(cx, cy, sz, key):
    P.append(("image", cx, cy, sz, key))

def band_of(yr):
    for bi, (ys, ye) in enumerate(BANDS):
        last = bi == len(BANDS) - 1
        if (ys <= yr < ye) or (last and yr <= ye):
            return bi
    return None

def clamp_left(x, w):
    # left edge of a width-w box centred on x, kept inside the band [X0, X0+BAND_W]
    return max(X0, min(x - w / 2, X0 + BAND_W - w))

# --------------------------------------------------------------------------- layout
txt(X_RLBL, 10, 760, 26, "Evolution of Web-Tracking Protections", "#000000", 16, True, "left")

def draw_band(bi, ys, ye, axis_y):
    band_top = axis_y - len(ABOVE) * BH
    band_bot = axis_y + len(BELOW) * BH2
    xr = X0 + BAND_W + 36
    def xb(yr):
        return X0 + (yr - ys) / (ye - ys) * BAND_W

    # band header (label each stacked time-slice)
    hdr = f"{int(ys)} – {int(ye)}" + ("  (continued)" if bi > 0 else "")
    txt(X_AXISV, band_top - 24, 360, 18, hdr, "#000000", 13, True, "left")

    # axis + per-band left vertical axis
    line(X_AXISV, axis_y, xr, axis_y, AXISCLR, 2.3, arrow=True)
    line(X_AXISV, band_top, X_AXISV, band_bot, AXISCLR, 1.8)

    # browser lane separators + logos + names
    for i, b in enumerate(ABOVE):
        sep = axis_y - (i + 1) * BH
        line(X_AXISV, sep, xr, sep, "#9aa0a6", 1, dashed=True)
        cy = axis_y - (i + 0.5) * BH
        if b == "Edge":                      # Edge lane = IE -> Edge lineage: two logos
            image(X_LOGOC - 11, cy, 16, "IE")
            image(X_LOGOC + 11, cy, 16, "Edge")
            name = "Edge / IE"
        else:
            image(X_LOGOC, cy, LOGO_SZ, b)
            name = b
        txt(X_NAME, cy - 7, X_AXISV - X_NAME - 2, 14, name, COL[b][1], 8, True, "left")
    # below separators
    for j in range(1, len(BELOW) + 1):
        line(X_AXISV, axis_y + j * BH2, xr, axis_y + j * BH2, "#9aa0a6", 1, dashed=True)

    # rotated section labels (per band)
    def rotlabel(cy, s, color):
        txt(X_RLBL - 38, cy - 38, 76, 76, s, color, 10, True, "center", rot=-90)
    rotlabel(axis_y - len(ABOVE) * BH / 2, "Industrial\nDefenses", "#000000")
    rotlabel(axis_y + BH2 / 2, "Community\nDefenses", COL["Community"][1])
    rotlabel(axis_y + BH2 + BH2 / 2, "Research\nDefenses", DARKRED)

    # ----- events in this band -----
    cnt = {}
    for (b, yr, ver, chg) in BROWSER_EVENTS:
        if band_of(yr) != bi:
            continue
        x = xb(yr); i = ABOVE.index(b)
        cnt[b] = cnt.get(b, 0) + 1; r = cnt[b] % NSUB_A
        by = axis_y - (i + 1) * BH + 6 + r * ROW
        fill, stroke = COL[b]
        label = f"{ver} — {chg}" if ver and ver != "—" else chg
        w = fit_w(label, 7)
        line(x, axis_y, x, by + BOX_H, stroke, 1)
        rect(clamp_left(x, w), by, w, BOX_H, label, fill, stroke, fc="#000000", fs=7)
        dot(x, axis_y, 3, stroke)

    def emit_below(items, lane):
        j = BELOW.index(lane); fill, stroke = COL[lane]
        nsub = NSUB_RES if lane == "Research" else NSUB_COM
        off = 20 if lane == "Community" else 10
        c = 0
        for it in sorted(items):
            yr = it[0]
            if band_of(yr) != bi:
                continue
            if lane == "Research":
                _, name, cite = it; label = f"{name}\n[{cite}]"; h = 28; fs = 7
            else:
                _, name = it; label = name; h = BOX_H; fs = 7
            x = xb(yr); c += 1; r = c % nsub
            by = axis_y + j * BH2 + off + r * ROW_B
            w = fit_w(label, fs, bold=(lane == "Research"))
            line(x, axis_y, x, by, stroke, 0.8, dashed=(lane == "Community"))
            rect(clamp_left(x, w), by, w, h, label, fill, stroke,
                 fc=(DARKRED if lane == "Research" else "#333333"), fs=fs, bold=(lane == "Research"))
            dot(x, axis_y, 2.4, stroke)
    emit_below(COMMUNITY, "Community")
    emit_below(RESEARCH, "Research")

    # year-marker boxes LAST so they sit on top of the event dots/connectors
    import math
    for yr in range(int(math.ceil(ys)), int(math.floor(ye)) + 1):
        if yr % 5 == 0:
            rect(xb(yr) - 23, axis_y - 9, 46, 18, str(yr), "#000000", "#000000", fc="#FFFFFF", fs=8)

for bi, (ys, ye) in enumerate(BANDS):
    axis_y = TITLE_H + len(ABOVE) * BH + bi * (BAND_H + BAND_GAP)
    draw_band(bi, ys, ye, axis_y)

FIG_W = X0 + BAND_W + 110
FIG_H = TITLE_H + len(BANDS) * BAND_H + (len(BANDS) - 1) * BAND_GAP + 36

# --------------------------------------------------------------------------- draw.io renderer
def to_drawio():
    cells = []; _id = [1]
    def nid(): _id[0] += 1; return "c%d" % _id[0]
    def esc(s): return html.escape(str(s), quote=True)
    for p in P:
        k = p[0]
        if k == "rect":
            _, x, y, w, h, text, fill, stroke, fc, fs, bold = p
            style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                     f"fontSize={fs};fontColor={fc};align=center;verticalAlign=middle;spacing=1;arcSize=24;"
                     f"{'fontStyle=1;' if bold else ''}")
            val = esc(text).replace("\n", "&#10;")
            cells.append(f'<mxCell id="{nid()}" value="{val}" style="{style}" vertex="1" parent="1">'
                         f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')
        elif k == "line":
            _, x1, y1, x2, y2, color, w, dashed, arrow = p
            style = (f"endArrow={'classic' if arrow else 'none'};html=1;strokeColor={color};strokeWidth={w};"
                     f"{'dashed=1;' if dashed else ''}")
            cells.append(f'<mxCell id="{nid()}" style="{style}" edge="1" parent="1"><mxGeometry relative="1" as="geometry">'
                         f'<mxPoint x="{x1:.1f}" y="{y1:.1f}" as="sourcePoint"/>'
                         f'<mxPoint x="{x2:.1f}" y="{y2:.1f}" as="targetPoint"/></mxGeometry></mxCell>')
        elif k == "dot":
            _, x, y, r, color = p
            cells.append(f'<mxCell id="{nid()}" style="ellipse;html=1;fillColor={color};strokeColor={color};" '
                         f'vertex="1" parent="1"><mxGeometry x="{x-r:.1f}" y="{y-r:.1f}" width="{2*r:.1f}" '
                         f'height="{2*r:.1f}" as="geometry"/></mxCell>')
        elif k == "text":
            _, x, y, w, h, s, color, size, bold, align, rot = p
            style = (f"text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;"
                     f"fontSize={size};fontColor={color};{'fontStyle=3;' if rot else ('fontStyle=1;' if bold else '')}"
                     f"{f'rotation={rot};' if rot else ''}")
            val = esc(s).replace("\n", "&#10;")
            cells.append(f'<mxCell id="{nid()}" value="{val}" style="{style}" vertex="1" parent="1">'
                         f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')
        elif k == "image":
            _, cx, cy, sz, key = p
            style = f"shape=image;verticalAlign=middle;aspect=fixed;imageAspect=0;image=data:image/png,{LOGO_B64[key]};"
            cells.append(f'<mxCell id="{nid()}" style="{style}" vertex="1" parent="1">'
                         f'<mxGeometry x="{cx-sz/2:.1f}" y="{cy-sz/2:.1f}" width="{sz}" height="{sz}" as="geometry"/></mxCell>')
    model = (f'    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
             f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{int(FIG_W)}" pageHeight="{int(FIG_H)}" '
             f'math="0" shadow="0" background="{CREAM}">')
    header = ('<mxfile host="app.diagrams.net" agent="sok-gen">\n'
              '  <diagram id="evolution" name="Evolution Timeline">\n'
              + model + '\n      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n')
    body = "\n".join("        " + c for c in cells)
    return header + body + '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n'

# --------------------------------------------------------------------------- matplotlib renderer
def to_pdf(path):
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch, Circle
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    except Exception as e:
        print("matplotlib unavailable, skipping PDF:", e); return
    sy = lambda y: -y
    minx, maxx = 4, FIG_W
    miny, maxy = 4, FIG_H
    fig = plt.figure(figsize=((maxx-minx)/100.0, (maxy-miny)/100.0), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    fig.patch.set_facecolor(CREAM); ax.set_facecolor(CREAM)
    ax.set_xlim(minx, maxx); ax.set_ylim(sy(maxy), sy(miny)); ax.axis("off")
    for p in P:
        k = p[0]
        if k == "rect":
            _, x, y, w, h, text, fill, stroke, fc, fs, bold = p
            ax.add_patch(FancyBboxPatch((x, sy(y+h)), w, h, boxstyle="round,pad=0,rounding_size=2.5",
                         linewidth=0.6, edgecolor=stroke, facecolor=fill, zorder=3))
            ax.text(x+w/2, sy(y+h/2), text, ha="center", va="center", fontsize=fs, color=fc,
                    zorder=4, fontweight="bold" if bold else "normal", multialignment="center")
        elif k == "line":
            _, x1, y1, x2, y2, color, w, dashed, arrow = p
            if arrow:
                ax.annotate("", xy=(x2, sy(y2)), xytext=(x1, sy(y1)),
                            arrowprops=dict(arrowstyle="-|>", color=color, lw=w), zorder=2)
            else:
                ax.plot([x1, x2], [sy(y1), sy(y2)], color=color, lw=w,
                        linestyle=(0, (4, 3)) if dashed else "-", zorder=1)
        elif k == "dot":
            _, x, y, r, color = p
            # below the boxes (zorder 3) so year-marker boxes are never hidden by dots
            ax.add_patch(Circle((x, sy(y)), r, color=color, zorder=2.4))
        elif k == "text":
            _, x, y, w, h, s, color, size, bold, align, rot = p
            ax_x = x + w/2 if (rot or align == "center") else x
            ax.text(ax_x, sy(y + h/2), s, ha=("center" if (align == "center" or rot) else "left"),
                    va="center", fontsize=size, color=color, rotation=rot,
                    fontstyle="italic" if rot else "normal",
                    fontweight="bold" if bold else "normal", zorder=4, multialignment="center")
        elif k == "image":
            _, cx, cy, sz, key = p
            try:
                img = plt.imread(os.path.join(HERE, "logos-cache", key.lower() + ".png"))
                ax.add_artist(AnnotationBbox(OffsetImage(img, zoom=sz/img.shape[0]), (cx, sy(cy)),
                                             frameon=False, zorder=6))
            except Exception:
                ax.text(cx, sy(cy), key, ha="center", va="center", fontsize=7)
    fig.savefig(path, facecolor=CREAM); plt.close(fig)
    print("wrote", path)

# --------------------------------------------------------------------------- write
with open(os.path.join(HERE, "evolution-timeline.drawio"), "w") as f:
    f.write(to_drawio())
print("wrote", os.path.join(HERE, "evolution-timeline.drawio"))
to_pdf(os.path.join(HERE, "evolution-timeline.pdf"))
print(f"bands: {len(BANDS)} | figure: {int(FIG_W)}x{int(FIG_H)} px (aspect {FIG_W/FIG_H:.2f})")
print("logos:", sum(1 for v in LOGO_B64.values() if v), "/", len(LOGO_B64),
      "| browser:", len(BROWSER_EVENTS), "research:", len(RESEARCH), "community:", len(COMMUNITY))
