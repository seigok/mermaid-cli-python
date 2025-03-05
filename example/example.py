"""
Example usage of mermaid-cli as a Python library

This module demonstrates how to use the mermaid-cli package as a Python library
to render Mermaid diagrams in various ways.

mermaid-cliをPythonライブラリとして使用する例

このモジュールは、Mermaid図を様々な方法で描画するために、
mermaid-cliパッケージをPythonライブラリとして使用する方法を示します。
"""

import asyncio
import os
import sys
from pathlib import Path
from mermaid_cli import render_mermaid, render_mermaid_file, render_mermaid_file_sync


# Create output directory if it doesn't exist
# 出力ディレクトリが存在しない場合は作成
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Add a .gitignore file to prevent committing generated images
# 生成された画像をコミットしないように.gitignoreファイルを追加
GITIGNORE_PATH = OUTPUT_DIR / ".gitignore"
if not GITIGNORE_PATH.exists():
    with open(GITIGNORE_PATH, "w") as f:
        f.write("# Ignore all files in this directory\n*\n!.gitignore\n")


async def example_flowchart():
    """
    Example of rendering a flowchart diagram
    
    フローチャート図の描画例
    """
    print("Rendering flowchart diagram...")
    
    # Load the flowchart from file
    # ファイルからフローチャートを読み込む
    input_file = Path(__file__).parent / "flowchart.mmd"
    with open(input_file, "r", encoding="utf-8") as f:
        definition = f.read()
    
    # Render to SVG with forest theme
    # フォレストテーマでSVGに描画
    title, desc, svg_data = await render_mermaid(
        definition,
        output_format="svg",
        background_color="white",
        mermaid_config={"theme": "forest"}
    )
    
    # Save the SVG data to a file
    # SVGデータをファイルに保存
    output_file = OUTPUT_DIR / "flowchart.svg"
    with open(output_file, "wb") as f:
        f.write(svg_data)
    
    print(f"Flowchart rendered to {output_file}")


async def example_sequence_diagram():
    """
    Example of rendering a sequence diagram
    
    シーケンス図の描画例
    """
    print("Rendering sequence diagram...")
    
    # Load the sequence diagram from file
    # ファイルからシーケンス図を読み込む
    input_file = Path(__file__).parent / "sequence.mmd"
    
    # Render to PNG with dark theme
    # ダークテーマでPNGに描画
    output_file = OUTPUT_DIR / "sequence.png"
    await render_mermaid_file(
        input_file=str(input_file),
        output_file=str(output_file),
        output_format="png",
        mermaid_config={"theme": "dark"},
        background_color="#333333"
    )
    
    print(f"Sequence diagram rendered to {output_file}")


async def example_class_diagram():
    """
    Example of rendering a class diagram
    
    クラス図の描画例
    """
    print("Rendering class diagram...")
    
    # Load the class diagram from file
    # ファイルからクラス図を読み込む
    input_file = Path(__file__).parent / "class.mmd"
    
    # Render to PDF
    # PDFに描画
    output_file = OUTPUT_DIR / "class.pdf"
    await render_mermaid_file(
        input_file=str(input_file),
        output_file=str(output_file),
        output_format="pdf",
        mermaid_config={"theme": "default"}
    )
    
    print(f"Class diagram rendered to {output_file}")


async def example_markdown_processing():
    """
    Example of processing a markdown file with embedded mermaid diagrams
    
    埋め込みmermaid図を含むmarkdownファイルの処理例
    """
    print("Processing markdown file...")
    
    # Load the markdown file
    # Markdownファイルを読み込む
    input_file = Path(__file__).parent / "example.md"
    
    # Process the markdown file and replace mermaid code blocks with images
    # Markdownファイルを処理し、mermaidコードブロックを画像に置き換え
    output_file = OUTPUT_DIR / "example_processed.md"
    await render_mermaid_file(
        input_file=str(input_file),
        output_file=str(output_file),
        output_format="svg"
    )
    
    print(f"Markdown file processed to {output_file}")
    print("Generated SVG files are saved alongside the markdown file")


