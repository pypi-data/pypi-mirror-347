# fa2svg

A small Python package that converts Font Awesome `<i>`/`<span>` tags into **embedded SVG images** (`<img src="data:image/svg+xml;base64,…">`) so you can safely use FA icons in emails (or any HTML source that strips out inline `<svg>`).

---

## Installation

```bash
pip install fa2svg
````

Or for local development:

```bash
git clone https://github.com/meena-erian/fa2svg.git
cd fa2svg
pip install -e .
```

---

## Upload to PyPI

Make sure your `.pypirc` is set up as described in the project docs, then:

```bash
# from project root
twine upload --config-file "./.pypirc" dist/*
```

---

## Usage

```python
from fa2svg.converter import to_inline_svg_img

html = '''
  <p>
    Coffee time:
    <i class="fas fa-mug-saucer"
       style="font-size:64px;color:#c60">
    </i>
    and stars:
    <span class="far fa-star"
          style="font-size:48px;color:gold">
    </span>
  </p>
'''

converted = to_inline_svg_img(html)
print(converted)
# => all <i>/<span> icons replaced with <img src="data:image/svg+xml;base64,…" …
#    preserving exact size, color, aspect ratio & baseline alignment
```

---

## API

* **`to_inline_svg_img(html: str) → str`**
  Fetches the correct FA SVG, bakes in your inline `font-size` and `color` (or defaults to `1em` & current text color), and outputs a `<img>` tag with a base64-encoded SVG data URI, plus the proper `width`, `height` and `vertical-align` CSS.

---

## Contributing

1. Fork the repo
2. Create a topic branch
3. Commit your changes & push
4. Open a Pull Request

Issues and PRs are very welcome!
