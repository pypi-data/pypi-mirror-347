from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

_locals = {}
with open("glitch_forge/_version.py") as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

setup(
    name="glitch_forge",
    version=version,
    description="Auto-generate PyQt6 GUIs from class parameters for quick tools and prototyping.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lukas Ukelis",
    author_email="lukasukelis@gmail.com",
    project_urls={
        "Source": "https://github.com/LukasUkelis/GlitchForge",
        "Issues": "https://github.com/LukasUkelis/GlitchForge/issues",
    },
    packages=["glitch_forge"],
    python_requires=">=3.10",
    install_requires=["PyQt6>=6.8.1"],
)
