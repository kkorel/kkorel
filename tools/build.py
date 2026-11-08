#!/usr/bin/env python3
"""Build Kuzey Korel's GitHub profile: every SVG panel (light + dark) and README.md.

Usage:
    pip install fonttools        # the only dependency
    python3 tools/build.py

All content comes from profile.toml. Fonts are subset per panel and embedded,
so the panels render identically on every OS and browser.
"""
from __future__ import annotations

import base64
import io
import math
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
ASSETS = ROOT / "assets"
RAW_BASE = "https://raw.githubusercontent.com/kkorel/kkorel/main/assets"

# --------------------------------------------------------------------------- theme
THEMES = {
    "light": dict(
        bg="#FBFAF6", border="#E4DFD3", dots="#E3DED2", ink="#16171B", ink2="#393A40",
        muted="#75736C", accent="#2643C4", accent_soft="#E9EDFB", rule="#E2DDD1",
        chip="#F2EFE7", chip_ink="#4A4A50",
    ),
    "dark": dict(
        bg="#101217", border="#262A32", dots="#1E222A", ink="#EEECE6", ink2="#C8C6BF",
        muted="#8E8C85", accent="#93A9FF", accent_soft="#1B2244", rule="#262A32",
        chip="#181B22", chip_ink="#B9B7B0",
    ),
}

# --------------------------------------------------------------------------- fonts
FONT_FILES = {
    "lm17": "lmroman17-regular.otf",
    "lmit": "lmroman10-italic.otf",
    "lmdemi": "lmromandemi10-regular.otf",
    "caps": "lmromancaps10-regular.otf",
    "mono": "lmmono10-regular.otf",
    "inter": "Inter-Regular.otf",
    "interm": "Inter-Medium.otf",
    "intersb": "Inter-SemiBold.otf",
}


class Font:
    def __init__(self, key: str, path: Path):
        self.key = key
        self.family = f"kk-{key}"
        self.path = path
        f = TTFont(path)
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]
        self.upem = f["head"].unitsPerEm

    def has(self, ch: str) -> bool:
        return ord(ch) in self.cmap

    def width(self, s: str, size: float, ls: float = 0.0) -> float:
        total = 0
        for ch in s:
            g = self.cmap.get(ord(ch))
            if g is None:
                raise SystemExit(f"Font {self.key} has no glyph for {ch!r} (in {s!r})")
            total += self.hmtx[g][0]
        return total * size / self.upem + ls * len(s)


F = {k: Font(k, FONTS / v) for k, v in FONT_FILES.items()}

# style: (font, size, letter-spacing, colour key)
STYLES = {
    "name": ("lm17", 60, 0, "ink"),
    "tagline": ("lmit", 21, 0, "ink2"),
    "sect": ("lmit", 21, 0, "accent"),
    "h2": ("lmdemi", 21, 0, "ink"),
    "h3": ("lmdemi", 20, 0, "ink"),
    "big": ("lm17", 34, 0, "ink"),
    "body": ("inter", 14, 0, "ink2"),
    "small": ("inter", 12.5, 0, "muted"),
    "label": ("intersb", 14, 0, "ink"),
    "medium": ("interm", 14, 0, "ink2"),
    "mono": ("mono", 12.5, 0, "muted"),
    "caps": ("caps", 12.5, 1.0, "muted"),
    "rule": ("lmit", 19, 0, "ink2"),
}


def typo(s: str) -> str:
    """Typographic apostrophes."""
    return s.replace("'", "’")


def wrap(text: str, style: str, maxw: float, size: float | None = None) -> list[str]:
    fk, sz, ls, _ = STYLES[style]
    sz = size or sz
    words, lines, cur = typo(text).split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if F[fk].width(trial, sz, ls) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def measure(text: str, style: str, size: float | None = None) -> float:
    fk, sz, ls, _ = STYLES[style]
    return F[fk].width(typo(text), size or sz, ls)


