#!/usr/bin/env python3
"""News image for Tuesday 24 November 2026 — one dense broadsheet page.

Draws a 1024x1024 newspaper poster with PIL: masthead, three drawn hero
scenes (Riyadh tower strike, TAIEX surge, Shanghai probe), and 29 further
stories in a numbered two-column index — 32 dated stories across 9 regions.
Fully deterministic: no randomness, no network, no timestamps in the image.
If PIL is missing, falls back to copying the pre-rendered poster.png.
Output goes to $MAKEFUN_OUTPUT_DIR/entry.png (or the script directory).
"""

import hashlib
import os
import shutil
import sys

W, H = 1024, 1024
MARGIN = 28
PAPER = (246, 241, 230)
INK = (22, 21, 18)
RED = (163, 22, 33)
BLACK = (16, 16, 16)
GREY = (92, 88, 80)
LIGHT = (233, 227, 214)
NAVY = (16, 28, 46)

# region -> colour chip
REGIONS = {
    "EAST ASIA": (194, 94, 30),
    "EUROPE": (32, 80, 128),
    "MIDDLE EAST": (140, 29, 24),
    "N. AMERICA": (31, 111, 92),
    "LATIN AMERICA": (123, 45, 139),
    "SE ASIA": (46, 125, 50),
    "OCEANIA": (166, 124, 0),
    "AFRICA": (176, 58, 91),
    "SOUTH ASIA": (74, 107, 31),
}

# (number, region, headline, one-line summary, hero kind or None)
# Every story is dated 24 November 2026; numbers below are the reported ones.
STORIES = [
    (1, "MIDDLE EAST", "HOUTHI DRONE HITS RIYADH'S PIF TOWER",
     "11 hurt in second strike on the tower in five days.", "tower"),
    (2, "EAST ASIA", "TAIEX SOARS 9% PAST 40,000",
     "TSMC leads Asia's chip rebound; Kospi +6.3%, Nikkei +3.9%.", "chart"),
    (3, "EAST ASIA", "SHANGHAI PARTY CHIEF UNDER PROBE",
     "Chen Jining is the 4th Politburo member investigated since Oct 2025.", "seal"),
    (4, "EUROPE", "Zaporizhzhia dawn strike kills two",
     "Russian attack wounds 40+, including an infant; 96 drones launched."),
    (5, "EUROPE", "Russian drone in Polish airspace",
     "Eight-minute incursion called deliberate; Warsaw held fire."),
    (6, "EUROPE", "NATO sends AWACS to Poland",
     "Early-warning plane deploys after missile and drone breaches."),
    (7, "N. AMERICA", "Huawei guilty on 10 of 12 counts",
     "Brooklyn jury convicts on trade secrets and bank fraud."),
    (8, "N. AMERICA", "Nvidia +31% as Huang returns",
     "Nasdaq +6.9% and S&P +4.7% in Wall Street's best day in years."),
    (9, "EUROPE", "Sanofi to buy Insmed for $41bn",
     "$175 a share in cash; biggest pharma deal in three years."),
    (10, "EUROPE", "UK heat deaths hit record 5,258",
     "Summer 2026 toll is the highest since records began in 2016."),
    (11, "MIDDLE EAST", "Iran says tankers hit mines",
     "Tehran blames mines in Hormuz as oil slides on diplomacy hopes."),
    (12, "N. AMERICA", "US blacklists Megaspeed, Alibaba unit",
     "Chip-diversion blacklist hits seven South-East Asian firms."),
    (13, "MIDDLE EAST", "Houthis 60 km from Aden",
     "Yemen's army says fighters are ready to attack the port city."),
    (14, "EUROPE", "Britain sanctions Houthis",
     "UK blacklists the group and four senior officials."),
    (15, "EUROPE", "Four-way peace talks take shape",
     "Zelenskyy readies talks with the US, Europe and Russia."),
    (16, "EUROPE", "COP31 collapses in Antalya",
     "No deal as oil states block any mention of fossil fuels."),
    (17, "LATIN AMERICA", "US brands Cartel de los Soles terrorists",
     "Designation raises pressure on Venezuela's Maduro."),
    (18, "SE ASIA", "Factory fire kills 24 in Banten",
     "Blaze at a candy factory in Indonesia; rescuers search ruins."),
    (19, "OCEANIA", "England level T20 series in Australia",
     "England chase 184 on the Gold Coast with overs to spare."),
    (20, "AFRICA", "Senegal regain AFCON title",
     "Court appeal hands back the Africa Cup of Nations crown."),
    (21, "EUROPE", "Ukraine drones hit Russian ships",
     "Strikes reported in the Gulf of Finland and off Libya."),
    (22, "N. AMERICA", "Dell lifts forecasts on AI servers",
     "Record quarter driven by surging AI server demand."),
    (23, "EAST ASIA", "Xiaomi tops estimates; Hon Hai bonds",
     "Revenue beats forecasts; Hon Hai sells $1.5bn convertibles."),
    (24, "EAST ASIA", "China Southern buys Boeing jets",
     "$7.4bn deal for jets from a China Southern unit."),
    (25, "N. AMERICA", "Insmed +14%; HPE slides 11%",
     "Sanofi deal lifts Insmed; margin warning hits HPE."),
    (26, "EAST ASIA", "Hang Seng, Shanghai end mixed",
     "Chip-probe fears weigh as Nvidia faces export scrutiny."),
    (27, "EUROPE", "UK warns over sabotage risk",
     "Firms backing Ukraine face higher Russian sabotage threat."),
    (28, "N. AMERICA", "America's Car-Mart files Ch. 11",
     "Subprime auto dealer collapses as credit strains spread."),
    (29, "EUROPE", "Germany plans petrol price cap",
     "Three-month cap from 2027 to shield drivers from fuel costs."),
    (30, "SOUTH ASIA", "Modi and Merz talk trade and peace",
     "India and Germany agree to work for a rules-based order."),
    (31, "OCEANIA", "Australia, Singapore sign pacts",
     "Supplies MoU and carbon-storage treaty agreed in Canberra."),
    (32, "OCEANIA", "Australia's online-safety deal",
     "Tech giants face fines of up to 5% under new laws."),
]

