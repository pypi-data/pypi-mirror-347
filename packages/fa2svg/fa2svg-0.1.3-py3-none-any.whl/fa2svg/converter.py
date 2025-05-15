# fa2svg/converter.py

import re
import base64
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

# Font Awesome version and CDN base
FA_VERSION  = "6.7.2"
FA_CDN_BASE = (
    f"https://cdn.jsdelivr.net/npm/"
    f"@fortawesome/fontawesome-free@{FA_VERSION}/svgs"
)

ICON_SELECTOR = "i[class*='fa-'], span[class*='fa-']"
STYLE_MAP     = {"fas": "solid", "far": "regular", "fab": "brands"}
STYLE_PROP    = re.compile(r"\s*([\w-]+)\s*:\s*([^;]+)\s*;?")

@lru_cache(maxsize=256)
def _fetch_raw_svg(style_dir: str, icon_name: str) -> str:
    url = f"{FA_CDN_BASE}/{style_dir}/{icon_name}.svg"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def to_inline_svg_img(html: str) -> str:
    """
    Replace FA <i>/<span> with <img src="data:image/svg+xml;base64,...">
    preserving aspect ratio, color (baked), size, and baseline shift.
    """
    soup = BeautifulSoup(html, "lxml")

    for el in soup.select(ICON_SELECTOR):
        classes = el.get("class", [])
        icon    = next((c.split("fa-")[1]
                        for c in classes
                        if c.startswith("fa-") and c != "fa"),
                       None)
        if not icon:
            continue

        style_dir = next((STYLE_MAP[c] for c in classes if c in STYLE_MAP),
                         "solid")
        styles    = dict(STYLE_PROP.findall(el.get("style","")))
        size_css  = styles.get("font-size")  # e.g. "24px" or "1.5em"
        color     = styles.get("color")      # e.g. "#c60" or "red"

        # 1) fetch raw SVG and parse
        raw_svg = _fetch_raw_svg(style_dir, icon)
        svg_tag = BeautifulSoup(raw_svg, "lxml").find("svg")

        # 2) bake in fill
        svg_tag["fill"] = color or "#000"

        # 3) set SVG width/height attr if you like (not strictly required for <img>)
        #    but we'll rely on CSS on the <img> instead.

        # 4) stringify and base64-encode the SVG
        svg_bytes = str(svg_tag).encode("utf-8")
        b64 = base64.b64encode(svg_bytes).decode("ascii")
        data_uri = f"data:image/svg+xml;base64,{b64}"

        # 5) build an <img> to replace the <i>/<span>
        img = soup.new_tag("img", src=data_uri)

        # sizing: use the same CSS units you had (or fallback to 1em)
        w = size_css or "1em"
        h = size_css or "1em"
        img["style"] = f"width:{w};height:{h};vertical-align:-0.125em;"

        el.replace_with(img)

    return str(soup)
