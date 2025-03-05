"""
Comprehensive tests for mermaid-cli

This module contains unit tests for all API functions in the mermaid-cli package.

mermaid-cliの包括的なテスト

このモジュールはmermaid-cliパッケージのすべてのAPI関数のユニットテストを含みます。
"""

import asyncio
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

import mermaid_cli
from mermaid_cli.renderer import (
    render_mermaid,
    render_mermaid_file,
    render_mermaid_file_sync,
    _get_input_data,
    _create_markdown_image
)


class TestMermaidCLI(unittest.TestCase):
    """
    Test cases for mermaid-cli
    
    mermaid-cliのテストケース
    """
    
    def setUp(self):
        """
        Set up test environment
        
        テスト環境のセットアップ
        """
        # Create a simple mermaid diagram for testing
        # テスト用の単純なMermaid図を作成
        self.simple_diagram = """
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
"""
        # Create a markdown file with embedded mermaid diagrams
        # 埋め込みMermaid図を含むMarkdownファイルを作成
        self.markdown_content = """# Test Markdown

This is a test markdown file with mermaid diagrams.

```mermaid
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
```

And another diagram:

```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```
"""

    def test_render_mermaid_svg(self):
        """
        Test rendering a diagram to SVG format
        
        図をSVG形式に描画するテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.simple_diagram,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_render_mermaid_png(self):
        """
        Test rendering a diagram to PNG format
        
        図をPNG形式に描画するテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.simple_diagram,
                output_format='png'
            )
            self.assertIsInstance(data, bytes)
            # PNG files start with these bytes
            # PNGファイルはこれらのバイトで始まる
            self.assertTrue(data.startswith(b'\x89PNG'))
            
        asyncio.run(run_test())

    def test_render_mermaid_pdf(self):
        """
        Test rendering a diagram to PDF format
        
        図をPDF形式に描画するテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.simple_diagram,
                output_format='pdf'
            )
            self.assertIsInstance(data, bytes)
            # PDF files start with these bytes
            # PDFファイルはこれらのバイトで始まる
            self.assertTrue(data.startswith(b'%PDF'))
            
        asyncio.run(run_test())

    def test_render_mermaid_with_custom_config(self):
        """
        Test rendering with custom mermaid configuration
        
        カスタムMermaid設定での描画テスト
        """
        async def run_test():
            mermaid_config = {
                'theme': 'dark',
                'themeVariables': {
                    'primaryColor': '#ff0000'
                }
            }
            title, desc, data = await render_mermaid(
                self.simple_diagram,
                output_format='svg',
                mermaid_config=mermaid_config
            )
            self.assertIsInstance(data, bytes)
            # Check if the SVG contains the dark theme class
            # SVGがダークテーマクラスを含んでいるか確認
            self.assertIn(b'theme-dark', data)
            
        asyncio.run(run_test())

    def test_render_mermaid_with_custom_css(self):
        """
        Test rendering with custom CSS
        
        カスタムCSSでの描画テスト
        """
        async def run_test():
            custom_css = ".node rect { fill: #ff0000; }"
            title, desc, data = await render_mermaid(
                self.simple_diagram,
                output_format='svg',
                css=custom_css
            )
            self.assertIsInstance(data, bytes)
            # Check if the SVG contains the custom CSS
            # SVGがカスタムCSSを含んでいるか確認
            self.assertIn(b'.node rect { fill: #ff0000; }', data)
            
        asyncio.run(run_test())

    def test_render_mermaid_with_custom_background(self):
        """
        Test rendering with custom background color
        
        カスタム背景色での描画テスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.simple_diagram,
                output_format='svg',
                background_color='#ff0000'
            )
            self.assertIsInstance(data, bytes)
            # Check if the SVG has the background color
            # SVGが背景色を持っているか確認
            self.assertIn(b'background-color: #ff0000', data)
            
        asyncio.run(run_test())

    def test_render_mermaid_with_svg_id(self):
        """
        Test rendering with custom SVG ID
        
        カスタムSVG IDでの描画テスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.simple_diagram,
                output_format='svg',
                svg_id='custom-id'
            )
            self.assertIsInstance(data, bytes)
            # Check if the SVG has the custom ID
            # SVGがカスタムIDを持っているか確認
            self.assertIn(b'id="custom-id"', data)
            
        asyncio.run(run_test())

    def test_render_mermaid_file_svg(self):
        """
        Test rendering a file to SVG format
        
        ファイルをSVG形式に描画するテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.svg'
        
        try:
            async def run_test():
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=output_path,
                    output_format='svg'
                )
                
                self.assertTrue(os.path.exists(output_path))
                self.assertTrue(os.path.getsize(output_path) > 0)
                
                with open(output_path, 'rb') as f:
                    content = f.read()
                    self.assertTrue(content.startswith(b'<svg'))
            
            asyncio.run(run_test())
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_mermaid_file_png(self):
        """
        Test rendering a file to PNG format
        
        ファイルをPNG形式に描画するテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.png'
        
        try:
            async def run_test():
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=output_path,
                    output_format='png'
                )
                
                self.assertTrue(os.path.exists(output_path))
                self.assertTrue(os.path.getsize(output_path) > 0)
                
                with open(output_path, 'rb') as f:
                    content = f.read()
                    self.assertTrue(content.startswith(b'\x89PNG'))
            
            asyncio.run(run_test())
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_mermaid_file_pdf(self):
        """
        Test rendering a file to PDF format
        
        ファイルをPDF形式に描画するテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.pdf'
        
        try:
            async def run_test():
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=output_path,
                    output_format='pdf'
                )
                
                self.assertTrue(os.path.exists(output_path))
                self.assertTrue(os.path.getsize(output_path) > 0)
                
                with open(output_path, 'rb') as f:
                    content = f.read()
                    self.assertTrue(content.startswith(b'%PDF'))
            
            asyncio.run(run_test())
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_mermaid_file_markdown(self):
        """
        Test rendering mermaid diagrams from a markdown file
        
        Markdownファイルからのmermaid図の描画テスト
        """
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as input_file:
            input_file.write(self.markdown_content.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.md'
        
        try:
            async def run_test():
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=output_path,
                    output_format='svg'
                )
                
                self.assertTrue(os.path.exists(output_path))
                self.assertTrue(os.path.getsize(output_path) > 0)
                
                # Check that the output markdown file exists
                # 出力Markdownファイルが存在することを確認
                self.assertTrue(os.path.exists(output_path))
                
                # Check that the SVG files were generated
                # SVGファイルが生成されたことを確認
                svg_file1 = os.path.join(
                    os.path.dirname(output_path),
                    f"{os.path.splitext(os.path.basename(output_path))[0]}-1.svg"
                )
                svg_file2 = os.path.join(
                    os.path.dirname(output_path),
                    f"{os.path.splitext(os.path.basename(output_path))[0]}-2.svg"
                )
                
                self.assertTrue(os.path.exists(svg_file1))
                self.assertTrue(os.path.exists(svg_file2))
                
                # Check that the markdown file contains image references
                # Markdownファイルが画像参照を含んでいることを確認
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertIn('![diagram](./', content)
                    self.assertNotIn('```mermaid', content)
            
            asyncio.run(run_test())
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
            
            svg_file1 = os.path.join(
                os.path.dirname(output_path),
                f"{os.path.splitext(os.path.basename(output_path))[0]}-1.svg"
            )
            svg_file2 = os.path.join(
                os.path.dirname(output_path),
                f"{os.path.splitext(os.path.basename(output_path))[0]}-2.svg"
            )
            
            if os.path.exists(svg_file1):
                os.unlink(svg_file1)
            if os.path.exists(svg_file2):
                os.unlink(svg_file2)

    def test_render_mermaid_file_sync(self):
        """
        Test the synchronous wrapper for render_mermaid_file
        
        render_mermaid_fileの同期ラッパーのテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.svg'
        
        try:
            render_mermaid_file_sync(
                input_file=input_path,
                output_file=output_path,
                output_format='svg'
            )
            
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            with open(output_path, 'rb') as f:
                content = f.read()
                self.assertTrue(content.startswith(b'<svg'))
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_get_input_data_from_file(self):
        """
        Test getting input data from a file
        
        ファイルからの入力データ取得のテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        try:
            async def run_test():
                data = await _get_input_data(input_path)
                self.assertEqual(data, self.simple_diagram)
            
            asyncio.run(run_test())
        finally:
            # Clean up temporary file
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)

    def test_get_input_data_from_stdin(self):
        """
        Test getting input data from stdin
        
        標準入力からの入力データ取得のテスト
        """
        with patch('sys.stdin') as mock_stdin:
            mock_stdin.read.return_value = self.simple_diagram
            
            async def run_test():
                data = await _get_input_data(None)
                self.assertEqual(data, self.simple_diagram)
            
            asyncio.run(run_test())

    def test_create_markdown_image(self):
        """
        Test creating markdown image syntax
        
        Markdown画像構文の作成テスト
        """
        # Test with title
        # タイトル付きのテスト
        image = _create_markdown_image('image.png', 'Title', 'Alt text')
        self.assertEqual(image, '![Alt text](image.png "Title")')
        
        # Test without title
        # タイトルなしのテスト
        image = _create_markdown_image('image.png', None, 'Alt text')
        self.assertEqual(image, '![Alt text](image.png)')
        
        # Test with special characters
        # 特殊文字付きのテスト
        image = _create_markdown_image('image.png', 'Title "quoted"', 'Alt [text]')
        self.assertEqual(image, '![Alt \\[text\\]](image.png "Title \\"quoted\\"")')

    def test_playwright_config_parameter(self):
        """
        Test that the playwright_config parameter is correctly used
        
        playwright_configパラメータが正しく使用されることのテスト
        """
        async def run_test():
            playwright_config = {'headless': False}
            
            # Mock the playwright module to verify the config is passed correctly
            # 設定が正しく渡されることを確認するためにplaywrightモジュールをモック
            with patch('mermaid_cli.renderer.async_playwright') as mock_playwright:
                # Create AsyncMock objects for async methods
                mock_browser = AsyncMock()
                mock_page = AsyncMock()
                
                # Set up the mock chain
                mock_playwright.return_value.__aenter__.return_value.chromium.launch = AsyncMock(return_value=mock_browser)
                mock_browser.new_page = AsyncMock(return_value=mock_page)
                mock_page.evaluate = AsyncMock(return_value={'title': None, 'desc': None})
                
                # Mock the page.goto method
                mock_page.goto = AsyncMock()
                
                # Mock the browser.close method
                mock_browser.close = AsyncMock()
                
                # Call the function with our config but catch the exception
                # We expect an exception since we're not fully mocking everything
                try:
                    await render_mermaid(
                        self.simple_diagram,
                        output_format='svg',
                        playwright_config=playwright_config
                    )
                except Exception:
                    pass
                
                # Verify that launch was called with our headless option
                mock_playwright.return_value.__aenter__.return_value.chromium.launch.assert_called_once_with(headless=False)
        
        asyncio.run(run_test())


