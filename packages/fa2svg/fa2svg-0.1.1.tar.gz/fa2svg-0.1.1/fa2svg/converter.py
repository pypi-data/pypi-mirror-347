import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

# Font Awesome version and CDN base (jsDelivr)
FA_VERSION = "6.7.2"
FA_CDN_BASE  = f"https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@{FA_VERSION}/svgs"

# Match any <i> or <span> with a class containing 'fa-'
ICON_SELECTOR = "i[class*='fa-'], span[class*='fa-']"
STYLE_MAP     = {"fas": "solid", "far": "regular", "fab": "brands"}
STYLE_PROP    = re.compile(r"\s*([\w-]+)\s*:\s*([^;]+)\s*;?")

@lru_cache(maxsize=256)
def _fetch_raw_svg(style_dir: str, icon_name: str) -> str:
    """Download the SVG text from jsDelivr and return it."""
    url = f"{FA_CDN_BASE}/{style_dir}/{icon_name}.svg"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def to_inline_svg(html: str) -> str:
    """Replace Font Awesome <i>/<span> tags with inline SVG preserving appearance."""
    soup = BeautifulSoup(html, "lxml")

    for el in soup.select(ICON_SELECTOR):
        classes = el.get("class", [])
        icon    = next((c.split("fa-")[1] for c in classes if c.startswith("fa-") and c != "fa"), None)
        if not icon:
            continue

        style_dir = next((STYLE_MAP[c] for c in classes if c in STYLE_MAP), "solid")

        # grab any inline override
        styles = dict(STYLE_PROP.findall(el.get("style", "")))
        size   = styles.get("font-size")  # e.g. "24px" or "1.5em"
        color  = styles.get("color")      # e.g. "#c60" or "red"

        raw_svg = _fetch_raw_svg(style_dir, icon)
        svg     = BeautifulSoup(raw_svg, "lxml").find("svg")

        # SIZE: explicit px/em or fallback to 1em
        if size:
            svg["width"]  = size
            svg["height"] = size
        else:
            svg["width"]  = "1em"
            svg["height"] = "1em"

        # COLOR: explicit or inherited
        if color:
            svg["fill"] = color
        else:
            svg["fill"] = "currentColor"

        # replace the original tag
        el.replace_with(svg)

    return str(soup)
