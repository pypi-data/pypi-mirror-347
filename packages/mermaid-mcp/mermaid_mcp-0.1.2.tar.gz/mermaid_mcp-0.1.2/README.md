# Mermaid MCP

Model Context Protocol server for Mermaid diagrams.

## Overview

Mermaid-MCP provides a server and CLI interface for creating, validating, and rendering Mermaid diagrams. It uses the `mmdc` (Mermaid CLI) to generate static SVG, PNG, or PDF files from Mermaid diagram specifications.

## Features

- API server for diagram generation and validation
- CLI tool for local diagram rendering
- Custom theme support
- Multiple output formats (SVG, PNG, PDF)
- Support for all Mermaid diagram types

## Installation

```bash
# Using pip
pip install mermaid-mcp

# Using uv
uv pip install mermaid-mcp
```

## Usage

### CLI

```bash
# Generate a diagram
mermaid-mcp cli chart flowchart diagram.mmd output.svg

# Validate a diagram
mermaid-mcp cli validate flowchart diagram.mmd
```

### Server

```bash
# Start the server
mermaid-mcp server start

# Install as a launch agent (macOS)
mermaid-mcp server install --port=27312
```

## Theme Support

Mermaid-MCP supports several methods of applying themes to your diagrams:

1. Built-in Mermaid themes: "default", "forest", "dark", "neutral", "base"
2. Custom CSS themes from the `css/` directory
3. Custom JSON theme configurations in the `themes/` directory

### Using a Theme

#### In CLI mode

```bash
# Use a built-in theme
mermaid-mcp cli chart --theme=dark flowchart diagram.mmd output.svg

# Use a CSS theme
mermaid-mcp cli chart --css-theme=dark-mode flowchart diagram.mmd output.svg

# Use a JSON theme
mermaid-mcp cli chart --json-theme=forest-night flowchart diagram.mmd output.svg
```

#### In Server mode

```json
// Example request to /generate/flowchart
{
  "input": "graph TD\n  A[Start] --> B[End]",
  "css_theme": "dark-mode"
}
```

### Creating Custom Themes

#### CSS Themes

Create a CSS file in the `css/` directory with CSS variables for theming:

```css
/* my-theme.css */
:root {
  /* General theme */
  --mermaid-primary-color: #282a36;
  --mermaid-primary-border-color: #bd93f9;
  --mermaid-primary-text-color: #f8f8f2;
  
  /* Node styling */
  --mermaid-node-border: #bd93f9;
  --mermaid-node-background: #44475a;
  --mermaid-node-text: #f8f8f2;
  
  /* More variables... */
}
```

**Important**: CSS themes must use direct color values (hexadecimal, rgb, etc.) and not CSS variable references like `var(--name)`.

#### JSON Themes

Create a JSON file in the `themes/` directory:

```json
{
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#282a36",
    "primaryBorderColor": "#bd93f9",
    "primaryTextColor": "#f8f8f2",
    "secondaryColor": "#44475a",
    "lineColor": "#bd93f9",
    "nodeBorder": "#bd93f9",
    "darkMode": true
  }
}
```

## API Reference

### Endpoints

- `GET /themes` - List available themes
- `POST /generate/{chart_type}` - Generate a chart
- `POST /validate/{chart_type}` - Validate a chart
- `GET /help/{chart_type}` - Get help for a specific chart type

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/mermaid-mcp.git
cd mermaid-mcp

# Install dependencies
pip install -e .

# Run tests
python -m tests.test_themes
```

## License

[MIT](LICENSE)
