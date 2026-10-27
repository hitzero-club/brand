"""Build the HitZero logo set (SVG) from geometry and the Sora font.

Usage (from the brand repo root):
    uv run --no-project --with shapely --with fonttools --with uharfbuzz \
        python source/build_logo.py

Writes assets/logo/*.svg. Sora (SIL OFL 1.1) is downloaded into source/.cache/ on first run.
PNG exports are rendered from these SVGs; see README.md.
"""

import io
import pathlib
import urllib.request

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'logo'
CACHE = ROOT / 'source' / '.cache'
SORA_URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/sora/Sora%5Bwght%5D.ttf'

# Brand tokens (index.html :root). CLUB_DARK is the platform's dark-mode primary (6.6:1 on black).
INK = '#0A0A0A'        # hz-black
WHITE = '#FFFFFF'
BLUE = '#0060B0'       # hz-blue
CLUB_DARK = '#1A98FF'  # primary, dark theme
RED = '#C82020'        # hz-red

# ---------------------------------------------------------------- the HZ mark
# Two rivals split by one diagonal slash. Units: H cap height 213.
R = 5          # outer corner radius
GAP = 6.5      # width of the slash


def cut_x(y):
    return 198 - 0.57 * (y - 120)


def _rounded(g):
    return g.buffer(-R, join_style=1).buffer(R, join_style=1)


_left = Polygon([(-100, -100), (cut_x(-100), -100), (cut_x(500), 500), (-100, 500)])
_right = Polygon([(cut_x(-100), -100), (600, -100), (600, 500), (cut_x(500), 500)])
_slash = LineString([(cut_x(-100), -100), (cut_x(500), 500)]).buffer(GAP / 2, cap_style=2)

# H: stems and crossbar; below the crossbar its right leg becomes a blade.
_H = unary_union([
    _rounded(unary_union([box(42, 40, 84, 254), box(80, 130, 190, 165), box(148, 40, 190, 170)])),
    Polygon([(148, 160), (215, 160), (121, 252), (146, 190)]),
])
# Z: dropped below the H; its sliced corner rises along the slash as a spike.
_Z = unary_union([
    _rounded(unary_union([
        box(185, 86, 309, 126),
        Polygon([(263, 120), (309, 120), (219, 264), (173, 264)]),
        box(172, 262, 311, 300),
    ])),
    Polygon([(243, 42), (226, 92), (195, 92)]),
])
H_SIDE = _H.intersection(_left).difference(_slash)
Z_SIDE = _Z.intersection(_right).difference(_slash)
SPIKE = Z_SIDE.intersection(box(0, 0, 600, 86))
Z_BODY = Z_SIDE.difference(box(0, 0, 600, 86))
MARK_BOX = (40, 40, 313, 300)


def _d(geom):
    out = []
    for p in getattr(geom, 'geoms', [geom]):
        if p.geom_type != 'Polygon':
            continue
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)[:-1]
            out.append('M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z')
    return ' '.join(out)


def mark(fg, tip):
    """The mark's paths in MARK_BOX units. tip=None draws it in one color."""
    if tip is None:
        return f'<path d="{_d(H_SIDE)}" fill="{fg}"/><path d="{_d(Z_SIDE)}" fill="{fg}"/>'
    return (f'<path d="{_d(H_SIDE)}" fill="{fg}"/><path d="{_d(Z_BODY)}" fill="{fg}"/>'
            f'<path d="{_d(SPIKE)}" fill="{tip}"/>')


def place_mark(x, y, height, fg, tip):
    x0, y0, x1, y1 = MARK_BOX
    s = height / (y1 - y0)
    g = f'<g transform="translate({x - x0 * s:.2f} {y - y0 * s:.2f}) scale({s:.5f})">{mark(fg, tip)}</g>'
    return g, (x1 - x0) * s


