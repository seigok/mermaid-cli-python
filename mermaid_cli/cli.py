"""
Command-line interface for mermaid-cli

This module provides the command-line interface for the mermaid-cli tool.
It handles parsing command-line arguments and executing the renderer.

このモジュールはmermaid-cliツールのコマンドラインインターフェースを提供します。
コマンドライン引数の解析とレンダラーの実行を処理します。
"""

import asyncio
import json
import os
import sys
from typing import List, Optional

import click
from colorama import Fore, Style, init

from .renderer import render_mermaid_file
from .version import __version__

# Initialize colorama for cross-platform colored terminal output
# クロスプラットフォームの色付きターミナル出力のためにcoloramaを初期化
init()


def error(message):
    """
    Print an error message and exit.
    
    Args:
        message: Error message to display
        
    エラーメッセージを表示して終了します。
    
    引数:
        message: 表示するエラーメッセージ
    """
    click.echo(f"{Fore.RED}\n{message}\n{Style.RESET_ALL}", err=True)
    sys.exit(1)


def warn(message):
    """
    Print a warning message.
    
    Args:
        message: Warning message to display
        
    警告メッセージを表示します。
    
    引数:
        message: 表示する警告メッセージ
    """
    click.echo(f"{Fore.YELLOW}\n{message}\n{Style.RESET_ALL}", err=True)


def check_config_file(file_path):
    """
    Check if a config file exists.
    
    Args:
        file_path: Path to the configuration file
        
    設定ファイルが存在するかどうかを確認します。
    
    引数:
        file_path: 設定ファイルへのパス
    """
    if not os.path.exists(file_path):
        error(f'Configuration file "{file_path}" doesn\'t exist')


@click.command()
@click.version_option(__version__)
@click.option('-t', '--theme', type=click.Choice(['default', 'forest', 'dark', 'neutral']), default='default',
              help='Theme of the chart')
@click.option('-w', '--width', type=int, default=800, help='Width of the page')
@click.option('-H', '--height', type=int, default=600, help='Height of the page')
@click.option('-i', '--input', help='Input mermaid file. Files ending in .md will be treated as Markdown and all charts '
                                    '(e.g. ```mermaid (...) or :::mermaid (...):::) will be extracted and generated. '
                                    'Use `-` to read from stdin.')
@click.option('-o', '--output', help='Output file. It should be either md, svg, png, pdf or use `-` to output to stdout. '
                                    'Optional. Default: input + ".svg"')
@click.option('-e', '--output-format', type=click.Choice(['svg', 'png', 'pdf']), default=None,
              help='Output format for the generated image.')
@click.option('-b', '--background-color', default='white',
              help='Background color for pngs/svgs (not pdfs). Example: transparent, red, \'#F0F0F0\'.')
@click.option('-c', '--config-file', help='JSON configuration file for mermaid.')
@click.option('-C', '--css-file', help='CSS file for the page.')
@click.option('-I', '--svg-id', help='The id attribute for the SVG element to be rendered.')
@click.option('-s', '--scale', type=int, default=1, help='Playwright scale factor')
@click.option('-f', '--pdf-fit', is_flag=True, help='Scale PDF to fit chart')
@click.option('-q', '--quiet', is_flag=True, help='Suppress log output')
@click.option('-p', '--playwright-config-file', help='JSON configuration file for playwright.')
@click.option('--icon-packs', multiple=True, help='Icon packs to use, e.g. @iconify-json/logos')
def main(theme, width, height, input, output, output_format, background_color, config_file, css_file, svg_id,
         playwright_config_file, scale, pdf_fit, quiet, icon_packs):
    """
    Command-line interface for mermaid.
    
    This tool renders Mermaid diagrams to various formats.
    
    mermaidのコマンドラインインターフェース。
    
    このツールはMermaid図を様々な形式に描画します。
    """
    # Check input file
    # 入力ファイルをチェック
    if not input:
        warn('No input file specified, reading from stdin. '
             'If you want to specify an input file, please use `-i <input>.` '
             'You can use `-i -` to read from stdin and to suppress this warning.')
    elif input == '-':
        # `--input -` means read from stdin, but suppress the above warning
        # `--input -` は標準入力から読み込むが、上記の警告を抑制する
        input = None
    elif not os.path.exists(input):
        error(f'Input file "{input}" doesn\'t exist')

    # Check output file
    # 出力ファイルをチェック
    if not output:
        # if an input file is defined, it should take precedence, otherwise, input is
        # coming from stdin and just name the file out.svg, if it hasn't been
        # specified with the '-o' option
        if output_format:
            output = f"{input}.{output_format}" if input else f"out.{output_format}"
        else:
            output = f"{input}.svg" if input else "out.svg"
    elif output == '-':
        # `--output -` means write to stdout.
        # `--output -` は標準出力に書き込むことを意味する
        output = '/dev/stdout'
        quiet = True

        if not output_format:
            output_format = 'svg'
            warn('No output format specified, using svg. '
                 'If you want to specify an output format and suppress this warning, '
                 'please use `-e <format>.` ')
    elif not output.lower().endswith(('.svg', '.png', '.pdf', '.md', '.markdown')):
        error('Output file must end with ".md"/".markdown", ".svg", ".png" or ".pdf"')

    # Check if output directory exists
    # 出力ディレクトリが存在するかチェック
    output_dir = os.path.dirname(output) or '.'
    if output != '/dev/stdout' and not os.path.exists(output_dir):
        error(f'Output directory "{output_dir}/" doesn\'t exist')

    # Load mermaid configuration
    # Mermaid設定を読み込む
    mermaid_config = {'theme': theme}
    if config_file:
        check_config_file(config_file)
        with open(config_file, 'r') as f:
            mermaid_config.update(json.load(f))

    # Load playwright configuration
    # Playwright設定を読み込む
    playwright_config = {
        'headless': True
    }
    if playwright_config_file:
        check_config_file(playwright_config_file)
        with open(playwright_config_file, 'r') as f:
            playwright_config.update(json.load(f))

    # Load CSS file if specified
    # 指定されている場合はCSSファイルを読み込む
    css = None
    if css_file:
        if not os.path.exists(css_file):
            error(f'CSS file "{css_file}" doesn\'t exist')
        with open(css_file, 'r') as f:
            css = f.read()

    # Run the renderer
    # レンダラーを実行
    try:
        asyncio.run(render_mermaid_file(
            input_file=input,
            output_file=output,
            output_format=output_format,
            playwright_config=playwright_config,
            quiet=quiet,
            viewport={'width': width, 'height': height, 'deviceScaleFactor': scale},
            background_color=background_color,
            mermaid_config=mermaid_config,
            css=css,
            pdf_fit=pdf_fit,
            svg_id=svg_id,
            icon_packs=list(icon_packs)
        ))
    except Exception as e:
        error(str(e))


if __name__ == '__main__':
    main()
