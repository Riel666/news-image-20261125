#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024 PNG).

Layout: navy masthead naming the day, one hero panel (Houthis hit
Riyadh's tallest tower, wounding 11, in a second strike in under a
week), three mid panels (Zelenskiy confirms Ukraine hit the Russian
ship Sparta II in the Gulf of Finland; Nvidia's bounce fades as shares
slide 6%; 25 people held hostage in a Cartagena supermarket), two
lower panels (Real Madrid rout PSV 5-1; England crush Australia in
the second T20I), and a ticker of the day's other stories. Flat vector
art only, drawn with Pillow; no network, no downloaded assets.
Rendered at 2x and downscaled.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SS = 2
W = 1024
H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 243, 232)
INK = (20, 20, 22)
NAVY = (20, 33, 61)
NAVY_LT = (38, 58, 96)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
GREY = (90, 88, 82)
SKY = (135, 190, 220)
SEA = (46, 111, 148)
GREEN = (28, 122, 64)
GREEN_LT = (226, 240, 228)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SS)


F_TITLE = font("DejaVuSerif-Bold.ttf", 44)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_KICK = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSerif-Bold.ttf", 25)
F_HEAD_SM = font("DejaVuSerif-Bold.ttf", 21)
F_SUB = font("DejaVuSans.ttf", 16)
F_TICK = font("DejaVuSans.ttf", 14)
F_FOOT = font("DejaVuSans.ttf", 12)


def X(v):
    return v * SS


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= X(max_w):
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((X(x), X(y)), ln, font=fnt, fill=fill)
        y += leading
    return y


def panel(d, x0, y0, x1, y1, fill=WHITE):
    d.rounded_rectangle([X(x0), X(y0), X(x1), X(y1)], radius=X(10),
                        fill=fill, outline=(200, 194, 178), width=X(2))


def kicker(d, x, y, label, color=RED):
    d.text((X(x), X(y)), label, font=F_KICK, fill=color)


def headline(d, x, y, text, max_w, fnt=F_HEAD, leading=30):
    lines = wrap(d, text, fnt, max_w)
    return text_block(d, x, y, lines, fnt, INK, leading)


def sub(d, x, y, text, max_w, leading=21):
    lines = wrap(d, text, F_SUB, max_w)
    return text_block(d, x, y, lines, F_SUB, (60, 58, 54), leading)