# --------------------------------------------------------------------------- canvas
@dataclass
class Canvas:
    w: int
    theme: str
    title: str
    desc: str = ""
    els: list[str] = field(default_factory=list)
    used: dict[str, set] = field(default_factory=dict)
    h: float = 0
    framed: bool = True

    @property
    def t(self):
        return THEMES[self.theme]

    def text(self, x, y, s, style, anchor="start", color=None, size=None, weight_key=None):
        fk, sz, ls, ck = STYLES[style]
        fk = weight_key or fk
        s = typo(s)
        F[fk].width(s, size or sz, ls)  # glyph check
        self.used.setdefault(fk, set()).update(s)
        fill = self.t[color or ck] if (color or ck) in self.t else (color or ck)
        attrs = (
            f'x="{x:.1f}" y="{y:.1f}" font-family="{F[fk].family}" font-size="{size or sz}" '
            f'fill="{fill}"'
        )
        if ls:
            attrs += f' letter-spacing="{ls}"'
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        self.els.append(f"<text {attrs}>{escape(s)}</text>")

    def lines(self, x, y, lines, style, lh, **kw):
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, style, **kw)
        return y + (len(lines) - 1) * lh

    def rect(self, x, y, w, h, fill, rx=0, stroke=None, sw=1):
        s = f' stroke="{self.t.get(stroke, stroke)}" stroke-width="{sw}"' if stroke else ""
        self.els.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{self.t.get(fill, fill)}"{s}/>'
        )

    def line(self, x1, y1, x2, y2, color="rule", sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.els.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{self.t[color]}" stroke-width="{sw}"{d}/>'
        )

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=1.5):
        f = self.t[fill] if fill else "none"
        s = f' stroke="{self.t[stroke]}" stroke-width="{sw}"' if stroke else ""
        self.els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{f}"{s}/>')

    def tomb(self, x, y, s=7):
        """QED tombstone, bottom-right anchored at (x, y)."""
        self.rect(x - s, y - s, s, s, "accent")

    def arrow(self, x, y, s=8, color="accent"):
        """North-east arrow with its bottom-left at (x, y)."""
        c = self.t[color]
        self.els.append(
            f'<path d="M{x:.1f} {y:.1f} L{x+s:.1f} {y-s:.1f} M{x+2.5:.1f} {y-s:.1f} '
            f'L{x+s:.1f} {y-s:.1f} L{x+s:.1f} {y-s+5.5:.1f}" stroke="{c}" stroke-width="1.5" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def chip(self, x, y, label, style="mono", fill="chip", color="chip_ink", pad=8, h=22):
        """Draw a chip whose top-left is (x, y); return its width."""
        w = measure(label, style) + 2 * pad
        self.rect(x, y, w, h, fill, rx=h / 2)
        self.text(x + pad, y + h / 2 + 4.2, label, style, color=color)
        return w

    def chips(self, x, y, labels, maxw, gap=6, h=22, **kw):
        """Flow chips left to right, wrapping; return the y of the last row's bottom."""
        cx, cy = x, y
        for lab in labels:
            w = measure(lab, kw.get("style", "mono")) + 2 * kw.get("pad", 8)
            if cx + w > x + maxw and cx > x:
                cx, cy = x, cy + h + gap
            cx += self.chip(cx, cy, lab, h=h, **kw) + gap
        return cy + h

    # ---- output
    def fontface_css(self) -> str:
        css = []
        for fk, chars in sorted(self.used.items()):
            opts = subset.Options()
            opts.flavor = "woff"
            opts.layout_features = ["kern", "liga", "tnum", "lnum"]
            opts.name_IDs = []
            opts.notdef_outline = True
            # recalcTimestamp=False keeps output byte-identical between builds.
            font = TTFont(F[fk].path, recalcTimestamp=False)
            sub = subset.Subsetter(opts)
            sub.populate(text="".join(sorted(chars)) + " ")
            sub.subset(font)
            buf = io.BytesIO()
            font.flavor = "woff"
            font.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            css.append(
                f"@font-face{{font-family:'{F[fk].family}';"
                f"src:url(data:font/woff;base64,{b64}) format('woff');}}"
            )
        return "".join(css)

    def svg(self) -> str:
        h = math.ceil(self.h)
        t = self.t
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{h}" '
            f'viewBox="0 0 {self.w} {h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{escape(self.title)}</title><desc id="d">{escape(self.desc)}</desc>'
            f"<style>{self.fontface_css()}text{{font-kerning:normal;}}</style>"
            f'<defs><pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.2" cy="1.2" r="0.9" fill="{t["dots"]}"/></pattern></defs>'
        )
        if self.framed:
            head += (
                f'<rect x="0.5" y="0.5" width="{self.w-1}" height="{h-1}" rx="14" fill="{t["bg"]}" '
                f'stroke="{t["border"]}"/>'
                f'<rect x="0.5" y="0.5" width="{self.w-1}" height="{h-1}" rx="14" fill="url(#dots)"/>'
            )
        return head + "".join(self.els) + "</svg>"