async def example_with_custom_css():
    """
    Example of rendering with custom CSS
    
    カスタムCSSでの描画例
    """
    print("Rendering with custom CSS...")
    
    # Define custom CSS
    # カスタムCSSを定義
    custom_css = """
    .node rect {
        fill: #ccffcc;
        stroke: #99cc99;
        stroke-width: 2px;
    }
    .edgePath path {
        stroke: #007700;
        stroke-width: 2px;
    }
    """
    
    # Load the flowchart from file
    # ファイルからフローチャートを読み込む
    input_file = Path(__file__).parent / "flowchart.mmd"
    with open(input_file, "r", encoding="utf-8") as f:
        definition = f.read()
    
    # Render to SVG with custom CSS
    # カスタムCSSでSVGに描画
    title, desc, svg_data = await render_mermaid(
        definition,
        output_format="svg",
        css=custom_css
    )
    
    # Save the SVG data to a file
    # SVGデータをファイルに保存
    output_file = OUTPUT_DIR / "flowchart_custom_css.svg"
    with open(output_file, "wb") as f:
        f.write(svg_data)
    
    print(f"Flowchart with custom CSS rendered to {output_file}")


async def example_with_custom_config():
    """
    Example of rendering with custom configuration
    
    カスタム設定での描画例
    """
    print("Rendering with custom configuration...")
    
    # Define custom configuration
    # カスタム設定を定義
    custom_config = {
        "theme": "neutral",
        "themeVariables": {
            "primaryColor": "#6699cc",
            "primaryTextColor": "#fff",
            "primaryBorderColor": "#336699",
            "lineColor": "#336699",
            "secondaryColor": "#ffcc66",
            "tertiaryColor": "#fff"
        }
    }
    
    # Load the flowchart from file
    # ファイルからフローチャートを読み込む
    input_file = Path(__file__).parent / "flowchart.mmd"
    
    # Render to SVG with custom configuration
    # カスタム設定でSVGに描画
    output_file = OUTPUT_DIR / "flowchart_custom_config.svg"
    await render_mermaid_file(
        input_file=str(input_file),
        output_file=str(output_file),
        output_format="svg",
        mermaid_config=custom_config
    )
    
    print(f"Flowchart with custom configuration rendered to {output_file}")


async def main():
    """
    Run all examples
    
    すべての例を実行
    """
    print("Mermaid CLI Python Examples")
    print("==========================")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    
    # Create example mermaid files if they don't exist
    # 例のmermaidファイルが存在しない場合は作成
    create_example_files()
    
    # Run all examples
    # すべての例を実行
    await example_flowchart()
    print()
    
    await example_sequence_diagram()
    print()
    
    await example_class_diagram()
    print()
    
    await example_markdown_processing()
    print()
    
    await example_with_custom_css()
    print()
    
    await example_with_custom_config()
    print()
    
    print("All examples completed successfully!")


def create_example_files():
    """
    Create example mermaid files if they don't exist
    
    例のmermaidファイルが存在しない場合は作成
    """
    example_dir = Path(__file__).parent
    
    # Flowchart example
    # フローチャートの例
    flowchart_file = example_dir / "flowchart.mmd"
    if not flowchart_file.exists():
        with open(flowchart_file, "w", encoding="utf-8") as f:
            f.write("""graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
""")
    
    # Sequence diagram example
    # シーケンス図の例
    sequence_file = example_dir / "sequence.mmd"
    if not sequence_file.exists():
        with open(sequence_file, "w", encoding="utf-8") as f:
            f.write("""sequenceDiagram
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
""")
    
    # Class diagram example
    # クラス図の例
    class_file = example_dir / "class.mmd"
    if not class_file.exists():
        with open(class_file, "w", encoding="utf-8") as f:
            f.write("""classDiagram
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
""")
    
    # Markdown example
    # Markdownの例
    markdown_file = example_dir / "example.md"
    if not markdown_file.exists():
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write("""# Example Markdown with Mermaid

This is a markdown file with embedded mermaid diagrams.

## Flowchart

```mermaid
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
```

## Sequence Diagram

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

## Class Diagram

```mermaid
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
```
""")


if __name__ == "__main__":
    asyncio.run(main())
