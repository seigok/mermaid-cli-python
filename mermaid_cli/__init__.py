"""
Mermaid CLI - A command-line interface for mermaid diagrams

This package provides tools to render Mermaid diagrams from the command line
or as a Python library. It supports rendering to SVG, PNG, and PDF formats,
as well as processing Markdown files with embedded Mermaid diagrams.

Mermaid CLI - Mermaid図のためのコマンドラインインターフェース

このパッケージはコマンドラインまたはPythonライブラリとしてMermaid図を描画するツールを提供します。
SVG、PNG、PDF形式での描画や、Mermaid図が埋め込まれたMarkdownファイルの処理をサポートしています。
"""

from .version import __version__
from .renderer import render_mermaid, render_mermaid_file, render_mermaid_file_sync

__all__ = ["__version__", "render_mermaid", "render_mermaid_file", "render_mermaid_file_sync"]