DATE_STR = "24 NOVEMBER 2026"


def load_fonts():
    from PIL import ImageFont
    base = "/usr/share/fonts/truetype/dejavu/"
    return {
        "title": ImageFont.truetype(base + "DejaVuSerif-Bold.ttf", 54),
        "kicker": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 13),
        "datebar": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 16),
        "lead": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 15),
        "hero_head": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 15),
        "hero_sum": ImageFont.truetype(base + "DejaVuSans.ttf", 11),
        "num": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 11),
        "head": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 13),
        "summ": ImageFont.truetype(base + "DejaVuSans.ttf", 11),
        "strip": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 11),
        "foot": ImageFont.truetype(base + "DejaVuSans.ttf", 10),
        "big": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 34),
        "mid": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 13),
    }


def wrap_text(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, font, max_w, warn):
    """Truncate with ellipsis if a single line overflows; record warning."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    warn.append(text)
    while text and draw.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."


# ---------------- drawn hero scenes (pure PIL shapes) ----------------

def paint_tower(d, x, y, w, h):
    """Night strike on a skyscraper: navy sky, lit tower, orange blast."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(18, 12), (60, 26), (120, 8), (200, 20), (260, 10),
                   (40, 48), (150, 40), (230, 46), (285, 30), (90, 60)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(230, 230, 210))
    tx = x + w // 2 - 27
    # tower in three set-back tiers
    d.rectangle([tx, y + 52, tx + 54, y + h - 14], fill=(38, 52, 74))
    d.rectangle([tx + 8, y + 34, tx + 46, y + 52], fill=(38, 52, 74))
    d.rectangle([tx + 18, y + 20, tx + 36, y + 34], fill=(38, 52, 74))
    d.rectangle([tx + 24, y + 12, tx + 30, y + 20], fill=(52, 68, 96))
    # lit windows
    for row in range(5):
        for col in range(4):
            wx = tx + 6 + col * 12
            wy = y + 60 + row * 15
            if (row + col) % 3 != 0:
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 214, 110))
    # blast at the tower crown
    bx, by = tx + 54, y + 30
    for r, col in [(26, (255, 120, 0)), (18, (255, 180, 60)), (10, (255, 235, 160))]:
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for dx, dy in [(30, -18), (34, 4), (26, 20), (-6, -30), (12, -32)]:
        d.line([bx, by, bx + dx, by + dy], fill=(255, 180, 60), width=3)
    # smoke puffs and ground
    for cx, cy, r in [(tx - 6, y + 44, 12), (tx + 60, y + 52, 14), (tx + 30, y + 38, 10)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 112))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(10, 16, 26))
    # small drone silhouette upper left
    d.rectangle([x + 14, y + 66, x + 30, y + 72], fill=(8, 10, 14))
    for ox in (12, 32):
        d.ellipse([x + ox - 2, y + 64, x + ox + 2, y + 68], fill=(200, 200, 200))


