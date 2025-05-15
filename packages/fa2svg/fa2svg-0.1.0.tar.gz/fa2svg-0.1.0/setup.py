from setuptools import setup, find_packages

setup(
    name="fa2svg",
    version="0.1.0",
    description="Convert Font Awesome HTML tags into inline SVG",
    author="meena-erian",
    url="https://github.com/meena-erian/fa2svg",
    project_urls={
        "Source": "https://github.com/meena-erian/fa2svg",
        "Issue Tracker": "https://github.com/meena-erian/fa2svg/issues",
    },
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "requests",
    ],
    python_requires=">=3.6",
)
