"""
Chart information for Mermaid MCP
Contains details and examples for each chart type
"""

from typing import Dict, Any

# Chart type information
CHART_TYPES: Dict[str, Dict[str, Any]] = {
    "flowchart": {
        "description": "Directed nodes & edges for process flows",
        "required_input": "`graph LR`/`TD`, node definitions, arrows (`A-->B`)",
        "example": "```mermaid\ngraph TD\n  A[Start] --> B[Step] --> C[End]\n```"
    },
    "basic-flowchart": {
        "description": "Minimal flowchart",
        "required_input": "Same as Flowchart",
        "example": "```mermaid\ngraph LR\n  X --> Y\n```"
    },
    "styled-flowchart": {
        "description": "Flowchart with custom styles",
        "required_input": "Nodes, links, plus style directives (`class`, `style`)",
        "example": "```mermaid\ngraph LR\n  A --> B\n  class A fill:#f9f,stroke:#333\n```"
    },
    "sequence": {
        "description": "Time‑ordered messages between actors",
        "required_input": "`sequenceDiagram`, `participant`, arrows (`A->>B:`)",
        "example": "```mermaid\nsequenceDiagram\n  Alice->>Bob: Hello\n```"
    },
    "basic-sequence": {
        "description": "Minimal sequence chart",
        "required_input": "Same as Sequence Diagram",
        "example": "```mermaid\nsequenceDiagram\n  A->B: Hi\n```"
    },
    "loop-sequence": {
        "description": "Control blocks (loops, alternatives, optional)",
        "required_input": "`loop`, `alt`, `opt` blocks around messages",
        "example": "```mermaid\nsequenceDiagram\n  loop every day\n    A->>B: Ping\n  end\n```"
    },
    "self-sequence": {
        "description": "Self‑referential messaging",
        "required_input": "Self arrow (`A->>A:`) inside `loop`",
        "example": "```mermaid\nsequenceDiagram\n  loop 3x\n    A->>A: repeat\n  end\n```"
    },
    "class": {
        "description": "UML‑style classes and relations",
        "required_input": "`classDiagram`, class names, relationships (`--|>`)",
        "example": "```mermaid\nclassDiagram\n  Animal <|-- Dog\n  Dog : bark()\n```"
    },
    "state": {
        "description": "States and transitions",
        "required_input": "`stateDiagram-v2`, states, arrows",
        "example": "```mermaid\nstateDiagram-v2\n  [*] --> Idle\n  Idle --> Active\n```"
    },
    "er": {
        "description": "ER‑model showing entities & cardinalities",
        "required_input": "`erDiagram`, entity names, relationships",
        "example": "```mermaid\nerDiagram\n  USER ||--o{ ORDER : places\n```"
    },
    "journey": {
        "description": "Steps a user takes through a flow",
        "required_input": "`journey`, `section`, steps (`\"Step\" : 5`)",
        "example": "```mermaid\njourney\n  title My Journey\n  section Start\n    Go to site: 5\n```"
    },
    "gantt": {
        "description": "Project timeline with dates or durations",
        "required_input": "`gantt`, `dateFormat`, tasks (`Task :a, YYYY-MM-DD, 3d`)",
        "example": "```mermaid\ngantt\n  dateFormat  YYYY-MM-DD\n  A :a, 2025-05-01, 3d\n```"
    },
    "timeline": {
        "description": "Sequential events on a date axis",
        "required_input": "`timeline`, events (`Event :date`)",
        "example": "```mermaid\ntimeline\n  2025-05-01 : Launch\n```"
    },
    "pie": {
        "description": "Proportional slices",
        "required_input": "`pie`, label-value pairs",
        "example": "```mermaid\npie\n  title Pets\n  \"Dogs\" : 5\n  \"Cats\" : 3\n```"
    },
    "basic-pie": {
        "description": "Minimal pie chart",
        "required_input": "Same as Pie Chart",
        "example": "```mermaid\npie\n  \"A\":2\n  \"B\":3\n```"
    },
    "quadrant": {
        "description": "Four‑quadrant scatter",
        "required_input": "`quadrantChart`, axis labels, data points",
        "example": "```mermaid\nquadrantChart\n  xAxis \"Speed\" \"High\"\n  yAxis \"Power\" \"Strong\"\n```"
    },
    "xy": {
        "description": "X–Y scatter or line plot",
        "required_input": "`xyChart`, axis defs, `dataSeries`",
        "example": "```mermaid\nxyChart xAxis=\"Day\" yAxis=\"Temp\"\n  dataSeries \"T\": [1,2,3]\n```"
    },
    "sankey": {
        "description": "Flow volumes between nodes",
        "required_input": "`sankey`, node defs, link widths",
        "example": "```mermaid\nsankey\n  A[Source] 10-> B[Target]\n```"
    },
    "block": {
        "description": "Rectangular blocks & connections",
        "required_input": "`blockdiag`, block and edge definitions",
        "example": "```mermaid\nblockdiag\n  A -> B\n```"
    },
    "packet": {
        "description": "Network packet fields layout",
        "required_input": "`packetdiag`, packet structure",
        "example": "```mermaid\npacketdiag\n  packet { header; payload; }\n```"
    },
    "kanban": {
        "description": "Board columns and cards",
        "required_input": "`kanban`, `column`, `card`",
        "example": "```mermaid\nkanban\n  column Backlog\n    card Task1\n```"
    },
    "requirement": {
        "description": "SysML requirements and relations",
        "required_input": "`requirementDiagram`, `requirement`, links",
        "example": "```mermaid\nrequirementDiagram\n  requirement R1\n```"
    },
    "git": {
        "description": "Git commit history",
        "required_input": "`gitGraph`, `commit`, branching commands",
        "example": "```mermaid\ngitGraph\n  commit\n  branch feature\n```"
    },
    "gitgraph": {
        "description": "Git commit history",
        "required_input": "`gitGraph`, `commit`, branching commands",
        "example": "```mermaid\ngitGraph\n  commit\n  branch feature\n```"
    },
    "commit-flow": {
        "description": "Simplified Git flow",
        "required_input": "Same as Gitgraph",
        "example": "```mermaid\ngitGraph\n  commit id:\"init\"\n```"
    },
    "c4": {
        "description": "Software architecture C4 levels",
        "required_input": "`C4Context`/`C4Component`, `Person`, `System`",
        "example": "```mermaid\nC4Context\n  Person(user, \"User\")\n```"
    },
    "architecture": {
        "description": "High‑level system layout",
        "required_input": "`architectureDiagram`, components",
        "example": "```mermaid\narchitectureDiagram\n  Component A --> B\n```"
    },
    "mindmap": {
        "description": "Tree of ideas",
        "required_input": "`mindmap`, root, sub-branches",
        "example": "```mermaid\nmindmap\n  root((Idea))\n    sub1((A))\n```"
    },
    "zenuml": {
        "description": "Lightweight UML-style",
        "required_input": "`zenuml`, `actor`, `usecase`",
        "example": "```mermaid\nzenuml\n  actor User\n```"
    },
    "radar": {
        "description": "Radial comparison chart",
        "required_input": "`radar`, `title`, axes, data",
        "example": "```mermaid\nradar\n  title Skills\n  Data: [3,4,2]\n```"
    }
}

# Configuration for each chart type
CHART_CONFIG: Dict[str, Dict[str, Any]] = {
    "flowchart": {
        "curve": "linear",
        "nodeSpacing": 50,
        "rankSpacing": 50,
        "useMaxWidth": True
    },
    "sequence": {
        "actorMargin": 50,
        "boxMargin": 10,
        "boxTextMargin": 5,
        "noteMargin": 10,
        "messageMargin": 35
    },
    "class": {
        "nodeSpacing": 50,
        "useMaxWidth": True
    },
    "state": {
        "useMaxWidth": True
    },
    "er": {
        "entityPadding": 15,
        "useMaxWidth": True
    },
    "gantt": {
        "barHeight": 20,
        "barGap": 4,
        "topPadding": 50
    },
    "pie": {
        "useWidth": 800
    }
} 