# --------------------------------------------------------------------------- layout helpers
W = 900
PAD = 40
HALF = 444


def header(c: Canvas, n: int, title: str, y: float = 52, x: float = PAD, right: str = "") -> float:
    """'§n  Title' with a hairline rule underneath; returns the y below it."""
    sect = f"§{n}"
    c.text(x, y, sect, "sect")
    c.text(x + measure(sect, "sect") + 10, y, title, "h2")
    if right:
        c.text(c.w - PAD, y, right, "mono", anchor="end")
    c.line(x, y + 14, c.w - PAD, y + 14)
    return y + 14


# --------------------------------------------------------------------------- panels
def p_hero(d, theme):
    p = d["person"]
    tagline = p.get("tagline", "").strip()
    c = Canvas(W, theme, f"{p['name']}. {tagline}" if tagline else p["name"])
    c.desc = " · ".join(p["meta"]) + f". LinkedIn: {p['linkedin_label']}. Email: {p['email']}."
    c.text(PAD, 50, "github.com/kkorel", "mono")
    c.text(W - PAD, 50, "Curriculum · in brief", "caps", anchor="end")
    c.line(PAD, 64, W - PAD, 64)
    c.text(PAD - 3, 136, p["name"], "name")
    if tagline:
        y = c.lines(PAD, 178, wrap(tagline, "tagline", 520), "tagline", 29) + 40
    else:
        y = 182

    # Decoration: a natural-deduction rule, from proofs to production.
    cx, top = 706, 104 if not tagline else 116
    c.text(cx - 52, top, "proof", "rule", anchor="middle")
    c.text(cx + 52, top, "tests", "rule", anchor="middle")
    c.line(cx - 104, top + 14, cx + 104, top + 14, color="ink2", sw=1.1)
    c.text(cx + 112, top + 19, "(ship)", "caps", color="accent")
    c.text(cx, top + 44, "production", "rule", anchor="middle", color="accent")

    meta = "  ·  ".join(p["meta"])
    c.text(PAD, y, meta, "medium", color="muted")
    y += 24
    c.line(PAD, y, W - PAD, y)
    y += 28
    x = PAD
    c.text(x, y, "LinkedIn", "caps")
    x += measure("LinkedIn", "caps") + 10
    c.text(x, y, p["linkedin_label"], "mono", color="ink")
    x += measure(p["linkedin_label"], "mono") + 34
    c.text(x, y, "Email", "caps")
    x += measure("Email", "caps") + 10
    c.text(x, y, p["email"], "mono", color="ink")
    c.tomb(W - PAD, y + 1)
    c.h = y + 30
    return c


def stat_columns(c, items, y, n_cols, big_size=34):
    """Four-up stat columns with vertical hairlines; returns bottom y."""
    colw = (W - 2 * PAD) / n_cols
    bottoms = []
    for i, it in enumerate(items):
        x = PAD + i * colw + (18 if i else 0)
        inner = colw - (36 if i else 18)
        if i:
            c.line(PAD + i * colw, y - 8, PAD + i * colw, y + 96, color="rule")
        size = big_size
        while measure(it["big"], "big", size) > inner and size > 20:
            size -= 1
        c.text(x, y + 30, it["big"], "big", size=size)
        c.text(x, y + 58, it["label"], "label")
        yy = c.lines(x, y + 78, wrap(it["sub"], "small", inner), "small", 17)
        bottoms.append(yy)
    return max(bottoms + [y + 96])


def p_highlights(d, theme, n):
    h = d["highlights"]
    c = Canvas(W, theme, h["title"])
    c.desc = "; ".join(f"{i['big']} {i['label']}: {i['sub']}" for i in h["items"])
    y = header(c, n, h["title"]) + 26
    c.h = stat_columns(c, h["items"], y, 4) + 30
    return c