def star4(d, cx, cy, r, fill):
    """Four-point compass star."""
    pts = [(cx, cy - r), (cx + r // 4, cy - r // 4), (cx + r, cy),
           (cx + r // 4, cy + r // 4), (cx, cy + r), (cx - r // 4, cy + r // 4),
           (cx - r, cy), (cx - r // 4, cy - r // 4)]
    d.polygon([(X(px), X(py)) for px, py in pts], fill=fill)


def draw():
    img = Image.new("RGB", (X(W), X(H)), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- masthead ----
    d.rectangle([0, 0, X(W), X(118)], fill=NAVY)
    d.text((X(W // 2), X(30)), "THE WORLD IN ONE PICTURE",
           font=F_TITLE, fill=WHITE, anchor="ma")
    d.text((X(W // 2), X(80)), "WEDNESDAY  25  NOVEMBER  2026",
           font=F_DATE, fill=GOLD, anchor="ma")
    d.line([(X(24), X(118)), (X(1000), X(118))], fill=GOLD, width=X(3))

    # ---- hero: Houthis hit Riyadh's tallest tower ----
    panel(d, 24, 132, 1000, 420)
    d.rounded_rectangle([X(40), X(148), X(430), X(404)], radius=X(8), fill=(16, 24, 48))
    # stars
    for sx, sy in [(70, 170), (110, 190), (400, 180), (380, 220), (90, 250),
                   (360, 320), (70, 340), (410, 380)]:
        d.ellipse([X(sx - 2), X(sy - 2), X(sx + 2), X(sy + 2)], fill=WHITE)
    # PIF Tower: tapered silhouette with lit windows
    d.polygon([(X(190), X(392)), (X(208), X(182)), (X(262), X(182)),
               (X(280), X(392))], fill=(52, 64, 92))
    for wy in range(200, 380, 22):
        for wx in (220, 236, 250):
            d.rectangle([X(wx), X(wy), X(wx + 8), X(wy + 10)], fill=GOLD)
    # damage burst halfway up the tower + smoke
    for fx, fy, r, col in [(235, 262, 14, (255, 120, 40)),
                           (248, 250, 18, (255, 180, 60)),
                           (228, 246, 10, (255, 80, 40))]:
        d.ellipse([X(fx - r), X(fy - r), X(fx + r), X(fy + r)], fill=col)
    for sx, sy, r in [(235, 218, 16), (252, 206, 12), (222, 204, 10)]:
        d.ellipse([X(sx - r), X(sy - r), X(sx + r), X(sy + r)],
                  fill=(120, 120, 128))
    # drone top right
    d.line([(X(330), X(196)), (X(356), X(196))], fill=WHITE, width=X(3))
    d.line([(X(343), X(188)), (X(343), X(204))], fill=WHITE, width=X(3))
    d.ellipse([X(339), X(192), X(347), X(200)], fill=(255, 80, 40))
    d.text((X(48), X(154)), "RIYADH",
           font=font("DejaVuSans-Bold.ttf", 13), fill=WHITE, anchor="la")
    d.text((X(48), X(378)), "PIF TOWER",
           font=font("DejaVuSans-Bold.ttf", 13), fill=WHITE, anchor="la")
    kicker(d, 462, 150, "MIDDLE EAST  •  SAUDI ARABIA")
    y = headline(d, 462, 172, "HOUTHIS HIT RIYADH'S TALLEST TOWER", 500, F_HEAD, 30)
    y = sub(d, 462, y + 8,
            "A drone strike wounds 11 in a second attack on the PIF "
            "Tower in under a week; Riyadh vows a decisive response.",
            500, 21)
    d.line([(X(462), X(348)), (X(972), X(348))], fill=(214, 208, 192), width=X(2))
    d.text((X(462), X(362)), "The tower houses the kingdom's sovereign wealth",
           font=F_TICK, fill=GREY)
    d.text((X(462), X(382)), "fund headquarters; the first strike caused no injuries.",
           font=F_TICK, fill=GREY)

    # ---- mid row: three panels ----
    mid = [(24, 336, "WAR  •  UKRAINE", "KYIV CONFIRMS SHIP STRIKE",
            "Kyiv says the Sparta II carried weapons; Norway urges caution.",
            "ship"),
           (356, 668, "BUSINESS  •  TECH", "NVIDIA BOUNCE FADES",
            "Shares slide 6% a day after the 31% surge on Huang's return.",
            "chart"),
           (688, 1000, "CRIME  •  COLOMBIA", "25 HELD HOSTAGE IN CARTAGENA",
            "Gunmen seize a supermarket after a failed armoured-truck raid.",
            "store")]
    for x0, x1, kick, head, s, art in mid:
        panel(d, x0, 434, x1, 692)
        ax0, ay0, ax1, ay1 = x0 + 14, 448, x1 - 14, 548
        if art == "ship":
            d.rounded_rectangle([X(ax0), X(ay0), X(ax1), X(ay1)], radius=X(8),
                                fill=(16, 42, 66))
            # sea
            d.rectangle([X(ax0), X(ay0 + 62), X(ax1), X(ay1)], fill=(10, 30, 52))
            # cargo ship: hull + containers
            d.polygon([(X(ax0 + 24), X(ay0 + 62)), (X(ax1 - 24), X(ay0 + 62)),
                       (X(ax1 - 44), X(ay1 - 14)), (X(ax0 + 44), X(ay1 - 14))],
                      fill=(40, 40, 44))
            for cx0, col in [(ax0 + 52, (178, 34, 34)),
                             (ax0 + 96, (201, 162, 39)),
                             (ax0 + 140, (28, 122, 64)),
                             (ax0 + 184, (178, 34, 34))]:
                d.rectangle([X(cx0), X(ay0 + 34), X(cx0 + 38), X(ay0 + 62)],
                            fill=col)
            d.rectangle([X(ax1 - 78), X(ay0 + 22), X(ax1 - 44), X(ay0 + 62)],
                        fill=(200, 194, 178))
            # drone above the ship
            d.line([(X(ax1 - 60), X(ay0 + 12)), (X(ax1 - 34), X(ay0 + 12))],
                   fill=WHITE, width=X(2))
            d.ellipse([X(ax1 - 50), X(ay0 + 8), X(ax1 - 42), X(ay0 + 16)],
                      fill=(255, 80, 40))
            # waves
            d.line([(X(ax0 + 16), X(ay1 - 6)), (X(ax1 - 16), X(ay1 - 6))],
                   fill=SKY, width=X(2))
            d.text((X(ax0 + 8), X(ay0 + 6)), "SPARTA II",
                   font=font("DejaVuSans-Bold.ttf", 13), fill=WHITE, anchor="la")
        elif art == "chart":
            d.rounded_rectangle([X(ax0), X(ay0), X(ax1), X(ay1)], radius=X(8),
                                fill=(30, 30, 34))
            # falling red bars (share price) + chip
            bars = [(26, 96), (62, 80), (98, 86), (134, 62), (170, 68),
                    (206, 44), (242, 50), (278, 26), (314, 32)]
            for bx, bh in bars:
                d.rectangle([X(ax0 + bx), X(ay1 - 8 - bh),
                             X(ax0 + bx + 24), X(ay1 - 8)], fill=RED)
            d.rectangle([X(ax0 + 104), X(ay0 + 16), X(ax0 + 204), X(ay0 + 80)],
                        fill=(30, 30, 34), outline=RED, width=X(3))
            d.text((X(ax0 + 154), X(ay0 + 24)), "NVDA",
                   font=font("DejaVuSans-Bold.ttf", 22), fill=WHITE, anchor="ma")
            d.text((X(ax0 + 154), X(ay0 + 54)), "-6%",
                   font=font("DejaVuSans-Bold.ttf", 18), fill=(255, 120, 120),
                   anchor="ma")
            d.text((X(ax0 + 8), X(ay0 + 6)), "NASDAQ",
                   font=font("DejaVuSans-Bold.ttf", 13), fill=WHITE, anchor="la")
        else:
            d.rounded_rectangle([X(ax0), X(ay0), X(ax1), X(ay1)], radius=X(8),
                                fill=(232, 226, 210))
            # supermarket storefront + police lights
            d.rectangle([X(ax0 + 40), X(ay1 - 56), X(ax1 - 40), X(ay1)],
                        fill=(70, 66, 60))
            for i in range(6):
                col = RED if i % 2 == 0 else WHITE
                d.rectangle([X(ax0 + 40 + i * 36), X(ay1 - 76),
                             X(ax0 + 76 + i * 36), X(ay1 - 56)], fill=col)
            d.rectangle([X(ax0 + 120), X(ay1 - 40), X(ax0 + 168), X(ay1)],
                        fill=(30, 30, 34))
            d.ellipse([X(ax0 + 16), X(ay0 + 12), X(ax0 + 40), X(ay0 + 36)],
                      fill=RED)
            d.ellipse([X(ax1 - 40), X(ay0 + 12), X(ax1 - 16), X(ay0 + 36)],
                      fill=(40, 80, 200))
            d.text((X(ax0 + 48), X(ay0 + 6)), "SUPERMARKET",
                   font=font("DejaVuSans-Bold.ttf", 13), fill=NAVY, anchor="la")
            d.text((X((ax0 + ax1) // 2), X(ay1 - 52)), "EXITO",
                   font=font("DejaVuSans-Bold.ttf", 13), fill=WHITE, anchor="ma")
        kicker(d, x0 + 16, 560, kick)
        y = headline(d, x0 + 16, 582, head, x1 - x0 - 32, F_HEAD_SM, 25)
        sub(d, x0 + 16, y + 6, s, x1 - x0 - 32, 20)

    # ---- lower row: two panels ----
    # Real Madrid rout PSV 5-1
    panel(d, 24, 706, 500, 930)
    d.rounded_rectangle([X(38), X(720), X(486), X(812)], radius=X(8), fill=(28, 122, 64))
    # pitch markings
    d.line([(X(262), X(720)), (X(262), X(812))], fill=WHITE, width=X(3))
    d.ellipse([X(222), X(726), X(302), X(806)], outline=WHITE, width=X(3))
    # goal + ball
    d.rectangle([X(392), X(730), X(472), X(802)], outline=WHITE, width=X(4))
    d.line([(X(392), X(730)), (X(472), X(730))], fill=WHITE, width=X(4))
    d.ellipse([X(330), X(748), X(374), X(792)], fill=WHITE, outline=INK, width=X(2))
    d.ellipse([X(346), X(762), X(358), X(774)], fill=INK)
    d.text((X(48), X(724)), "REAL 5 – 1 PSV",
           font=font("DejaVuSans-Bold.ttf", 24), fill=WHITE, anchor="la")
    d.text((X(48), X(756)), "MADRID",
           font=font("DejaVuSans-Bold.ttf", 18), fill=WHITE, anchor="la")
    kicker(d, 40, 824, "SPORT  •  FOOTBALL", color=NAVY_LT)
    headline(d, 40, 846, "REAL MADRID ROUT PSV 5-1", 448, F_HEAD_SM, 25)
    sub(d, 40, 890, "Bellingham stunner and Mbappe brace complete the "
                     "comeback.", 448, 20)

    # England crush Australia in the second T20I
    panel(d, 524, 706, 1000, 930)
    d.rounded_rectangle([X(538), X(720), X(986), X(812)], radius=X(8), fill=(226, 232, 244))
    # cricket pitch + stumps + bat + ball
    d.rectangle([X(700), X(720), X(800), X(812)], fill=(210, 190, 150))
    for sx in (726, 744, 762):
        d.line([(X(sx), X(728)), (X(sx), X(756))], fill=GOLD, width=X(4))
    d.rectangle([X(716), X(724), X(772), X(728)], fill=GOLD)
    d.polygon([(X(830), X(740)), (X(852), X(748)), (X(820), X(800)),
               (X(800), X(792))], fill=(139, 90, 43))
    d.ellipse([X(660), X(770), X(684), X(794)], fill=RED, outline=WHITE,
              width=X(2))
    d.text((X(548), X(724)), "GOLD COAST",
           font=font("DejaVuSans-Bold.ttf", 18), fill=NAVY, anchor="la")
    d.text((X(940), X(724)), "188/2",
           font=font("DejaVuSans-Bold.ttf", 18), fill=NAVY, anchor="ra")
    kicker(d, 540, 824, "SPORT  •  CRICKET")
    headline(d, 540, 846, "ENGLAND CRUSH AUSTRALIA", 448, F_HEAD_SM, 25)
    sub(d, 540, 890, "Donald's 85 off 32 balls levels the T20 series 1-1.",
        448, 20)

    # ---- ticker + sources ----
    d.rectangle([0, X(944), X(W), X(H)], fill=NAVY)
    d.text((X(24), X(956)),
           "ALSO TODAY:  Trump gives Giuliani the Medal of Freedom  •  "
           "Sweden nominates Kristersson for PM  •  Iraq orders seizure of "
           "Kurdish oilfields",
           font=F_TICK, fill=WHITE)
    d.text((X(24), X(982)),
           "Leaked records put Russian war dead at 720,000  •  Citi weighs "
           "a Venezuela return  •  Trump spares turkeys Freedom and Feathers",
           font=F_TICK, fill=(200, 205, 220))
    d.text((X(W // 2), X(1006)), "Sources: Reuters  •  AP  •  BBC  •  UEFA  •  ESPNcricinfo — as reported on 25 November 2026",
           font=F_FOOT, fill=GOLD, anchor="ma")

    out = img.resize((W, H), Image.LANCZOS)
    out.save("entry.png", optimize=True)
    print("wrote entry.png (1024, 1024) %d bytes" % os.path.getsize("entry.png"))


if __name__ == "__main__":
    draw()