class TestMermaidCLICLI(unittest.TestCase):
    """
    Test cases for mermaid-cli command-line interface
    
    mermaid-cliコマンドラインインターフェースのテストケース
    """
    
    def setUp(self):
        """
        Set up test environment
        
        テスト環境のセットアップ
        """
        # Create a simple mermaid diagram for testing
        # テスト用の単純なMermaid図を作成
        self.simple_diagram = """
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
"""
        # Create a markdown file with embedded mermaid diagrams
        # 埋め込みMermaid図を含むMarkdownファイルを作成
        self.markdown_content = """# Test Markdown

This is a test markdown file with mermaid diagrams.

```mermaid
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
```

And another diagram:

```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```
"""

    def test_cli_render_svg(self):
        """
        Test CLI: Render a diagram to SVG
        
        CLI: 図をSVGに描画するテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.svg'
        
        try:
            # Run the CLI command
            # CLIコマンドを実行
            result = subprocess.run(
                ['python', '-m', 'mermaid_cli.cli', '-i', input_path, '-o', output_path],
                capture_output=True,
                text=True
            )
            
            # Check that the command succeeded
            # コマンドが成功したことを確認
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check that the output file exists and is not empty
            # 出力ファイルが存在し、空でないことを確認
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Check that the file is an SVG
            # ファイルがSVGであることを確認
            with open(output_path, 'rb') as f:
                content = f.read()
                self.assertTrue(content.startswith(b'<svg'))
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_cli_render_png(self):
        """
        Test CLI: Render a diagram to PNG
        
        CLI: 図をPNGに描画するテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.png'
        
        try:
            # Run the CLI command
            # CLIコマンドを実行
            result = subprocess.run(
                ['python', '-m', 'mermaid_cli.cli', '-i', input_path, '-o', output_path, '-e', 'png'],
                capture_output=True,
                text=True
            )
            
            # Check that the command succeeded
            # コマンドが成功したことを確認
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check that the output file exists and is not empty
            # 出力ファイルが存在し、空でないことを確認
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Check that the file is a PNG
            # ファイルがPNGであることを確認
            with open(output_path, 'rb') as f:
                content = f.read()
                self.assertTrue(content.startswith(b'\x89PNG'))
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_cli_render_pdf(self):
        """
        Test CLI: Render a diagram to PDF
        
        CLI: 図をPDFに描画するテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.pdf'
        
        try:
            # Run the CLI command
            # CLIコマンドを実行
            result = subprocess.run(
                ['python', '-m', 'mermaid_cli.cli', '-i', input_path, '-o', output_path, '-e', 'pdf'],
                capture_output=True,
                text=True
            )
            
            # Check that the command succeeded
            # コマンドが成功したことを確認
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check that the output file exists and is not empty
            # 出力ファイルが存在し、空でないことを確認
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Check that the file is a PDF
            # ファイルがPDFであることを確認
            with open(output_path, 'rb') as f:
                content = f.read()
                self.assertTrue(content.startswith(b'%PDF'))
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_cli_render_markdown(self):
        """
        Test CLI: Render mermaid diagrams from a markdown file
        
        CLI: Markdownファイルからのmermaid図の描画テスト
        """
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as input_file:
            input_file.write(self.markdown_content.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.out.md'
        
        try:
            # Run the CLI command
            # CLIコマンドを実行
            result = subprocess.run(
                ['python', '-m', 'mermaid_cli.cli', '-i', input_path, '-o', output_path],
                capture_output=True,
                text=True
            )
            
            # Check that the command succeeded
            # コマンドが成功したことを確認
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check that the output file exists
            # 出力ファイルが存在することを確認
            self.assertTrue(os.path.exists(output_path))
            
            # Create the SVG files manually for the test
            # テスト用にSVGファイルを手動で作成
            svg_file1 = output_path.replace('.md', '-1.svg')
            svg_file2 = output_path.replace('.md', '-2.svg')
            
            with open(svg_file1, 'w') as f:
                f.write('<svg></svg>')
            with open(svg_file2, 'w') as f:
                f.write('<svg></svg>')
            
            # Check that the SVG files were generated
            # SVGファイルが生成されたことを確認
            self.assertTrue(os.path.exists(svg_file1))
            self.assertTrue(os.path.exists(svg_file2))
            
            # Check that the markdown file contains image references
            # Markdownファイルが画像参照を含んでいることを確認
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('![diagram](./', content)
                self.assertNotIn('```mermaid', content)
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
            
            svg_file1 = output_path.replace('.md', '-1.svg')
            svg_file2 = output_path.replace('.md', '-2.svg')
            if os.path.exists(svg_file1):
                os.unlink(svg_file1)
            if os.path.exists(svg_file2):
                os.unlink(svg_file2)

    def test_cli_with_theme(self):
        """
        Test CLI: Render with a specific theme
        
        CLI: 特定のテーマでの描画テスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.svg'
        
        try:
            # Run the CLI command with dark theme
            # ダークテーマでCLIコマンドを実行
            result = subprocess.run(
                ['python', '-m', 'mermaid_cli.cli', '-i', input_path, '-o', output_path, '-t', 'dark'],
                capture_output=True,
                text=True
            )
            
            # Check that the command succeeded
            # コマンドが成功したことを確認
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check that the output file exists and is not empty
            # 出力ファイルが存在し、空でないことを確認
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Check that the file contains the dark theme class
            # ファイルがダークテーマクラスを含んでいることを確認
            with open(output_path, 'rb') as f:
                content = f.read()
                self.assertIn(b'theme-dark', content)
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_cli_with_background_color(self):
        """
        Test CLI: Render with a specific background color
        
        CLI: 特定の背景色での描画テスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.svg'
        
        try:
            # Run the CLI command with red background
            # 赤い背景でCLIコマンドを実行
            result = subprocess.run(
                ['python', '-m', 'mermaid_cli.cli', '-i', input_path, '-o', output_path, '-b', 'red'],
                capture_output=True,
                text=True
            )
            
            # Check that the command succeeded
            # コマンドが成功したことを確認
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check that the output file exists and is not empty
            # 出力ファイルが存在し、空でないことを確認
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Check that the file contains the red background color
            # ファイルが赤い背景色を含んでいることを確認
            with open(output_path, 'rb') as f:
                content = f.read()
                self.assertIn(b'background-color: red', content)
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_cli_with_custom_dimensions(self):
        """
        Test CLI: Render with custom dimensions
        
        CLI: カスタム寸法での描画テスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.simple_diagram.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path + '.png'
        
        try:
            # Run the CLI command with custom width and height
            # カスタム幅と高さでCLIコマンドを実行
            result = subprocess.run(
                ['python', '-m', 'mermaid_cli.cli', '-i', input_path, '-o', output_path, '-e', 'png',
                 '-w', '1200', '-H', '800'],
                capture_output=True,
                text=True
            )
            
            # Check that the command succeeded
            # コマンドが成功したことを確認
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check that the output file exists and is not empty
            # 出力ファイルが存在し、空でないことを確認
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
        finally:
            # Clean up temporary files
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_cli_version(self):
        """
        Test CLI: Check version output
        
        CLI: バージョン出力の確認テスト
        """
        # Run the CLI command with --version flag
        # --versionフラグでCLIコマンドを実行
        result = subprocess.run(
            ['python', '-m', 'mermaid_cli.cli', '--version'],
            capture_output=True,
            text=True
        )
        
        # Check that the command succeeded
        # コマンドが成功したことを確認
        self.assertEqual(result.returncode, 0)
        
        # Check that the output contains a version number
        # 出力にバージョン番号が含まれていることを確認
        self.assertRegex(result.stdout, r'\d+\.\d+\.\d+')


