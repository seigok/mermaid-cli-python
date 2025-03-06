"""
Setup script for the mermaid-cli package

This script configures the package for distribution.

mermaid-cliパッケージのセットアップスクリプト

このスクリプトはパッケージの配布のための設定を行います。
"""

from setuptools import setup, find_packages
from mermaid_cli.version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mermaid_cli",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "playwright>=1.30.0",
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "mmdc=mermaid_cli.cli:main",
        ],
    },
    package_data={
        "mermaid_cli": ["templates/*.html"],
    },
    python_requires=">=3.7",
    description="Command-line interface and Python library for mermaid diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mermaid CLI Python Team",
    author_email="seigo.kawamura@gmail.com",
    url="https://github.com/seigok/mermaid-cli-python",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
    ],
    keywords="mermaid, diagram, chart, markdown, documentation, cli",
)
