from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="tframex",
    version="0.1.2",  # or whatever your new version is
    description="Framework for building agent-based flows and patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",  # This tells PyPI to render markdown
    packages=find_packages(),  # auto-discovers tframex/
)
