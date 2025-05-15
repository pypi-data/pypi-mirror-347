# fa2svg/converter.py

import re
from functools import lru_cache
import base64
import requests
from bs4 import BeautifulSoup
import cairosvg

# Font Awesome version and CDN base (jsDelivr)
FA_VERSION = "6.7.2"
FA_CDN_BASE = (
    f"https://cdn.jsdelivr.net/npm/"
    f"@fortawesome/fontawesome-free@{FA_VERSION}/svgs"
)

# Match any <i> or <span> whose class list contains 'fa-'
ICON_SELECTOR = "i[class*='fa-'], span[class*='fa-']"
# Map style-prefix to CDN folder
STYLE_MAP = {"fas": "solid", "far": "regular", "fab": "brands"}
# Regex to pull inline CSS props like 'font-size:24px;color:#f00;'
STYLE_PROP = re.compile(r"\s*([\w-]+)\s*:\s*([^;]+)\s*;?")

# Scale factor for higher resolution (pixel density)
IMAGE_SCALE = 10

@lru_cache(maxsize=256)
def _fetch_raw_svg(style_dir: str, icon_name: str) -> str:
    url = f"{FA_CDN_BASE}/{style_dir}/{icon_name}.svg"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def parse_css_size(size_str: str, parent_px: float=16.0) -> float:
    s = size_str.strip()
    try:
        if s.endswith("px"):
            return float(s[:-2])
        if s.endswith("em"):
            return float(s[:-2]) * parent_px
        if s.endswith("%"):
            return float(s[:-1]) / 100.0 * parent_px
        return float(s)
    except:
        return parent_px

def get_computed_font_size(el) -> float:
    DEFAULT = 16.0
    current = el
    while current:
        props = dict(STYLE_PROP.findall(current.get("style","")))
        if "font-size" in props:
            parent_px = get_computed_font_size(current.parent) if current.parent else DEFAULT
            return parse_css_size(props["font-size"], parent_px)
        current = current.parent
    return DEFAULT

def get_inherited_color(el) -> str:
    current = el
    while current:
        props = dict(STYLE_PROP.findall(current.get("style","")))
        if "color" in props:
            return props["color"].strip()
        current = current.parent
    return "#000"

def to_inline_png_img(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for el in soup.select(ICON_SELECTOR):
        classes = el.get("class", [])
        icon = next((c.split("fa-")[1]
                     for c in classes
                     if c.startswith("fa-") and c != "fa"),
                    None)
        if not icon:
            continue
        style_dir = next((STYLE_MAP[c] for c in classes if c in STYLE_MAP), "solid")

        # 1) compute desired pixel height & color
        size_px = get_computed_font_size(el)
        color = get_inherited_color(el)

        # 2) fetch the raw SVG text
        raw_svg = _fetch_raw_svg(style_dir, icon)

        # 3) strip width/height and inject fill + preserveAspectRatio
        svg_txt = re.sub(r'\s(width|height)="[^"]*"', '', raw_svg, flags=re.IGNORECASE)
        svg_txt = re.sub(
            r'<svg\b',
            f'<svg fill="{color}" preserveAspectRatio="xMidYMid meet"',
            svg_txt,
            count=1
        )

        # 4) pull viewBox for aspect
        m = re.search(r'viewBox="([\d.\s]+)"', svg_txt)
        if m:
            nums = [float(n) for n in m.group(1).split()]
            vb_w, vb_h = nums[2], nums[3]
            target_h = int(size_px)
            target_w = int(size_px * (vb_w / vb_h))
        else:
            target_w = target_h = int(size_px)

        # 5) render PNG at higher resolution
        png_bytes = cairosvg.svg2png(
            bytestring=svg_txt.encode("utf-8"),
            output_width=int(target_w * IMAGE_SCALE),
            output_height=int(target_h * IMAGE_SCALE)
        )
        b64 = base64.b64encode(png_bytes).decode("ascii")
        src = f"data:image/png;base64,{b64}"

        # 6) replace original tag with <img>, CSS scales it back to intended size
        img = soup.new_tag("img", src=src)
        img["style"] = f"height:{target_h}px;width:auto;vertical-align:-0.125em;"
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

