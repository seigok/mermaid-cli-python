import asyncio
import io

import pytest
from PIL import Image

from mermaid_cli import render_mermaid


# Diagram types documented in Mermaid syntax pages (representative minimal snippets)
DIAGRAMS = {
    "flowchart": """flowchart TD
  A[Start] --> B{Decision}
  B -->|Yes| C[Do it]
  B -->|No| D[Stop]
""",
    "sequence": """sequenceDiagram
  participant A as Alice
  participant B as Bob
  A->>B: Hello Bob
  B-->>A: Hi Alice
""",
    "class": """classDiagram
  class Animal
  Animal : +String name
  Animal : +eat()
  class Dog
  Dog --|> Animal
""",
    "state": """stateDiagram-v2
  [*] --> Still
  Still --> [*]
""",
    "er": """erDiagram
  CUSTOMER ||--o{ ORDER : places
  CUSTOMER {
    string name
  }
  ORDER {
    int id
  }
""",
    "journey": """journey
  title My day
  section Morning
    Eat: 5: Me
    Code: 3: Me
""",
    "gantt": """gantt
  title A Gantt Diagram
  dateFormat  YYYY-MM-DD
  section Section
  A task           :a1, 2024-01-01, 3d
""",
    "pie": """pie title Pets
  "Dogs" : 40
  "Cats" : 35
  "Birds" : 25
""",
    "requirement": """requirementDiagram
  requirement test_req {
    id: 1
    text: example
    risk: Low
    verifymethod: Test
  }
""",
    "gitgraph": """gitGraph
  commit
  branch develop
  checkout develop
  commit
""",
    "c4context": """C4Context
    title System Context diagram for Internet Banking System
    Person(customerA, "Customer A", "A customer")
    System(banking_system, "Internet Banking System", "Allows users")
    Rel(customerA, banking_system, "Uses")
""",
    "mindmap": """mindmap
  root((mindmap))
    A
    B
""",
    "timeline": """timeline
  title Mermaid Timeline
  2024 : Project start
  2025 : v1 release
""",
    "zenuml": """zenuml
  title Order Service
  @Actor Client
  @Boundary API
  Client->API: createOrder()
""",
    "quadrant": """quadrantChart
  title Reach and engagement
  x-axis Low Reach --> High Reach
  y-axis Low Engagement --> High Engagement
  quadrant-1 We should expand
  A: [0.3, 0.6]
""",
    "xychart": """xychart-beta
  title "Sales Revenue"
  x-axis [Jan, Feb, Mar]
  y-axis "Revenue" 0 --> 100
  bar [10, 20, 35]
""",
    "sankey": """sankey-beta
  source,target,value
  A,B,10
  B,C,7
""",
    "block": """block-beta
  columns 2
  A B
  C D
""",
    "architecture": """architecture-beta
  group api(cloud)[API]
  service db(database)[Database] in api
""",
    "packet": """packet
  0-3: "Version"
  4-7: "IHL"
  8-15: "Type"
""",
    "kanban": """kanban
  title Project Board
  section Todo
    Task A
  section Doing
    Task B
""",
    "treemap": """treemap-beta
  title Disk Usage
  "root" : 100
  "apps" : 40
  "data" : 60
""",
    "radar": """radar-beta
  axis a,b,c
  curve c1{1,2,3}
""",
}


def _non_white_pixels(png_bytes: bytes) -> int:
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    count = 0
    for r, g, b, a in img.getdata():
        if a > 0 and not (r > 245 and g > 245 and b > 245):
            count += 1
    return count


@pytest.mark.parametrize("name,definition", DIAGRAMS.items())
def test_mermaid_diagram_syntax_renders_non_blank(name, definition):
    _, _, png = asyncio.run(render_mermaid(definition, output_format="png", quiet=True))
    non_white = _non_white_pixels(png)
    assert non_white > 100, f"{name} diagram rendered blank/near-blank (non_white={non_white})"
