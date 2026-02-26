import asyncio

import pytest

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
  "Disk Usage"
    "Applications"
      "Editor": 18
      "Browser": 22
    "Data"
      "Photos": 35
      "Docs": 25
""",
    "radar": """radar-beta
  axis a,b,c
  curve c1{1,2,3}
""",
}


# Japanese coverage for all diagram types: (definition, expected Japanese token in rendered SVG)
DIAGRAMS_JA = {
    "flowchart": (
        """flowchart TD
  A[開始] --> B{判定}
  B -->|はい| C[実行]
  B -->|いいえ| D[停止]
""",
        "開始",
    ),
    "sequence": (
        """sequenceDiagram
  participant A as 太郎
  participant B as 花子
  A->>B: こんにちは
  B-->>A: 了解です
""",
        "こんにちは",
    ),
    "class": (
        """classDiagram
  class 動物
  動物 : +名前
  動物 : +食べる()
  class 犬
  犬 --|> 動物
""",
        "動物",
    ),
    "state": (
        """stateDiagram-v2
  [*] --> 待機
  待機 --> [*]
""",
        "待機",
    ),
    "er": (
        """erDiagram
  顧客 ||--o{ 注文 : 注文する
  顧客 {
    string 名前
  }
  注文 {
    int 注文ID
  }
""",
        "顧客",
    ),
    "journey": (
        """journey
  title ある一日
  section 午前
    朝食: 5: 私
    開発: 4: 私
""",
        "ある一日",
    ),
    "gantt": (
        """gantt
  title 開発計画
  dateFormat  YYYY-MM-DD
  section 開発
  実装           :a1, 2024-01-01, 3d
""",
        "開発計画",
    ),
    "pie": (
        """pie title 好きな動物
  "犬" : 40
  "猫" : 35
  "鳥" : 25
""",
        "好きな動物",
    ),
    "requirement": (
        """requirementDiagram
  requirement req_jp {
    id: 1
    text: "日本語の要件"
    risk: Low
    verifymethod: Test
  }
""",
        "日本語の要件",
    ),
    "gitgraph": (
        """gitGraph
  commit id: "c1" tag: "日本語"
  branch develop
  checkout develop
  commit id: "c2"
""",
        "日本語",
    ),
    "c4context": (
        """C4Context
    title インターネットバンキングのコンテキスト
    Person(customerA, "顧客", "利用者")
    System(banking_system, "バンキングシステム", "取引を処理")
    Rel(customerA, banking_system, "利用する")
""",
        "顧客",
    ),
    "mindmap": (
        """mindmap
  root((中心))
    設計
    実装
""",
        "中心",
    ),
    "timeline": (
        """timeline
  title 開発タイムライン
  2024 : 開始
  2025 : 公開
""",
        "開発タイムライン",
    ),
    "zenuml": (
        """zenuml
  title 注文サービス
  @Actor 利用者
  @Boundary API
  利用者->API: 注文する()
""",
        "注文サービス",
    ),
    "quadrant": (
        """quadrantChart
  title "到達度と反応"
  x-axis "Low" --> "High"
  y-axis "Low" --> "High"
  quadrant-1 "強化領域"
  A: [0.3, 0.6]
""",
        "強化領域",
    ),
    "xychart": (
        """xychart-beta
  title "売上"
  x-axis ["1月", "2月", "3月"]
  y-axis "金額" 0 --> 100
  bar [10, 20, 35]
""",
        "売上",
    ),
    "sankey": (
        """sankey-beta
  source,target,value
  開発,レビュー,10
  レビュー,本番,7
""",
        "開発",
    ),
    "block": (
        """block-beta
  columns 2
  左 右
  上 下
""",
        "左",
    ),
    "architecture": (
        """architecture-beta
  group platform(cloud)[基盤]
  service db(database)[データベース] in platform
""",
        "基盤",
    ),
    "packet": (
        """packet
  0-3: "版"
  4-7: "ヘッダ長"
  8-15: "種別"
""",
        "ヘッダ長",
    ),
    "kanban": (
        """kanban
  title 開発ボード
  section 未着手
    タスクA
  section 進行中
    タスクB
""",
        "開発ボード",
    ),
    "treemap": (
        """treemap-beta
  "ディスク使用量"
    "アプリ"
      "エディタ": 18
      "ブラウザ": 22
    "データ"
      "写真": 35
      "文書": 25
""",
        "ディスク使用量",
    ),
    "radar": (
        """radar-beta
  axis q["品質"], s["速度"], st["安定性"]
  curve current["現状"]{70,60,80}
""",
        "品質",
    ),
}


def _is_non_blank_svg(svg_text: str) -> bool:
    # A practical non-blank signal without external image deps:
    # rendered svg exists and has at least one visible shape/text primitive.
    if "<svg" not in svg_text:
        return False
    primitives = ("<path", "<rect", "<circle", "<ellipse", "<polygon", "<polyline", "<line", "<text")
    return any(tag in svg_text for tag in primitives)


@pytest.mark.parametrize("name,definition", DIAGRAMS.items())
def test_mermaid_diagram_syntax_renders_non_blank(name, definition):
    _, _, svg = asyncio.run(render_mermaid(definition, output_format="svg", quiet=True))
    svg_text = svg.decode("utf-8", errors="replace")
    assert _is_non_blank_svg(svg_text), f"{name} diagram rendered blank/invalid svg"


@pytest.mark.parametrize("name,payload", DIAGRAMS_JA.items())
def test_mermaid_diagram_supports_japanese_text(name, payload):
    definition, expected_text = payload
    _, _, svg = asyncio.run(render_mermaid(definition, output_format="svg", quiet=True))
    svg_text = svg.decode("utf-8", errors="replace")
    assert _is_non_blank_svg(svg_text), f"{name} diagram rendered blank/invalid svg for Japanese text"
    assert expected_text in svg_text, f"{name} diagram did not keep Japanese text token: {expected_text}"
