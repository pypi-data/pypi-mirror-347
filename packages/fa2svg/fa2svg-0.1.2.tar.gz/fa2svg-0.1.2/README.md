
# fa2svg

A Python package to convert Font Awesome `<i>`/`<span>` tags into inline SVG elements. It was specifically made so you can use Font Awesome in emails by passing the email body through this converter before sending.

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

# Upload
```bash
twine upload --config-file "./.pypirc" dist\*
```

## Usage

```python
from fa2svg.converter import to_inline_svg

html = '<p>Icon: <i class="fas fa-mug-saucer" style="font-size:64px;color:#c60"></i></p>'
print(to_inline_svg(html))
```

## Contributing

Fork the repo, open issues, submit pull requests!