def p_now(d, theme, n):
    s = d["now"]
    c = Canvas(W, theme, s["title"])
    c.desc = "; ".join(f"{i['role']}, {i['where']}: {i['note']}" for i in s["items"])
    y = header(c, n, s["title"]) + 40
    numerals = ["i.", "ii.", "iii.", "iv.", "v."]
    for i, it in enumerate(s["items"]):
        c.text(PAD, y, numerals[i], "sect", size=19)
        x = PAD + 44
        c.text(x, y, it["role"], "label", size=15)
        x2 = x + measure(it["role"], "label", 15) + 10
        c.text(x2, y, it["where"], "medium", color="accent")
        c.text(x, y + 22, it["note"], "body", color="muted")
        y += 58
    c.h = y - 10
    return c


def p_experience(d, theme, n):
    s = d["experience"]
    c = Canvas(W, theme, s["title"])
    c.desc = "; ".join(f"{i['when']}: {i['role']}, {i['where']}" for i in s["items"])
    y = header(c, n, s["title"]) + 40
    rail = PAD + 132
    first_y = y
    for i, it in enumerate(s["items"]):
        c.text(PAD, y, it["when"], "mono")
        x = rail + 24
        c.text(x, y, it["role"], "label")
        c.text(x, y + 20, it["where"], "small")
        if it["tag"]:
            tw = measure(it["tag"], "mono") + 16
            c.chip(W - PAD - tw, y - 15, it["tag"], fill="accent_soft", color="accent")
        y += 52
    last_y = y - 52
    c.line(rail, first_y - 4, rail, last_y - 4, color="rule", sw=1.2)
    for i in range(len(s["items"])):
        yy = first_y + i * 52 - 4.5
        c.circle(rail, yy, 4.5, fill="bg", stroke="accent" if i < 2 else "muted")
        if "now" in s["items"][i]["when"]:
            c.circle(rail, yy, 2.2, fill="accent")
    c.h = y - 14
    return c


def p_impact(d, theme, n):
    s = d["impact"]
    c = Canvas(W, theme, s["title"])
    c.desc = s["subtitle"] + " " + "; ".join(f"{i['big']} {i['label']}" for i in s["stats"]) + ". " + " ".join(s["notes"])
    y = header(c, n, s["title"], right="SDE Intern · Jul–Sep 2026") + 34
    y = c.lines(PAD, y, wrap(s["subtitle"], "body", W - 2 * PAD, 15), "body", 23, size=15) + 30
    colw = (W - 2 * PAD) / 4
    for i, it in enumerate(s["stats"]):
        x = PAD + i * colw + (18 if i else 0)
        if i:
            c.line(PAD + i * colw, y - 6, PAD + i * colw, y + 70, color="rule")
        c.text(x, y + 34, it["big"], "big", size=40, color="accent" if i < 3 else "ink")
        c.lines(x, y + 58, wrap(it["label"], "small", colw - 36), "small", 17)
    y += 112
    for note in s["notes"]:
        c.rect(PAD, y - 9, 10, 1.4, "accent")
        y = c.lines(PAD + 22, y - 4, wrap(note, "body", W - 2 * PAD - 22), "body", 21) + 30
    c.h = y - 6
    return c


def p_label(theme, n, title, right=""):
    c = Canvas(W, theme, title, framed=False)
    header(c, n, title, y=34, right=right)
    c.h = 56
    return c


def p_feature(d, theme):
    s = d["work"]["feature"]
    c = Canvas(W, theme, s["name"])
    c.desc = f"{s['name']} ({s['org']}). {s['summary']} " + " ".join(s["points"])
    y = 56
    c.text(PAD, y, s["name"], "h2", size=26)
    c.text(W - PAD - 14, y - 4, s["url"].replace("https://", ""), "mono", anchor="end", color="accent")
    c.arrow(W - PAD - 8, y - 2)
    c.text(PAD, y + 26, s["org"], "mono")
    y += 60
    y = c.lines(PAD, y, wrap(s["summary"], "body", W - 2 * PAD, 15), "body", 23, size=15) + 34
    colw = (W - 2 * PAD - 30) / 2
    ys = [y, y]
    for i, pt in enumerate(s["points"]):
        col = i % 2
        x = PAD + col * (colw + 30)
        yy = ys[col]
        c.rect(x, yy - 9, 10, 1.4, "accent")
        yy = c.lines(x + 20, yy - 4, wrap(pt, "body", colw - 20), "body", 21) + 34
        ys[col] = yy
    y = max(ys) - 8
    c.chips(PAD, y, s["stack"], W - 2 * PAD - 30)
    c.tomb(W - PAD, y + 18)
    c.h = y + 22 + PAD - 6
    return c


