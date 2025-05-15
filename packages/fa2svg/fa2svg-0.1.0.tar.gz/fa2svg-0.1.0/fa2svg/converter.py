import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

# Font Awesome version and CDN base (jsDelivr)
FA_VERSION = "6.7.2"
FA_CDN_BASE = f"https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@{FA_VERSION}/svgs"

# Selectors and mappings
# Match any <i> or <span> with a class containing 'fa-'
ICON_SELECTOR = "i[class*='fa-'], span[class*='fa-']"
STYLE_MAP = {"fas": "solid", "far": "regular", "fab": "brands"}
# Inline-style extraction regex (e.g. "font-size:24px;color:#f00;")
STYLE_PROP = re.compile(r"\s*([\w-]+)\s*:\s*([^;]+)\s*;?")

@lru_cache(maxsize=256)
def _fetch_raw_svg(style_dir: str, icon_name: str) -> str:
    """Download the SVG text from jsDelivr and return it."""
    url = f"{FA_CDN_BASE}/{style_dir}/{icon_name}.svg"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def to_inline_svg(html: str) -> str:
    """Replace Font Awesome <i> or <span> tags with inline SVG preserving size & color."""
    soup = BeautifulSoup(html, "lxml")

    for el in soup.select(ICON_SELECTOR):
        classes = el.get("class", [])
        # extract icon slug from class list (e.g. "fa-mug-saucer" → "mug-saucer")
        icon = next((c.split("fa-")[1] for c in classes if c.startswith("fa-") and c != "fa"), None)
        if not icon:
            continue

        # determine style folder (solid/regular/brands)
        style_dir = next((STYLE_MAP[c] for c in classes if c in STYLE_MAP), "solid")

        # parse inline styles, if any
        styles = dict(STYLE_PROP.findall(el.get("style", "")))
        size = styles.get("font-size")
        color = styles.get("color")

        # fetch and parse the raw SVG
        raw_svg = _fetch_raw_svg(style_dir, icon)
        svg = BeautifulSoup(raw_svg, "lxml").find("svg")

        # apply inline attributes
        if size:
            svg["width"] = size
            svg["height"] = size
        if color:
            svg["fill"] = color

        # replace the original <i> or <span> with the SVG element
        el.replace_with(svg)

    return str(soup)
