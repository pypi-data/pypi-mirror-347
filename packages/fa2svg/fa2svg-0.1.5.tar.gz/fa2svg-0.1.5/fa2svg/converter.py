# fa2svg/converter.py

import re
from functools import lru_cache
import base64
import requests
import difflib
from functools import lru_cache
from bs4 import BeautifulSoup
import cairosvg

from .constants import VALID_FA_ICONS

# Font Awesome version and CDN base (jsDelivr)
FA_VERSION = "6.7.2"
FA_CDN_BASE = (
    f"https://cdn.jsdelivr.net/npm/"
    f"@fortawesome/fontawesome-free@{FA_VERSION}/svgs"
)

# Select any <i> or <span> with a 'fa-' class
ICON_SELECTOR = "i[class*='fa-'], span[class*='fa-']"

# Map prefix to sub-folder in CDN
STYLE_MAP = {"fas": "solid", "far": "regular", "fab": "brands"}

# Regex for inline CSS props (e.g. font-size, color)
STYLE_PROP = re.compile(r"\s*([\w-]+)\s*:\s*([^;]+)\s*;?")

# Render at 10× pixel density for crispness
IMAGE_SCALE = 10


@lru_cache(maxsize=256)
def _fetch_raw_svg(style_dir: str, icon_name: str) -> str:
    """
    Download (and cache) the raw SVG text for a given style/icon.
    Raises on 404 or other HTTP errors, which will be caught by caller.
    """
    url = f"{FA_CDN_BASE}/{style_dir}/{icon_name}.svg"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


@lru_cache(maxsize=256)
def _render_png_data_uri(style_dir: str, icon_name: str, size: int, color: str) -> str:
    """
    Take raw SVG, inject fill + aspect, render to PNG at high DPI,
    and return a base64 data URI. Cached by (style,icon,size,color).
    """
    raw_svg = _fetch_raw_svg(style_dir, icon_name)

    # strip any width/height attributes
    svg_txt = re.sub(
        r'\s(width|height)="[^"]*"',
        "",
        raw_svg,
        flags=re.IGNORECASE
    )

    # inject fill color + preserveAspectRatio
    svg_txt = re.sub(
        r"<svg\b",
        f'<svg fill="{color}" preserveAspectRatio="xMidYMid meet"',
        svg_txt,
        count=1
    )

    # extract viewBox to compute target width
    match = re.search(r'viewBox="([\d.\s]+)"', svg_txt)
    if match:
        nums = [float(n) for n in match.group(1).split()]
        vb_w, vb_h = nums[2], nums[3]
        target_w = int(size * (vb_w / vb_h))
    else:
        target_w = size

    # render PNG at IMAGE_SCALE×
    png_bytes = cairosvg.svg2png(
        bytestring=svg_txt.encode("utf-8"),
        output_width=target_w * IMAGE_SCALE,
        output_height=size * IMAGE_SCALE
    )
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f"data:image/png;base64,{b64}"


def parse_css_size(size_str: str, parent_px: float = 16.0) -> float:
    """
    Convert a CSS size string (px, em, %) to absolute px.
    Defaults to parent_px if parsing fails.
    """
    s = size_str.strip()
    try:
        if s.endswith("px"):
            return float(s[:-2])
        if s.endswith("em"):
            return float(s[:-2]) * parent_px
        if s.endswith("%"):
            return float(s[:-1]) / 100.0 * parent_px
        return float(s)
    except Exception:
        return parent_px


def get_computed_font_size(el) -> float:
    """
    Walk up the tree to find a 'font-size' style and compute
    its absolute px value (default 16px).
    """
    DEFAULT = 16.0
    current = el
    while current:
        props = dict(STYLE_PROP.findall(current.get("style", "")))
        if "font-size" in props:
            parent = get_computed_font_size(current.parent) if current.parent else DEFAULT
            return parse_css_size(props["font-size"], parent)
        current = current.parent
    return DEFAULT