def card(s, theme, min_h=0):
    c = Canvas(HALF, theme, s["name"])
    c.desc = f"{s['name']} ({s['tag']}). {s['summary']} " + " ".join(s["points"])
    x0, inner = 30, HALF - 60
    y = 52
    c.text(x0, y, s["name"], "h3", size=23)
    tw = measure(s["tag"], "mono") + 16
    c.chip(HALF - x0 - tw, y - 17, s["tag"], fill="accent_soft", color="accent")
    y += 34
    y = c.lines(x0, y, wrap(s["summary"], "body", inner), "body", 21) + 28
    for pt in s["points"]:
        c.rect(x0, y - 8.5, 9, 1.3, "accent")
        y = c.lines(x0 + 18, y - 4, wrap(pt, "small", inner - 18, 13), "small", 19, size=13) + 26
    y = max(y - 6, min_h - 52)  # 52 = chip row (22) + bottom padding (30)
    c.chips(x0, y, s["stack"], inner - 30)
    if s["url"]:
        c.arrow(HALF - x0 - 8, y + 15)
    else:
        c.tomb(HALF - x0, y + 16)
    c.h = y + 22 + 30
    return c


def p_systems(d, theme, n):
    s = d["systems"]
    c = Canvas(W, theme, s["title"])
    c.desc = "; ".join(f"{i['name']} ({i['lang']}): {i['detail']} {i['proof']}" for i in s["items"])
    y0 = header(c, n, s["title"]) + 40
    colw = (W - 2 * PAD - 40) / 2
    rows = [s["items"][0:2], s["items"][2:4]]
    y = y0
    for r, row in enumerate(rows):
        bottoms = []
        for col, it in enumerate(row):
            x = PAD + col * (colw + 40)
            c.text(x, y, it["name"], "h3", size=19)
            c.text(x + measure(it["name"], "h3", 19) + 12, y, it["lang"], "medium", size=12.5, color="accent")
            yy = c.lines(x, y + 26, wrap(it["detail"], "body", colw, 13.5), "body", 21, size=13.5)
            bottoms.append(yy)
        yb = max(bottoms) + 30
        for col, it in enumerate(row):
            x = PAD + col * (colw + 40)
            c.rect(x, yb - 9, 8, 8, "accent")
            c.text(x + 16, yb - 1, it["proof"], "mono", color="accent")
        if r == 0:
            c.line(PAD, yb + 22, W - PAD, yb + 22, dash="2 4")
        y = yb + 62
    c.h = y - 26
    return c


def p_maths(d, theme, n):
    s = d["maths"]
    c = Canvas(W, theme, s["title"])
    c.desc = "; ".join(f"{i['big']} {i['label']}: {i['sub']}" for i in s["items"])
    y = header(c, n, s["title"]) + 26
    c.h = stat_columns(c, s["items"], y, 4, big_size=30) + 30
    return c


def p_stack(d, theme, n):
    s = d["stack"]
    c = Canvas(W, theme, s["title"])
    c.desc = "; ".join(f"{g['name']}: {', '.join(g['items'])}" for g in s["groups"])
    y = header(c, n, s["title"]) + 28
    for g in s["groups"]:
        c.text(PAD, y + 15, g["name"], "caps")
        y = c.chips(PAD + 170, y, g["items"], W - 2 * PAD - 170) + 16
    c.h = y + 14
    return c


def p_side(d, theme, n):
    s = d["side"]
    c = Canvas(W, theme, f"{s['title']}: {s['name']}")
    c.desc = s["detail"]
    y = header(c, n, s["title"]) + 38
    c.text(PAD, y, s["name"], "h3", size=19)
    c.text(W - PAD - 14, y - 2, s["url"].replace("https://", ""), "mono", anchor="end", color="accent")
    c.arrow(W - PAD - 8, y)
    y = c.lines(PAD, y + 26, wrap(s["detail"], "body", W - 2 * PAD, 14), "body", 21, size=14)
    c.h = y + 30
    return c


