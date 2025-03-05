"""
API reference tests for mermaid-cli

This module contains tests for all API functions in the mermaid-cli package,
ensuring that each function works as expected and can be used as a library.

mermaid-cliのAPIリファレンステスト

このモジュールはmermaid-cliパッケージのすべてのAPI関数のテストを含み、
各関数が期待通りに動作し、ライブラリとして使用できることを確認します。
"""

import asyncio
import os
import tempfile
import unittest
from pathlib import Path

from mermaid_cli import (
    render_mermaid,
    render_mermaid_file,
    render_mermaid_file_sync
)


class TestMermaidCLIAPI(unittest.TestCase):
    """
    Test cases for mermaid-cli API functions
    
    mermaid-cli API関数のテストケース
    """
    
    def setUp(self):
        """
        Set up test environment
        
        テスト環境のセットアップ
        """
        # Create test diagrams for different chart types
        # 異なるチャートタイプのテスト図を作成
        
        # Flowchart
        self.flowchart = """
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
"""
        
        # Sequence diagram
        self.sequence_diagram = """
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
"""
        
        # Class diagram
        self.class_diagram = """
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }
"""
        
        # State diagram
        self.state_diagram = """
stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
"""
        
        # Entity Relationship diagram
        self.er_diagram = """
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
"""
        
        # Gantt chart
        self.gantt_chart = """
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2014-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2014-01-12  , 12d
    another task     : 24d
"""
        
        # Pie chart
        self.pie_chart = """
pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 85
    "Rats" : 15
"""
        
        # User Journey diagram
        self.user_journey = """
journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me
"""

    def test_api_render_mermaid_flowchart(self):
        """
        Test API: render_mermaid with flowchart
        
        API: フローチャートでのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.flowchart,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_sequence_diagram(self):
        """
        Test API: render_mermaid with sequence diagram
        
        API: シーケンス図でのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.sequence_diagram,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_class_diagram(self):
        """
        Test API: render_mermaid with class diagram
        
        API: クラス図でのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.class_diagram,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_state_diagram(self):
        """
        Test API: render_mermaid with state diagram
        
        API: 状態図でのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.state_diagram,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_er_diagram(self):
        """
        Test API: render_mermaid with ER diagram
        
        API: ER図でのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.er_diagram,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_gantt_chart(self):
        """
        Test API: render_mermaid with Gantt chart
        
        API: ガントチャートでのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.gantt_chart,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_pie_chart(self):
        """
        Test API: render_mermaid with Pie chart
        
        API: 円グラフでのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.pie_chart,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_user_journey(self):
        """
        Test API: render_mermaid with User Journey
        
        API: ユーザージャーニーでのrender_mermaidのテスト
        """
        async def run_test():
            title, desc, data = await render_mermaid(
                self.user_journey,
                output_format='svg'
            )
            self.assertIsInstance(data, bytes)
            self.assertTrue(data.startswith(b'<svg'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_all_formats(self):
        """
        Test API: render_mermaid with all output formats
        
        API: すべての出力形式でのrender_mermaidのテスト
        """
        async def run_test():
            # Test SVG output
            title, desc, svg_data = await render_mermaid(
                self.flowchart,
                output_format='svg'
            )
            self.assertIsInstance(svg_data, bytes)
            self.assertTrue(svg_data.startswith(b'<svg'))
            
            # Test PNG output
            title, desc, png_data = await render_mermaid(
                self.flowchart,
                output_format='png'
            )
            self.assertIsInstance(png_data, bytes)
            self.assertTrue(png_data.startswith(b'\x89PNG'))
            
            # Test PDF output
            title, desc, pdf_data = await render_mermaid(
                self.flowchart,
                output_format='pdf'
            )
            self.assertIsInstance(pdf_data, bytes)
            self.assertTrue(pdf_data.startswith(b'%PDF'))
            
        asyncio.run(run_test())

    def test_api_render_mermaid_file_all_formats(self):
        """
        Test API: render_mermaid_file with all output formats
        
        API: すべての出力形式でのrender_mermaid_fileのテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.flowchart.encode('utf-8'))
            input_path = input_file.name
        
        try:
            async def run_test():
                # Test SVG output
                svg_output = input_path + '.svg'
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=svg_output,
                    output_format='svg'
                )
                self.assertTrue(os.path.exists(svg_output))
                with open(svg_output, 'rb') as f:
                    self.assertTrue(f.read().startswith(b'<svg'))
                os.unlink(svg_output)
                
                # Test PNG output
                png_output = input_path + '.png'
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=png_output,
                    output_format='png'
                )
                self.assertTrue(os.path.exists(png_output))
                with open(png_output, 'rb') as f:
                    self.assertTrue(f.read().startswith(b'\x89PNG'))
                os.unlink(png_output)
                
                # Test PDF output
                pdf_output = input_path + '.pdf'
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=pdf_output,
                    output_format='pdf'
                )
                self.assertTrue(os.path.exists(pdf_output))
                with open(pdf_output, 'rb') as f:
                    self.assertTrue(f.read().startswith(b'%PDF'))
                os.unlink(pdf_output)
                
            asyncio.run(run_test())
        finally:
            # Clean up temporary file
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)

    def test_api_render_mermaid_file_sync_all_formats(self):
        """
        Test API: render_mermaid_file_sync with all output formats
        
        API: すべての出力形式でのrender_mermaid_file_syncのテスト
        """
        with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as input_file:
            input_file.write(self.flowchart.encode('utf-8'))
            input_path = input_file.name
        
        try:
            # Test SVG output
            svg_output = input_path + '.svg'
            render_mermaid_file_sync(
                input_file=input_path,
                output_file=svg_output,
                output_format='svg'
            )
            self.assertTrue(os.path.exists(svg_output))
            with open(svg_output, 'rb') as f:
                self.assertTrue(f.read().startswith(b'<svg'))
            os.unlink(svg_output)
            
            # Test PNG output
            png_output = input_path + '.png'
            render_mermaid_file_sync(
                input_file=input_path,
                output_file=png_output,
                output_format='png'
            )
            self.assertTrue(os.path.exists(png_output))
            with open(png_output, 'rb') as f:
                self.assertTrue(f.read().startswith(b'\x89PNG'))
            os.unlink(png_output)
            
            # Test PDF output
            pdf_output = input_path + '.pdf'
            render_mermaid_file_sync(
                input_file=input_path,
                output_file=pdf_output,
                output_format='pdf'
            )
            self.assertTrue(os.path.exists(pdf_output))
            with open(pdf_output, 'rb') as f:
                self.assertTrue(f.read().startswith(b'%PDF'))
            os.unlink(pdf_output)
            
        finally:
            # Clean up temporary file
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)

    def test_api_render_mermaid_file_markdown(self):
        """
        Test API: render_mermaid_file with markdown input
        
        API: Markdown入力でのrender_mermaid_fileのテスト
        """
        # Create a markdown file with multiple diagrams
        # 複数の図を含むMarkdownファイルを作成
        markdown_content = """# Test Markdown

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
        
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as input_file:
            input_file.write(markdown_content.encode('utf-8'))
            input_path = input_file.name
        
        output_path = input_path.replace('.md','.out.md')
        
        try:
            async def run_test():
                await render_mermaid_file(
                    input_file=input_path,
                    output_file=output_path,
                    output_format='svg'  # Changed from 'md' to 'svg'
                )
                
                self.assertTrue(os.path.exists(output_path))
                
                # Check that the SVG files were generated
                # SVGファイルが生成されたことを確認
                svg_file1 = output_path.replace('.md', '-1.svg')  # Changed from '.md' to '.svg'
                svg_file2 = output_path.replace('.md', '-2.svg')  # Changed from '.md' to '.svg'
                self.assertTrue(os.path.exists(svg_file1))
                self.assertTrue(os.path.exists(svg_file2))
                
                # Check that the markdown file contains image references
                # Markdownファイルが画像参照を含んでいることを確認
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertIn('![diagram](./', content)
                    self.assertNotIn('```mermaid', content)
                
                # Clean up generated files
                # 生成されたファイルをクリーンアップ
                os.unlink(svg_file1)
                os.unlink(svg_file2)
                os.unlink(output_path)
            
            asyncio.run(run_test())
        finally:
            # Clean up temporary file
            # 一時ファイルをクリーンアップ
            if os.path.exists(input_path):
                os.unlink(input_path)


if __name__ == '__main__':
    unittest.main()