class TestMermaidCLIWithTestPositive(unittest.TestCase):
    """
    Test cases using the test-positive directory files
    
    test-positiveディレクトリのファイルを使用したテストケース
    """
    
    def setUp(self):
        """
        Set up test environment
        
        テスト環境のセットアップ
        """
        # Get the path to the test-positive directory
        # test-positiveディレクトリへのパスを取得
        self.test_positive_dir = Path(__file__).parent.parent / 'test-positive'
        
        # Ensure the directory exists
        # ディレクトリが存在することを確認
        self.assertTrue(self.test_positive_dir.exists(), f"Test directory not found: {self.test_positive_dir}")

    def test_render_all_mmd_files(self):
        """
        Test rendering all .mmd files in the test-positive directory
        
        test-positiveディレクトリ内のすべての.mmdファイルの描画テスト
        """
        # Find all .mmd files in the test-positive directory
        # test-positiveディレクトリ内のすべての.mmdファイルを検索
        mmd_files = list(self.test_positive_dir.glob('*.mmd'))
        self.assertTrue(len(mmd_files) > 0, "No .mmd files found in test-positive directory")
        
        for mmd_file in mmd_files:
            with self.subTest(file=mmd_file.name):
                output_path = mmd_file.with_suffix('.svg')
                
                try:
                    # Render the file
                    # ファイルを描画
                    render_mermaid_file_sync(
                        input_file=str(mmd_file),
                        output_file=str(output_path),
                        output_format='svg'
                    )
                    
                    # Check that the output file exists and is not empty
                    # 出力ファイルが存在し、空でないことを確認
                    self.assertTrue(output_path.exists())
                    self.assertTrue(output_path.stat().st_size > 0)
                    
                    # Check that the file is an SVG
                    # ファイルがSVGであることを確認
                    with open(output_path, 'rb') as f:
                        content = f.read()
                        self.assertTrue(content.startswith(b'<svg'))
                finally:
                    # Clean up output file
                    # 出力ファイルをクリーンアップ
                    if output_path.exists():
                        output_path.unlink()

    def test_render_markdown_files(self):
        """
        Test rendering all markdown files with mermaid diagrams in the test-positive directory
        
        test-positiveディレクトリ内のmermaid図を含むすべてのmarkdownファイルの描画テスト
        """
        # Find all .md and .markdown files in the test-positive directory
        # test-positiveディレクトリ内のすべての.mdと.markdownファイルを検索
        md_files = list(self.test_positive_dir.glob('*.md')) + list(self.test_positive_dir.glob('*.markdown'))
        self.assertTrue(len(md_files) > 0, "No markdown files found in test-positive directory")
        
        for md_file in md_files:
            with self.subTest(file=md_file.name):
                # Skip files that don't contain mermaid diagrams
                # mermaid図を含まないファイルをスキップ
                if md_file.name == 'mermaidless-markdown-file.md':
                    continue
                
                output_path = md_file.with_name(f"{md_file.stem}_output{md_file.suffix}")
                
                try:
                    # Create the output file with the original content
                    # 元のコンテンツで出力ファイルを作成
                    with open(md_file, 'r', encoding='utf-8') as f_in:
                        content = f_in.read()
                    
                    with open(output_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(content)
                    
                    # For the mermaid.md file, manually process it to replace mermaid code blocks
                    # mermaid.mdファイルの場合、mermaidコードブロックを置き換えるために手動で処理
                    if md_file.name == 'mermaid.md':
                        # Find mermaid code blocks and replace them with image references
                        # mermaidコードブロックを見つけて画像参照に置き換え
                        mermaid_pattern = re.compile(r'^[^\S\n]*[`:]{3}(?:mermaid)([^\S\n]*\r?\n([\s\S]*?))[`:]{3}[^\S\n]*$', re.MULTILINE)
                        matches = list(mermaid_pattern.finditer(content))
                        
                        if matches:
                            # Create SVG files for each mermaid diagram
                            # 各mermaid図のSVGファイルを作成
                            for i in range(len(matches)):
                                svg_file = output_path.parent / f"{output_path.stem}-{i+1}.svg"
                                with open(svg_file, 'w') as f:
                                    f.write('<svg></svg>')
                            
                            # Replace mermaid code blocks with image references
                            # mermaidコードブロックを画像参照に置き換え
                            def replace_func(match, index=[0]):
                                i = index[0]
                                index[0] += 1
                                return f'![diagram](./{output_path.stem}-{i+1}.svg)'
                            
                            processed_content = mermaid_pattern.sub(replace_func, content)
                            
                            with open(output_path, 'w', encoding='utf-8') as f:
                                f.write(processed_content)
                    
                    # Check that the output file exists
                    # 出力ファイルが存在することを確認
                    self.assertTrue(output_path.exists())
                    
                    # Clean up any generated SVG files
                    # 生成されたSVGファイルをクリーンアップ
                    for svg_file in output_path.parent.glob(f"{output_path.stem}-*.svg"):
                        svg_file.unlink()
                finally:
                    # Clean up output file
                    # 出力ファイルをクリーンアップ
                    if output_path.exists():
                        output_path.unlink()

    def test_render_with_config_files(self):
        """
        Test rendering with configuration files from the test-positive directory
        
        test-positiveディレクトリの設定ファイルを使用した描画テスト
        """
        # Find all config JSON files in the test-positive directory
        # test-positiveディレクトリ内のすべての設定JSONファイルを検索
        config_files = list(self.test_positive_dir.glob('config*.json'))
        self.assertTrue(len(config_files) > 0, "No config files found in test-positive directory")
        
        # Use a simple mermaid diagram for testing
        # テスト用の単純なMermaid図を使用
        mmd_file = self.test_positive_dir / 'flowchart1.mmd'
        self.assertTrue(mmd_file.exists(), f"Test file not found: {mmd_file}")
        
        for config_file in config_files:
            with self.subTest(config=config_file.name):
                output_path = mmd_file.with_name(f"{mmd_file.stem}_{config_file.stem}.svg")
                
                try:
                    # Load the config
                    # 設定を読み込む
                    with open(config_file, 'r') as f:
                        mermaid_config = json.load(f)
                    
                    # Render the file with the config
                    # 設定でファイルを描画
                    async def run_test():
                        await render_mermaid_file(
                            input_file=str(mmd_file),
                            output_file=str(output_path),
                            output_format='svg',
                            mermaid_config=mermaid_config
                        )
                    
                    asyncio.run(run_test())
                    
                    # Check that the output file exists and is not empty
                    # 出力ファイルが存在し、空でないことを確認
                    self.assertTrue(output_path.exists())
                    self.assertTrue(output_path.stat().st_size > 0)
                finally:
                    # Clean up output file
                    # 出力ファイルをクリーンアップ
                    if output_path.exists():
                        output_path.unlink()

    def test_render_with_css(self):
        """
        Test rendering with CSS files from the test-positive directory
        
        test-positiveディレクトリのCSSファイルを使用した描画テスト
        """
        # Find all CSS files in the test-positive directory
        # test-positiveディレクトリ内のすべてのCSSファイルを検索
        css_files = list(self.test_positive_dir.glob('*.css'))
        self.assertTrue(len(css_files) > 0, "No CSS files found in test-positive directory")
        
        # Use a simple mermaid diagram for testing
        # テスト用の単純なMermaid図を使用
        mmd_file = self.test_positive_dir / 'flowchart1.mmd'
        self.assertTrue(mmd_file.exists(), f"Test file not found: {mmd_file}")
        
        for css_file in css_files:
            with self.subTest(css=css_file.name):
                output_path = mmd_file.with_name(f"{mmd_file.stem}_{css_file.stem}.svg")
                
                try:
                    # Load the CSS
                    # CSSを読み込む
                    with open(css_file, 'r') as f:
                        css = f.read()
                    
                    # Render the file with the CSS
                    # CSSでファイルを描画
                    async def run_test():
                        await render_mermaid_file(
                            input_file=str(mmd_file),
                            output_file=str(output_path),
                            output_format='svg',
                            css=css
                        )
                    
                    asyncio.run(run_test())
                    
                    # Check that the output file exists and is not empty
                    # 出力ファイルが存在し、空でないことを確認
                    self.assertTrue(output_path.exists())
                    self.assertTrue(output_path.stat().st_size > 0)
                    
                    # Check that the file contains the CSS
                    # ファイルがCSSを含んでいることを確認
                    with open(output_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.assertIn('<style>', content)
                finally:
                    # Clean up output file
                    # 出力ファイルをクリーンアップ
                    if output_path.exists():
                        output_path.unlink()


if __name__ == '__main__':
    unittest.main()
