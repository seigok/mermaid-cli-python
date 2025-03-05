"""
Mermaid diagram renderer using playwright

This module provides functionality to render Mermaid diagrams using Playwright.
It supports rendering to SVG, PNG, and PDF formats.

このモジュールはPlaywrightを使用してMermaid図を描画する機能を提供します。
SVG、PNG、PDFフォーマットでの出力をサポートしています。
"""

import asyncio
import json
import math
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

from playwright.async_api import async_playwright

# Path to the HTML template
# HTMLテンプレートへのパス
TEMPLATE_PATH = Path(__file__).parent / "templates" / "index.html"


async def render_mermaid(
    definition: str,
    output_format: str = "svg",
    viewport: Dict[str, int] = None,
    background_color: str = "white",
    mermaid_config: Dict[str, Any] = None,
    css: str = None,
    pdf_fit: bool = False,
    svg_id: str = None,
    icon_packs: List[str] = None,
    playwright_config: Dict[str, Any] = None,
) -> Tuple[Optional[str], Optional[str], bytes]:
    """
    Render a mermaid diagram.

    Args:
        definition: Mermaid diagram definition
        output_format: Output format (svg, png, pdf)
        viewport: Viewport dimensions (width, height, deviceScaleFactor)
        background_color: Background color
        mermaid_config: Mermaid configuration
        css: Custom CSS
        pdf_fit: Scale PDF to fit chart
        svg_id: ID attribute for the SVG element
        icon_packs: Icon packages to use
        playwright_config: Browser configuration

    Returns:
        Tuple of (title, description, data)

    Mermaid図を描画します。

    引数:
        definition: Mermaid図の定義
        output_format: 出力形式（svg、png、pdf）
        viewport: ビューポートの寸法（幅、高さ、デバイススケールファクター）
        background_color: 背景色
        mermaid_config: Mermaidの設定
        css: カスタムCSS
        pdf_fit: PDFをチャートに合わせてスケーリング
        svg_id: SVG要素のID属性
        icon_packs: 使用するアイコンパッケージ
        playwright_config: ブラウザ設定

    戻り値:
        (タイトル、説明、データ)のタプル
    """
    # Set default values for optional parameters
    # オプションパラメータのデフォルト値を設定
    if viewport is None:
        viewport = {"width": 800, "height": 600, "deviceScaleFactor": 1}
    
    if mermaid_config is None:
        mermaid_config = {}
    
    if icon_packs is None:
        icon_packs = []
    
    if playwright_config is None:
        playwright_config = {}
    
    # Extract browser options from playwright_config
    # playwright_configからブラウザオプションを抽出
    browser_options = {}
    if "headless" in playwright_config:
        browser_options["headless"] = playwright_config["headless"]
    
    async with async_playwright() as p:
        # Launch browser
        # ブラウザを起動
        browser = await p.chromium.launch(**browser_options)
        
        try:
            # Create a new page with specified viewport
            # 指定されたビューポートで新しいページを作成
            page = await browser.new_page(viewport=viewport)
            
            # Set up console logging - use await to properly handle the coroutine
            # コンソールログの設定 - コルーチンを適切に処理するためにawaitを使用
            async def log_console(msg):
                print(f"Browser console: {msg.text}")
            
            page.on('console', lambda msg: asyncio.create_task(log_console(msg)))
            
            # Load the template
            # テンプレートを読み込む
            await page.goto(f"file://{TEMPLATE_PATH.absolute()}")
            
            # Set background color
            # 背景色を設定
            await page.evaluate("document.body.style.background = '" + background_color + "'")
            
            # Set variables in the page context
            # ページコンテキストに変数を設定
            await page.evaluate("window.mermaidDefinition = " + json.dumps(definition))
            await page.evaluate("window.mermaidConfig = " + json.dumps(mermaid_config))
            await page.evaluate("window.cssContent = " + json.dumps(css if css else ""))
            await page.evaluate("window.bgColor = " + json.dumps(background_color))
            await page.evaluate("window.svgId = " + json.dumps(svg_id if svg_id else ""))
            await page.evaluate("window.iconPacks = " + json.dumps(icon_packs))
            
            # Execute the rendering
            # 描画を実行
            result = await page.evaluate("""
            async () => {
                const definition = window.mermaidDefinition;
                const mermaidConfig = window.mermaidConfig;
                const css = window.cssContent;
                const backgroundColor = window.bgColor;
                const svgId = window.svgId;
                const iconPacks = window.iconPacks;
                
                // Wait for fonts to load
                // フォントの読み込みを待つ
                await Promise.all(Array.from(document.fonts, (font) => font.load()));
                
                // Initialize mermaid
                // mermaidを初期化
                mermaid.registerExternalDiagrams([window['mermaid-zenuml']]);
                
                // Register icon packs if available
                // アイコンパックが利用可能な場合は登録
                if (iconPacks && iconPacks.length > 0) {
                    mermaid.registerIconPacks(
                        iconPacks.map((icon) => ({
                            name: icon.split('/')[1],
                            loader: () =>
                                fetch(`https://unpkg.com/${icon}/icons.json`)
                                    .then((res) => res.json())
                                    .catch(() => console.error(`Failed to fetch icon: ${icon}`))
                        }))
                    );
                }
                
                // Initialize mermaid with proper theme handling
                // 適切なテーマ処理でmermaidを初期化
                const config = { startOnLoad: false, ...mermaidConfig };
                
                // Add theme class to the container if theme is specified
                // テーマが指定されている場合、コンテナにテーマクラスを追加
                const container = document.getElementById('container');
                
                mermaid.initialize(config);
                
                // Render the diagram
                // 図を描画
                const { svg: svgText } = await mermaid.render(svgId || 'my-svg', definition, container);
                container.innerHTML = svgText;
                
                // Apply background color and CSS
                // 背景色とCSSを適用
                const svg = container.getElementsByTagName('svg')[0];
                if (svg) {
                    if (svg.style) {
                        svg.style.backgroundColor = backgroundColor;
                    }
                    
                    // Also set the background color as an attribute for better compatibility
                    // より良い互換性のために背景色を属性としても設定
                    svg.setAttribute('style', svg.getAttribute('style') + `; background-color: ${backgroundColor};`);
                    
                    // Add explicit background property for test compatibility
                    if (backgroundColor !== 'transparent' && backgroundColor !== 'white') {
                        const styleAttr = svg.getAttribute('style') || '';
                        svg.setAttribute('style', styleAttr + `; background: ${backgroundColor};`);
                    }
                    
                    // Add theme class to SVG if specified in config
                    // 設定でテーマが指定されている場合、SVGにテーマクラスを追加
                    if (config.theme) {
                        svg.classList.add(`theme-${config.theme}`);
                    }
                }
                
                if (css) {
                    const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
                    style.appendChild(document.createTextNode(css));
                    svg.appendChild(style);
                }
                
                // Extract metadata
                // メタデータを抽出
                let title = null;
                if (svg.firstChild && svg.firstChild.tagName === 'title') {
                    title = svg.firstChild.textContent;
                }
                
                let desc = null;
                for (const svgNode of svg.children) {
                    if (svgNode.tagName === 'desc') {
                        desc = svgNode.textContent;
                        break;
                    }
                }
                
                return { title, desc };
            }
            """)
            
            title = result.get('title')
            desc = result.get('desc')
            
            # Generate output based on the requested format
            # 要求されたフォーマットに基づいて出力を生成
            if output_format == 'svg':
                # Get SVG as XML string
                # SVGをXML文字列として取得
                svg_xml = await page.evaluate("""
                () => {
                    const svg = document.querySelector('svg');
                    const xmlSerializer = new XMLSerializer();
                    return xmlSerializer.serializeToString(svg);
                }
                """)
                data = svg_xml.encode('utf-8')
            elif output_format == 'png':
                # Get the bounding box of the SVG element
                # SVG要素の境界ボックスを取得
                clip = await page.evaluate("""
                () => {
                    const svg = document.querySelector('svg');
                    const rect = svg.getBoundingClientRect();
                    return { 
                        x: Math.floor(rect.left), 
                        y: Math.floor(rect.top), 
                        width: Math.ceil(rect.width), 
                        height: Math.ceil(rect.height) 
                    };
                }
                """)
                
                # Resize viewport to fit the diagram
                # ビューポートを図に合わせてリサイズ
                await page.set_viewport_size({
                    'width': clip['x'] + clip['width'],
                    'height': clip['y'] + clip['height']
                })
                
                # Take screenshot with clip area
                # クリップ領域でスクリーンショットを撮る
                data = await page.screenshot(
                    clip={
                        'x': clip['x'],
                        'y': clip['y'],
                        'width': clip['width'],
                        'height': clip['height']
                    },
                    omit_background=background_color == 'transparent'
                )
            else:  # pdf
                if pdf_fit:
                    # Get the bounding box of the SVG element
                    # SVG要素の境界ボックスを取得
                    clip = await page.evaluate("""
                    () => {
                        const svg = document.querySelector('svg');
                        const rect = svg.getBoundingClientRect();
                        return { 
                            x: rect.left, 
                            y: rect.top, 
                            width: rect.width, 
                            height: rect.height 
                        };
                    }
                    """)
                    
                    # Generate PDF with custom dimensions
                    # カスタム寸法でPDFを生成
                    data = await page.pdf(
                        width=f"{math.ceil(clip['width']) + clip['x'] * 2}px",
                        height=f"{math.ceil(clip['height']) + clip['y'] * 2}px",
                        print_background=background_color != 'transparent',
                        page_ranges='1-1'
                    )
                else:
                    # Generate PDF with default dimensions
                    # デフォルトの寸法でPDFを生成
                    data = await page.pdf(
                        print_background=background_color != 'transparent'
                    )
            
            return title, desc, data
        
        finally:
            # Always close the browser
            # 常にブラウザを閉じる
            await browser.close()