def paint_chart(d, x, y, w, h):
    """Rising market bars with a +9% callout."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=(180, 175, 165), width=1)
    base = y + h - 34
    for gy in range(4):
        gyv = y + 18 + gy * 26
        d.line([x + 10, gyv, x + w - 10, gyv], fill=(228, 224, 214), width=1)
    heights = [22, 34, 30, 48, 62, 78]
    bw, gap = 30, 14
    px = x + 16
    tops = []
    for ht in heights:
        d.rectangle([px, base - ht, px + bw, base], fill=(31, 122, 77))
        tops.append((px + bw // 2, base - ht))
        px += bw + gap
    d.line(tops, fill=(163, 22, 33), width=3)
    for tx, ty in tops:
        d.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=(163, 22, 33))
    d.line([x + 10, base, x + w - 10, base], fill=INK, width=2)
    d.text((x + 14, y + 8), "+9%", font=F["big"], fill=(31, 122, 77))
    d.text((x + 118, y + 16), "TAIEX", font=F["mid"], fill=INK)
    d.text((x + 118, y + 34), "past 40,000", font=F["mid"], fill=GREY)


def paint_seal(d, x, y, w, h):
    """Government building with a red investigation stamp across it."""
    from PIL import Image
    d.rectangle([x, y, x + w, y + h], fill=(223, 227, 232))
    bx, bw = x + 46, w - 92
    d.rectangle([bx, y + 78, bx + bw, y + h - 16], fill=(120, 124, 130))
    d.polygon([(bx - 8, y + 78), (bx + bw + 8, y + 78),
               (bx + bw // 2, y + 52)], fill=(96, 100, 106))
    for i in range(5):
        cx = bx + 14 + i * ((bw - 28) // 4)
        d.rectangle([cx, y + 86, cx + 10, y + h - 26], fill=(235, 236, 238))
    d.rectangle([bx - 6, y + h - 26, bx + bw + 6, y + h - 16], fill=(96, 100, 106))
    # rotated red stamp: solid band, white text, slight tilt
    stamp = Image.new("RGBA", (250, 56), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([2, 2, 247, 53], radius=8, fill=RED + (255,))
    sd.text((125, 28), "UNDER INVESTIGATION", font=F["mid"],
            fill=(255, 255, 255), anchor="mm")
    stamp = stamp.rotate(8, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (x + (w - stamp.width) // 2, y + 68), stamp)
    d.text((x + 12, y + 8), "SHANGHAI", font=F["mid"], fill=INK)


# need ImageDraw at module scope for the painters
from PIL import Image, ImageDraw  # noqa: E402


def build_poster():
    """Render the full 1024x1024 poster; returns (Image, warnings)."""
    global img, F
    from PIL import Image, ImageDraw
    F = load_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    warn = []

    # ---- masthead ----
    d.text((MARGIN, 20), "GLOBAL EDITION", font=F["kicker"], fill=INK)
    d.text((W - MARGIN, 20), "TUESDAY", font=F["kicker"], fill=INK, anchor="ra")
    d.line([MARGIN, 42, W - MARGIN, 42], fill=INK, width=2)
    d.text((W // 2, 52), "THE WORLD IN ONE DAY", font=F["title"],
           fill=INK, anchor="ma")
    bar = "TUESDAY 24 NOVEMBER 2026  ·  32 STORIES  ·  9 REGIONS  ·  DATE-CHECKED"
    d.rectangle([MARGIN, 116, W - MARGIN, 148], fill=BLACK)
    d.text((W // 2, 132), bar, font=F["datebar"], fill=(255, 255, 255), anchor="mm")
    d.text((MARGIN, 158), "SHANGHAI PURGE  ·  RIYADH TOWER STRUCK  ·  TAIEX +9%",
           font=F["lead"], fill=RED)

    # ---- three hero panels ----
    heroes = [s for s in STORIES if len(s) == 5]
    painters = {"tower": paint_tower, "chart": paint_chart, "seal": paint_seal}
    pw, gap = 312, 16
    hy, ph = 188, 148
    for i, s in enumerate(heroes):
        px = MARGIN + i * (pw + gap)
        d.rectangle([px, hy, px + pw, hy + ph], outline=(150, 144, 132), width=1)
        painters[s[4]](d, px + 1, hy + 1, pw - 2, ph - 2)
        cy = hy + ph + 8
        head_lines = wrap_text(d, s[2], F["hero_head"], pw)
        for ln in head_lines:
            d.text((px, cy), ln, font=F["hero_head"], fill=INK)
            cy += 18
        sum_lines = wrap_text(d, s[3], F["hero_sum"], pw)
        for ln in sum_lines:
            d.text((px, cy), ln, font=F["hero_sum"], fill=GREY)
            cy += 14
        tag = s[1]
        d.rectangle([px, hy + ph - 20, px + 8 + d.textlength(tag, font=F["num"]),
                     hy + ph - 4], fill=REGIONS[tag])
        d.text((px + 4, hy + ph - 12), tag, font=F["num"],
               fill=(255, 255, 255), anchor="lm")

    # ---- region strip (counts computed from the data) ----
    counts = {}
    for s in STORIES:
        counts[s[1]] = counts.get(s[1], 0) + 1
    assert len(STORIES) == 32 and len(counts) == 9, (len(STORIES), len(counts))
    strip_y = 424
    d.line([MARGIN, strip_y, W - MARGIN, strip_y], fill=INK, width=1)
    parts = [f"{r} {counts[r]}" for r in
             sorted(counts, key=lambda r: -counts[r])]
    strip = "9 REGIONS — " + "  ·  ".join(parts)
    d.text((MARGIN, strip_y + 8), fit_one_line(d, strip, F["strip"],
           W - 2 * MARGIN, warn), font=F["strip"], fill=INK)

    # ---- numbered story index, two columns ----
    grid = [s for s in STORIES if len(s) == 4]
    assert len(grid) == 29
    col_w = (W - 2 * MARGIN - 32) // 2
    row_h, top = 33, 462
    for idx, s in enumerate(grid):
        col = idx // 15
        row = idx % 15
        gx = MARGIN + col * (col_w + 32)
        gy = top + row * row_h
        if row == 0:
            d.line([gx, gy - 6, gx + col_w, gy - 6], fill=INK, width=1)
        d.rectangle([gx, gy, gx + 22, gy + 16], fill=RED)
        d.text((gx + 11, gy + 8), str(s[0]), font=F["num"],
               fill=(255, 255, 255), anchor="mm")
        tx = gx + 28
        tw = col_w - 28
        head = fit_one_line(d, s[2], F["head"], tw, warn)
        d.text((tx, gy), head, font=F["head"], fill=INK)
        summ = fit_one_line(d, s[3], F["summ"], tw, warn)
        d.text((tx, gy + 16), summ, font=F["summ"], fill=GREY)

    # ---- footer ----
    fy = 972
    d.line([MARGIN, fy, W - MARGIN, fy], fill=INK, width=1)
    foot = ("Sources: Reuters · AP · BBC · Al Jazeera · Xinhua · UKHSA · pm.gov.au"
            "   |   Compiled 24 November 2026   |   All 32 stories dated 24 Nov 2026")
    d.text((W // 2, fy + 12), foot, font=F["foot"], fill=GREY, anchor="ma")
    return img, warn


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__))
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "entry.png")
    try:
        from PIL import Image  # noqa: F401
        poster, warn = build_poster()
        poster.save(out_path, format="PNG")
    except ImportError:
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "poster.png")
        shutil.copyfile(src, out_path)
        warn = []
    data = open(out_path, "rb").read()
    print(f"wrote {out_path} bytes={len(data)} "
          f"sha256={hashlib.sha256(data).hexdigest()}")
    print(f"stories=32 regions=9 warnings={len(warn)}")
    for w in warn:
        print("TRUNCATED:", w)


if __name__ == "__main__":
    main()
