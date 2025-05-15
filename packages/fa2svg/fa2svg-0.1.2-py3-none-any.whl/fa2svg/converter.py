# fa2svg/converter.py

import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

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

@lru_cache(maxsize=256)
def _fetch_raw_svg(style_dir: str, icon_name: str) -> str:
    """Download the SVG text from jsDelivr and return it."""
    url = f"{FA_CDN_BASE}/{style_dir}/{icon_name}.svg"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

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
