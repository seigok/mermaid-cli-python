# Mermaid CLI (Python)

A command-line interface and Python library for [mermaid](https://mermaidjs.github.io/), which allows you to generate diagrams and flowcharts from text.

This code has been ported to Python from the following library:
https://github.com/mermaid-js/mermaid-cli

## Features

- Render Mermaid diagrams to SVG, PNG, or PDF formats
- Process Markdown files with embedded Mermaid diagrams
- Use as a command-line tool or Python library
- Customize output with themes, colors, and CSS
- Support for icon packs

## Installation

```bash
pip install mermaid-cli
```

After installation, you need to install the Playwright browsers:

```bash
playwright install chromium
```

## Usage

### Command Line

```bash
# Simple diagram rendering
mmdc -i input.mmd -o output.svg

# Markdown file with mermaid diagrams
mmdc -i input.md -o output.md

# Customize output
mmdc -i input.mmd -o output.png -t dark -b transparent -w 1024 -H 768
```

### Python Library

```python
import asyncio
from mermaid_cli import render_mermaid, render_mermaid_file

# Render a diagram directly
async def render_diagram():
    definition = """
    graph TD
        A[Start] --> B{Is it?}
        B -->|Yes| C[OK]
        C --> D[Rethink]
        D --> B
        B ---->|No| E[End]
    """
    
    title, desc, svg_data = await render_mermaid(
        definition,
        output_format="svg",
        background_color="white",
        mermaid_config={"theme": "forest"}
    )
    
    with open("output.svg", "wb") as f:
        f.write(svg_data)

# Render from a file
async def render_file():
    await render_mermaid_file(
        input_file="input.mmd",
        output_file="output.svg",
        output_format="svg",
        mermaid_config={"theme": "dark"}
    )

# Run the async functions
asyncio.run(render_diagram())
asyncio.run(render_file())

# Or use the synchronous wrapper
from mermaid_cli import render_mermaid_file_sync

render_mermaid_file_sync(
    input_file="input.mmd",
    output_file="output.png",
    output_format="png"
)
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `-t, --theme [theme]` | Theme of the chart (default, forest, dark, neutral) |
| `-w, --width [width]` | Width of the page |
| `-H, --height [height]` | Height of the page |
| `-i, --input <input>` | Input mermaid file or markdown with mermaid code blocks |
| `-o, --output [output]` | Output file (svg, png, pdf, or md) |
| `-e, --output-format [format]` | Output format (svg, png, pdf) |
| `-b, --background-color [color]` | Background color (e.g., transparent, white, #F0F0F0) |
| `-c, --config-file [file]` | JSON configuration file for mermaid |
| `-C, --css-file [file]` | CSS file for styling the output |
| `-I, --svg-id [id]` | ID attribute for the SVG element |
| `-s, --scale [scale]` | Browser scale factor |
| `-f, --pdf-fit` | Scale PDF to fit chart |
| `-q, --quiet` | Suppress log output |
| `-p, --puppeteer-config-file [file]` | JSON configuration file for browser options |
| `--icon-packs <icons...>` | Icon packs to use (e.g., @iconify-json/logos) |

## API Reference

### render_mermaid

```python
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
    puppeteer_config: Dict[str, Any] = None,
) -> Tuple[Optional[str], Optional[str], bytes]
```

Renders a Mermaid diagram definition to the specified format.

**Parameters:**
- `definition`: Mermaid diagram definition string
- `output_format`: Output format (svg, png, pdf)
- `viewport`: Viewport dimensions (width, height, deviceScaleFactor)
- `background_color`: Background color
- `mermaid_config`: Mermaid configuration dictionary
- `css`: Custom CSS string
- `pdf_fit`: Scale PDF to fit chart
- `svg_id`: ID attribute for the SVG element
- `icon_packs`: List of icon packages to use
- `puppeteer_config`: Browser configuration dictionary

**Returns:**
A tuple of (title, description, data) where data is the binary content of the rendered diagram.

### render_mermaid_file

```python
async def render_mermaid_file(
    input_file: Optional[str],
    output_file: str,
    output_format: Optional[str] = None,
    puppeteer_config: Dict[str, Any] = None,
    quiet: bool = False,
    **kwargs
) -> None
```

Renders a Mermaid diagram from a file or processes a Markdown file with embedded Mermaid diagrams.

**Parameters:**
- `input_file`: Path to input file or None for stdin
- `output_file`: Path to output file
- `output_format`: Output format (svg, png, pdf)
- `puppeteer_config`: Browser configuration dictionary
- `quiet`: Suppress log output
- `**kwargs`: Additional options for render_mermaid

### render_mermaid_file_sync

```python
def render_mermaid_file_sync(
    input_file: Optional[str],
    output_file: str,
    output_format: Optional[str] = None,
    **kwargs
) -> None
```

Synchronous wrapper for render_mermaid_file.

## Examples

### Basic Flowchart

```
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
```

### Sequence Diagram

```
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```

### Class Diagram

```
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

## License

MIT