def get_inherited_color(el) -> str:
    """
    Walk up the tree to find a 'color' style. Defaults to black.
    """
    current = el
    while current:
        props = dict(STYLE_PROP.findall(current.get("style", "")))
        if "color" in props:
            return props["color"].strip()
        current = current.parent
    return "#000"


def to_inline_png_img(html: str) -> str:
    """
    Convert all <i>/<span> FontAwesome tags in `html` into
    high-DPI PNG data-URIs wrapped in <img> tags.

    - Skips any icon not in VALID_FA_ICONS (per‐style).
    - Fuzzy‐matches typos to the closest valid icon (cutoff=0.6).
    - Gracefully skips on network or rendering errors.
    """
    soup = BeautifulSoup(html, "lxml")

    for el in soup.select(ICON_SELECTOR):
        classes = el.get("class", [])
        # find the 'fa-xyz' icon name
        icon = next(
            (c.split("fa-")[1] for c in classes if c.startswith("fa-") and c != "fa"),
            None
        )
        if not icon:
            continue

        # determine style folder (solid/regular/brands)
        style_dir = next((STYLE_MAP[c] for c in classes if c in STYLE_MAP), "solid")

        # fetch the correct set of valid icons for this style
        allowed = VALID_FA_ICONS.get(style_dir, set())

        # if not exact, try fuzzy match
        if icon not in allowed:
            match = difflib.get_close_matches(icon, allowed, n=1, cutoff=0.6)
            if match:
                icon = match[0]
            else:
                continue  # skip entirely

        # compute display size & fill color
        size_px = int(get_computed_font_size(el))
        color = get_inherited_color(el)

        # render PNG data URI (skip on any exception)
        try:
            data_uri = _render_png_data_uri(style_dir, icon, size_px, color)
        except Exception:
            continue

        # replace <i>/<span> with <img>
        img = soup.new_tag("img", src=data_uri)
        img["style"] = f"height:{size_px}px;width:auto;vertical-align:-0.125em;"
        el.replace_with(img)

    return str(soup)



def to_inline_svg(html: str) -> str:
    """Replace Font Awesome <i>/<span> tags with inline SVG preserving CSS-like sizing/color."""
    soup = BeautifulSoup(html, "lxml")

    for el in soup.select(ICON_SELECTOR):
        classes = el.get("class", [])
        # find the 'fa-xyz' part
        icon = next(
            (c.split("fa-")[1] for c in classes if c.startswith("fa-") and c != "fa"),
            None
        )
        if not icon:
            continue

        # pick solid/regular/brands
        style_dir = next((STYLE_MAP[c] for c in classes if c in STYLE_MAP), "solid")

        # parse any inline overrides
        styles = dict(STYLE_PROP.findall(el.get("style", "")))
        size  = styles.get("font-size")  # e.g. "1.5em" or "24px"
        color = styles.get("color")      # e.g. "#c60" or "red"

        # fetch and parse the SVG
        raw_svg = _fetch_raw_svg(style_dir, icon)
        svg     = BeautifulSoup(raw_svg, "lxml").find("svg")

        # extract viewBox dimensions for aspect ratio
        vb = svg.get("viewBox", "").split()
        if len(vb) == 4:
            vb_w, vb_h = float(vb[2]), float(vb[3])
            aspect = vb_w / vb_h
        else:
            aspect = 1.0

        # SIZE: if override, honor it; else use height=1em & proportional width
        if size:
            svg["width"]  = size
            svg["height"] = size
        else:
            svg["height"] = "1em"
            svg["width"]  = f"{aspect:.3f}em"

        # COLOR: override or inherit
        svg["fill"] = color if color else "currentColor"

        # VERTICAL ALIGN: mimic FA's -0.125em baseline shift
        existing_style = svg.get("style", "").rstrip(";")
        svg["style"] = (
            (existing_style + ";" if existing_style else "")
            + "vertical-align:-0.125em"
        )

        # replace the original tag with our enriched SVG
        el.replace_with(svg)

    return str(soup)