async def _get_input_data(input_file: Optional[str]) -> str:
    """
    Get input data from file or stdin.
    
    Args:
        input_file: Path to input file or None for stdin
        
    Returns:
        Input data as string

    ファイルまたは標準入力から入力データを取得します。
    
    引数:
        input_file: 入力ファイルのパスまたは標準入力の場合はNone
        
    戻り値:
        文字列としての入力データ
    """
    if input_file:
        with open(input_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        import sys
        return sys.stdin.read()


def _create_markdown_image(url: str, title: Optional[str], alt: str) -> str:
    """
    Create markdown image syntax.
    
    Args:
        url: Path to image
        title: Optional image title
        alt: Image alt text
        
    Returns:
        Markdown image text

    Markdown画像構文を作成します。
    
    引数:
        url: 画像へのパス
        title: オプションの画像タイトル
        alt: 画像の代替テキスト
        
    戻り値:
        Markdown画像テキスト
    """
    # Escape special characters in alt text
    # alt テキスト内の特殊文字をエスケープ
    alt_escaped = alt.replace('[', '\\[').replace(']', '\\]')
    
    if title:
        # Include title if provided
        # タイトルが提供されている場合は含める
        title_escaped = title.replace('"', '\\"')
        return f'![{alt_escaped}]({url} "{title_escaped}")'
    else:
        return f'![{alt_escaped}]({url})'


async def render_mermaid_file(
    input_file: Optional[str],
    output_file: str,
    output_format: Optional[str] = None,
    playwright_config: Dict[str, Any] = None,
    quiet: bool = False,
    **kwargs
) -> None:
    """
    Render a mermaid diagram or markdown file containing mermaid diagrams.
    
    Args:
        input_file: Path to input file or None for stdin
        output_file: Path to output file
        output_format: Output format (svg, png, pdf)
        playwright_config: Browser configuration
        quiet: Suppress log output
        **kwargs: Additional options for render_mermaid

    Mermaid図またはMermaid図を含むMarkdownファイルを描画します。
    
    引数:
        input_file: 入力ファイルのパスまたは標準入力の場合はNone
        output_file: 出力ファイルのパス
        output_format: 出力形式（svg、png、pdf）
        playwright_config: ブラウザ設定
        quiet: ログ出力を抑制
        **kwargs: render_mermaidの追加オプション
    """
    def info(message):
        """Print info message if not in quiet mode"""
        """quietモードでない場合、情報メッセージを表示"""
        if not quiet:
            print(message)
    
    # Determine output format from file extension if not specified
    # 出力形式が指定されていない場合、ファイル拡張子から決定
    if not output_format:
        ext = os.path.splitext(output_file)[1].lower()
        if ext in ('.md', '.markdown'):
            output_format = 'svg'
        elif ext:
            output_format = ext[1:]  # Remove the dot
    
    if output_format not in ('svg', 'png', 'pdf'):
        raise ValueError('Output format must be one of "svg", "png" or "pdf"')
    
    # Get input data
    # 入力データを取得
    definition = await _get_input_data(input_file)
    
    # Create output directory if it doesn't exist
    # 出力ディレクトリが存在しない場合は作成
    output_dir = os.path.dirname(os.path.abspath(output_file))
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if input is markdown
    # 入力がMarkdownかどうかをチェック
    if input_file and input_file.lower().endswith(('.md', '.markdown')):
        if output_file == '/dev/stdout':
            raise ValueError('Cannot use stdout with markdown input')
        
        # Find mermaid code blocks in markdown
        # Markdown内のmermaidコードブロックを検索
        mermaid_pattern = re.compile(r'^[^\S\n]*[`:]{3}(?:mermaid)([^\S\n]*\r?\n([\s\S]*?))[`:]{3}[^\S\n]*$', re.MULTILINE)
        matches = list(mermaid_pattern.finditer(definition))
        
        if matches:
            info(f'Found {len(matches)} mermaid charts in Markdown input')
            
            image_data = []
            for i, match in enumerate(matches):
                mermaid_definition = match.group(2)
                
                # Create output filename with absolute paths
                # 絶対パスで出力ファイル名を作成
                output_file_abs = os.path.abspath(output_file)
                output_dir = os.path.dirname(output_file_abs)
                
                if output_file.lower().endswith(('.md', '.markdown')):
                    output_image = os.path.join(
                        output_dir,
                        f"{os.path.splitext(os.path.basename(output_file))[0]}-{i+1}.{output_format}"
                    )
                else:
                    output_image = os.path.join(
                        output_dir,
                        f"{os.path.splitext(os.path.basename(output_file))[0]}-{i+1}.{output_format}"
                    )
                
                # Calculate relative path for embedding in markdown
                # Markdownに埋め込むための相対パスを計算
                output_image_relative = os.path.relpath(output_image, output_dir)
                if not output_image_relative.startswith('.'):
                    output_image_relative = f'./{output_image_relative}'
                
                # Render the diagram
                # 図を描画
                title, desc, data = await render_mermaid(
                    mermaid_definition,
                    output_format,
                    playwright_config=playwright_config,
                    **kwargs
                )
                
                # Write the output file
                # 出力ファイルを書き込む
                with open(output_image, 'wb') as f:
                    f.write(data)
                
                info(f' ✅ {output_image_relative}')
                
                image_data.append({
                    'url': output_image_relative,
                    'title': title,
                    'alt': desc or 'diagram'
                })
            
            # If output is markdown, replace mermaid code blocks with images
            # 出力がMarkdownの場合、mermaidコードブロックを画像に置き換え
            if output_file.lower().endswith(('.md', '.markdown')):
                def replace_func(match):
                    if not image_data:
                        return match.group(0)  # Keep original if no image data
                    img = image_data.pop(0)
                    return _create_markdown_image(img['url'], img['title'], img['alt'])
                
                out_definition = mermaid_pattern.sub(replace_func, definition)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(out_definition)
                
                info(f' ✅ {output_file}')
        else:
            info('No mermaid charts found in Markdown input')
            # Create an empty output file to ensure it exists even when no charts are found
            # チャートが見つからない場合でも確実に出力ファイルが存在するようにする
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(definition)
            
            info(f' ✅ {output_file}')
    else:
        # Render a single mermaid diagram
        # 単一のMermaid図を描画
        info('Generating single mermaid chart')
        
        title, desc, data = await render_mermaid(
            definition,
            output_format,
            playwright_config=playwright_config,
            **kwargs
        )
        
        if output_file == '/dev/stdout':
            # Write to stdout
            # 標準出力に書き込む
            import sys
            sys.stdout.buffer.write(data)
        else:
            # Write to file
            # ファイルに書き込む
            with open(output_file, 'wb') as f:
                f.write(data)


def render_mermaid_file_sync(
    input_file: Optional[str],
    output_file: str,
    output_format: Optional[str] = None,
    **kwargs
) -> None:
    """
    Synchronous wrapper for render_mermaid_file.
    
    Args:
        input_file: Path to input file or None for stdin
        output_file: Path to output file
        output_format: Output format (svg, png, pdf)
        **kwargs: Additional options for render_mermaid

    render_mermaid_fileの同期ラッパー。
    
    引数:
        input_file: 入力ファイルのパスまたは標準入力の場合はNone
        output_file: 出力ファイルのパス
        output_format: 出力形式（svg、png、pdf）
        **kwargs: render_mermaidの追加オプション
    """
    # Use asyncio.run() instead of manually getting the event loop
    # イベントループを手動で取得する代わりにasyncio.run()を使用
    asyncio.run(render_mermaid_file(input_file, output_file, output_format, **kwargs))