# ---------------------------------------------------------------- the wordmark
def _font():
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / 'Sora.ttf'
    if not path.exists():
        urllib.request.urlretrieve(SORA_URL, path)
    tt = instantiateVariableFont(TTFont(path), {'wght': 800})
    buf = io.BytesIO()
    tt.save(buf)
    return tt, hb.Font(hb.Face(buf.getvalue()))


TT, HBF = _font()
GLYPHS = TT.getGlyphSet()
ORDER = TT.getGlyphOrder()
CAP = TT['OS/2'].sCapHeight


def text(t, x, baseline, cap_height, track=0.0):
    """Outline `t` with its cap height = cap_height; returns (path d, end x)."""
    s = cap_height / CAP
    buf = hb.Buffer()
    buf.add_str(t)
    buf.guess_segment_properties()
    hb.shape(HBF, buf, {'kern': True})
    parts = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(GLYPHS)
        GLYPHS[ORDER[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, baseline)))
        parts.append(pen.getCommands())
        x += pos.x_advance * s + track
    return ' '.join(parts), x


def wordmark(x, baseline, cap_height, fg, club):
    word, end = text('HITZERO', x, baseline, cap_height, track=cap_height * 0.05)
    small = cap_height * 0.36
    club_w = text('.club', 0, 0, small)[1]
    dot, _ = text('.club', end - club_w, baseline + cap_height * 0.58, small)
    return f'<path d="{word}" fill="{fg}"/><path d="{dot}" fill="{club}"/>', end


# ---------------------------------------------------------------- files
def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.0f} {h:.0f}">\n<title>{title}</title>\n{body}\n</svg>\n')


def lockup(fg, club, tip, bg=None):
    pad, h = 16, 160
    m, w = place_mark(pad, pad, h, fg, tip)
    cap = h * 0.36
    wm, end = wordmark(pad + w + h * 0.22, pad + h * 0.62, cap, fg, club)
    W, H = end + pad, h + 2 * pad
    back = f'<rect width="{W:.0f}" height="{H:.0f}" fill="{bg}"/>' if bg else ''
    return W, H, back + m + wm


def icon(size, bg, fg, tip, radius):
    m, w = place_mark(0, 0, size * 0.56, fg, tip)
    rect = f'<rect width="{size}" height="{size}" rx="{radius:.1f}" fill="{bg}"/>'
    return rect + f'<g transform="translate({(size - w) / 2:.2f} {size * 0.22:.2f})">{m}</g>'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = MARK_BOX
    mw, mh = x1 - x0 + 16, y1 - y0 + 16
    files = {
        'hitzero-mark.svg': svg(mw, mh, place_mark(8, 8, y1 - y0, INK, RED)[0], 'HitZero mark'),
        'hitzero-mark-dark.svg': svg(mw, mh, place_mark(8, 8, y1 - y0, WHITE, RED)[0], 'HitZero mark, dark'),
        'hitzero-mark-mono.svg': svg(mw, mh, place_mark(8, 8, y1 - y0, INK, None)[0], 'HitZero mark, one color'),
        'hitzero-app-icon.svg': svg(1024, 1024, icon(1024, INK, WHITE, RED, 0), 'HitZero app icon'),
        'hitzero-favicon.svg': svg(64, 64, icon(64, INK, WHITE, RED, 14), 'HitZero favicon'),
    }
    for name, args in {
        'hitzero-logo.svg': (INK, BLUE, RED),
        'hitzero-logo-dark.svg': (WHITE, CLUB_DARK, RED),
        'hitzero-logo-mono.svg': (INK, INK, None),
    }.items():
        W, H, body = lockup(*args)
        files[name] = svg(W, H, body, 'HitZero logo')
    word, end = wordmark(16, 16 + 96, 96, INK, BLUE)
    files['hitzero-wordmark.svg'] = svg(end + 16, 16 + 96 + 96 * 0.58 + 16, word, 'HitZero wordmark')
    for name, content in files.items():
        (OUT / name).write_text(content)
        print('wrote', (OUT / name).relative_to(ROOT))


if __name__ == '__main__':
    main()