def p_beyond(d, theme, n):
    s = d["beyond"]
    c = Canvas(W, theme, s["title"])
    c.desc = "; ".join(f"{i['name']}: {i['detail']}" for i in s["items"])
    y = header(c, n, s["title"]) + 40
    k = len(s["items"])
    colw = (W - 2 * PAD) / k
    for i, it in enumerate(s["items"]):
        x = PAD + i * colw + (16 if i else 0)
        if i:
            c.line(PAD + i * colw, y - 18, PAD + i * colw, y + 30, color="rule")
        c.text(x, y, it["name"], "rule", size=19, color="ink")
        c.lines(x, y + 22, wrap(it["detail"], "small", colw - 28), "small", 17)
    c.tomb(W - PAD, y + 56)
    c.h = y + 82
    return c


# --------------------------------------------------------------------------- build
def save(name: str, build) -> None:
    for theme in THEMES:
        c = build(theme)
        (ASSETS / f"{name}-{theme}.svg").write_text(c.svg(), encoding="utf-8")
    ALT[name] = (c.title + ". " + c.desc).strip()


ALT: dict[str, str] = {}


def picture(name: str, width: str = "100%") -> str:
    alt = escape(ALT[name], {'"': "&quot;"})
    return (
        f'<picture><source media="(prefers-color-scheme: dark)" srcset="{RAW_BASE}/{name}-dark.svg">'
        f'<img alt="{alt}" src="{RAW_BASE}/{name}-light.svg" width="{width}"></picture>'
    )


def linked(name: str, url: str, width: str = "100%") -> str:
    pic = picture(name, width)
    return f'<a href="{url}">{pic}</a>' if url else pic


def main() -> None:
    d = tomllib.loads((ROOT / "profile.toml").read_text(encoding="utf-8"))
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("*.svg"):
        old.unlink()

    save("hero", lambda t: p_hero(d, t))
    save("highlights", lambda t: p_highlights(d, t, 1))
    save("now", lambda t: p_now(d, t, 2))
    save("experience", lambda t: p_experience(d, t, 3))
    save("impact", lambda t: p_impact(d, t, 4))
    save("label-work", lambda t: p_label(t, 5, d["work"]["title"]))
    save("feature", lambda t: p_feature(d, t))
    cards = d["work"]["cards"]
    for a, b in zip(cards[0::2], cards[1::2]):
        h = max(card(a, "light").h, card(b, "light").h)
        for s in (a, b):
            save(f"card-{s['slug']}", lambda t, s=s: card(s, t, min_h=h))
    save("systems", lambda t: p_systems(d, t, 6))
    save("maths", lambda t: p_maths(d, t, 7))
    save("stack", lambda t: p_stack(d, t, 8))
    save("side", lambda t: p_side(d, t, 9))
    save("beyond", lambda t: p_beyond(d, t, 10))

    p = d["person"]
    gap = "\n\n"

    def para(html: str) -> str:
        return f"<p>{html}</p>"

    parts = [
        "<!-- Generated by tools/build.py from profile.toml. Edit those, not this file. -->",
        para(picture("hero")),
        f'<p><a href="{p["linkedin"]}">LinkedIn</a> &nbsp;·&nbsp; '
        f'<a href="mailto:{p["email"]}">{p["email"]}</a></p>',
        para(picture("highlights")),
        para(picture("now")),
        para(picture("experience")),
        para(picture("impact")),
        para(picture("label-work")),
        para(linked("feature", d["work"]["feature"]["url"])),
    ]
    for a, b in zip(cards[0::2], cards[1::2]):
        parts.append(
            "<p>"
            + linked(f"card-{a['slug']}", a["url"], "49%")
            + " "
            + linked(f"card-{b['slug']}", b["url"], "49%")
            + "</p>"
        )
    parts += [
        para(picture("systems")),
        para(picture("maths")),
        para(picture("stack")),
        para(linked("side", d["side"]["url"])),
        para(picture("beyond")),
    ]
    (ROOT / "README.md").write_text(gap.join(parts) + "\n", encoding="utf-8")
    total = sum(f.stat().st_size for f in ASSETS.glob("*.svg"))
    print(f"Built {len(list(ASSETS.glob('*.svg')))} SVGs ({total/1024:.0f} KB) and README.md")


if __name__ == "__main__":
    sys.exit(main())
