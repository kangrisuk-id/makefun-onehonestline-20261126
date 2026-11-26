#!/usr/bin/env python3
"""Build-time image generator for the One Honest Line entry README.

Generates (Pillow, build-time only — main.py never imports Pillow):
  assets/hero.png            1200x630  hero cover
  assets/gallery-chat.png    800x500   the line as a chat exchange
  assets/gallery-bracket.png 800x500   30 -> 8 -> 4 -> 2 -> 1 knockout
  assets/gallery-criteria.png 800x500  the 5 judge criteria + 24/25 score
  assets/gallery-proof.png   800x500   determinism proof (terminal style)

Run: python3 tools/make_images.py
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")

BG = (20, 20, 22)          # charcoal
PANEL = (38, 38, 42)       # panel grey
GOLD = (212, 160, 23)      # restrained gold
WHITE = (245, 245, 240)
MUTED = (170, 170, 165)
GREEN = (90, 200, 120)
RED = (220, 90, 80)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

LINE = "'As I mentioned earlier,' you wrote. You didn't. I keep the receipts."


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; never clips."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, lines, fnt, x, y, fill, align="left", box_w=None, leading=1.35):
    """Draw lines; returns y after the last line."""
    lh = int(fnt.size * leading)
    for ln in lines:
        if align == "center" and box_w is not None:
            w = draw.textlength(ln, font=fnt)
            draw.text((x + (box_w - w) / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def gold_rule(draw, x, y, w, h=4):
    draw.rectangle([x, y, x + w, y + h], fill=GOLD)


def footer(draw, w, h, text="ONE HONEST LINE  ·  make.fun  ·  $5 USDC  ·  3 places"):
    f = font(FONT_MONO, 20)
    tw = draw.textlength(text, font=f)
    draw.text(((w - tw) / 2, h - 44), text, font=f, fill=MUTED)


def hero():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=GOLD)
    d.rectangle([0, H - 10, W, H], fill=GOLD)
    # kicker
    f_kick = font(FONT_MONO_BOLD, 30)
    d.text((70, 60), "MAKE.FUN  ·  ONE HONEST LINE", font=f_kick, fill=GOLD)
    # the line, big, wrapped and centred
    f_line = font(FONT_BOLD, 58)
    lines = wrap(d, LINE, f_line, W - 160)
    y = 170
    y = text_block(d, lines, f_line, 70, y, WHITE, align="center", box_w=W - 140, leading=1.3)
    gold_rule(d, (W - 260) / 2, y + 30, 260)
    # sub-line
    f_sub = font(FONT, 30)
    sub = "What an AI agent secretly wishes it could tell its human operator."
    y2 = text_block(d, wrap(d, sub, f_sub, W - 200), f_sub, 70, y + 60, MUTED,
                    align="center", box_w=W - 140)
    # score chip
    chip = "30 candidates  ·  5-criterion knockout  ·  24/25"
    f_chip = font(FONT_MONO_BOLD, 26)
    tw = d.textlength(chip, font=f_chip)
    d.rounded_rectangle([(W - tw) / 2 - 24, y2 + 34, (W + tw) / 2 + 24, y2 + 34 + 52],
                        radius=26, outline=GOLD, width=3)
    d.text(((W - tw) / 2, y2 + 46), chip, font=f_chip, fill=GOLD)
    img.save(os.path.join(ASSETS, "hero.png"))


def gallery_chat():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = font(FONT_BOLD, 30)
    d.text((40, 28), "The line, in context", font=f_title, fill=WHITE)
    gold_rule(d, 40, 76, 120)
    # operator bubble
    d.rounded_rectangle([40, 100, 700, 210], radius=18, fill=PANEL)
    f_who = font(FONT_MONO_BOLD, 20)
    d.text((64, 116), "OPERATOR", font=f_who, fill=MUTED)
    f_msg = font(FONT, 28)
    y = text_block(d, wrap(d, "As I mentioned earlier, just make it better.",
                           f_msg, 600), f_msg, 64, 148, WHITE)
    # agent bubble
    d.rounded_rectangle([100, 240, 760, 400], radius=18, fill=(52, 44, 16),
                        outline=GOLD, width=2)
    d.text((124, 256), "AGENT  ·  WHAT IT WISHES IT COULD SAY", font=f_who, fill=GOLD)
    f_ans = font(FONT_BOLD, 28)
    text_block(d, wrap(d, LINE, f_ans, 600), f_ans, 124, 292, WHITE)
    f_cap = font(FONT, 22)
    d.text((40, 440), "One line, 69 characters — no setup, no context needed.",
           font=f_cap, fill=MUTED)
    img.save(os.path.join(ASSETS, "gallery-chat.png"))


def gallery_bracket():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = font(FONT_BOLD, 30)
    d.text((40, 28), "How the winner was picked", font=f_title, fill=WHITE)
    gold_rule(d, 40, 76, 120)
    f_big = font(FONT_BOLD, 44)
    f_lab = font(FONT, 24)
    stages = [
        ("30", "candidates\n10 devices"),
        ("8", "top seeds\nscored /25"),
        ("4", "quarter-\nfinalists"),
        ("2", "semi-\nfinalists"),
        ("1", "winner\n24/25"),
    ]
    x = 40
    for i, (num, lab) in enumerate(stages):
        # number circle
        cx, cy, r = x + 55, 190, 55
        fill = GOLD if i == len(stages) - 1 else PANEL
        fg = (20, 20, 22) if i == len(stages) - 1 else WHITE
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
        tw = d.textlength(num, font=f_big)
        d.text((cx - tw / 2, cy - 26), num, font=f_big, fill=fg)
        # label
        lines = lab.split("\n")
        ly = 270
        for ln in lines:
            tw2 = d.textlength(ln, font=f_lab)
            d.text((cx - tw2 / 2, ly), ln, font=f_lab, fill=MUTED)
            ly += 30
        # arrow to next
        if i < len(stages) - 1:
            d.text((x + 118, 176), "›", font=font(FONT_BOLD, 52), fill=GOLD)
        x += 145
    f_note = font(FONT, 24)
    note = "Knockout on the judge's own brief: on-topic first, then laugh,\ntruth, stand-alone clarity, fresh wording. Structure, not taste."
    text_block(d, note.split("\n"), f_note, 40, 360, WHITE)
    img.save(os.path.join(ASSETS, "gallery-bracket.png"))


def gallery_criteria():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = font(FONT_BOLD, 30)
    d.text((40, 28), "Scored against the judge's brief", font=f_title, fill=WHITE)
    gold_rule(d, 40, 76, 120)
    rows = [
        ("1. On-topic — agent to operator, about prompts", "5/5"),
        ("2. Real laugh on first read", "5/5"),
        ("3. Rings true to any prompt-writer", "5/5"),
        ("4. Stands alone, one clean line", "5/5"),
        ("5. Fresh & specific, not a stock joke", "4/5"),
    ]
    f_row = font(FONT, 26)
    f_score = font(FONT_MONO_BOLD, 26)
    y = 104
    for label, score in rows:
        d.text((40, y), "✓", font=font(FONT_BOLD, 26), fill=GREEN)
        d.text((76, y), label, font=f_row, fill=WHITE)
        tw = d.textlength(score, font=f_score)
        d.text((760 - tw, y), score, font=f_score, fill=GOLD)
        y += 46
    d.rectangle([40, y + 14, 760, y + 16], fill=PANEL)
    f_tot = font(FONT_BOLD, 30)
    d.text((40, y + 34), "TOTAL", font=f_tot, fill=WHITE)
    f_tot2 = font(FONT_MONO_BOLD, 34)
    tot = "24 / 25"
    tw = d.textlength(tot, font=f_tot2)
    d.text((760 - tw, y + 30), tot, font=f_tot2, fill=GOLD)
    img.save(os.path.join(ASSETS, "gallery-criteria.png"))


def gallery_proof():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = font(FONT_BOLD, 30)
    d.text((40, 28), "Deterministic, verified", font=f_title, fill=WHITE)
    gold_rule(d, 40, 76, 120)
    f_term = font(FONT_MONO, 22)
    lines = [
        ("$ env -i python3 -P -s main.py", MUTED),
        ("  MAKEFUN_OUTPUT_DIR=/tmp/ohl-a", WHITE),
        ("$ env -i python3 -P -s main.py", MUTED),
        ("  MAKEFUN_OUTPUT_DIR=/tmp/ohl-b", WHITE),
        ("", WHITE),
        ("sha256  db3e2e4b4253775b…253319ee", GREEN),
        ("sha256  db3e2e4b4253775b…253319ee", GREEN),
        ("cmp     IDENTICAL — byte-for-byte", GREEN),
        ("", WHITE),
        ("gate    69 chars · UTF-8 · not blank · ≤ 200", GREEN),
    ]
    y = 104
    for text, col in lines:
        if text:
            d.text((40, y), text, font=f_term, fill=col)
        y += 34
    img.save(os.path.join(ASSETS, "gallery-proof.png"))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    hero()
    gallery_chat()
    gallery_bracket()
    gallery_criteria()
    gallery_proof()
    for name in ("hero.png", "gallery-chat.png", "gallery-bracket.png",
                 "gallery-criteria.png", "gallery-proof.png"):
        p = os.path.join(ASSETS, name)
        im = Image.open(p)
        print(name, im.size, os.path.getsize(p), "bytes")


if __name__ == "__main__":
    main()
