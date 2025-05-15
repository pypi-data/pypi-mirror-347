"""
Server module for Mermaid MCP
Implements the HTTP server with REST API endpoints
"""

import os
import logging
import json
import tempfile
from typing import Optional, Dict, Any, List, Union
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from mermaid_mcp.utils import run_mmdc, find_chart_info, is_valid_chart_type, get_download_dir, list_css_themes, read_css_theme, css_to_theme_variables, list_json_themes, load_json_theme, DEBUG_THEMES

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mermaid-mcp")

app = FastAPI(
    title="Mermaid MCP",
    description="Model Context Protocol server for Mermaid diagrams",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class MermaidRequest(BaseModel):
    input: str
    css: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    output: Optional[str] = None
    background_color: Optional[str] = None
    css_theme: Optional[str] = None
    json_theme: Optional[str] = None

class ValidationResponse(BaseModel):
    valid: bool
    message: Optional[str] = None

class HelpResponse(BaseModel):
    chart_types: List[str]
    examples: Dict[str, str]
    description: str


@app.get("/")
async def root():
    """Root endpoint that returns basic server info"""
    return {
        "name": "Mermaid MCP",
        "version": "0.1.0",
        "endpoints": [
            "/validate/{chart_type}",
            "/generate/{chart_type}",
            "/generate",
            "/download/{chart_type}",
            "/download",
            "/help/{chart_type}",
            "/help",
            "/themes"
        ]
    }


@app.post("/validate/{chart_type}", response_model=ValidationResponse)
async def validate_chart(chart_type: str, request: MermaidRequest):
    """Validate a mermaid diagram of the specified chart type"""
    # Check if chart type is valid
    if not is_valid_chart_type(chart_type):
        raise HTTPException(status_code=400, detail=f"Invalid chart type: {chart_type}")
    
    # Create a temporary file with the mermaid content
    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False) as tmp:
        tmp.write(request.input)
        tmp_path = tmp.name
    
    try:
        # Create a config file if provided
        config_path = None
        if request.config:
            with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as cfg:
                json.dump(request.config, cfg)
                config_path = cfg.name
        
        # Run mmdc with validate option
        result, output = run_mmdc(tmp_path, validate=True, config_file=config_path)
        
        if result:
            return {"valid": True}
        else:
            return {"valid": False, "message": output}
    finally:
        # Clean up temporary files
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if config_path and os.path.exists(config_path):
            os.unlink(config_path)


@app.post("/generate/{chart_type}")
async def generate_chart(chart_type: str, request: MermaidRequest):
    """Generate a chart image from mermaid code"""
    # Check if chart type is valid
    if not is_valid_chart_type(chart_type):
        raise HTTPException(status_code=400, detail=f"Invalid chart type: {chart_type}")
    
    # Create a temporary file with the mermaid content
    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False) as tmp:
        tmp.write(request.input)
        tmp_path = tmp.name
    
    # Determine output format (svg, png, pdf)
    output_format = "svg"
    if request.output and "." in request.output:
        ext = request.output.split(".")[-1].lower()
        if ext in ["svg", "png", "pdf"]:
            output_format = ext
    
    # Create temporary output file
    with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as out:
        output_path = out.name
    
    try:
        # Create a config file if provided
        config_path = None
        if request.config:
            with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as cfg:
                json.dump(request.config, cfg)
                config_path = cfg.name
        
        # Handle CSS - either direct CSS or theme
        css_path = None
        if request.css:
            with tempfile.NamedTemporaryFile(suffix=".css", mode="w", delete=False) as css:
                css.write(request.css)
                css_path = css.name
        
        # Run mmdc to generate the chart
        result, error_output = run_mmdc(
            tmp_path, 
            output_path=output_path, 
            config_file=config_path, 
            css_file=css_path,
            background_color=request.background_color,
            css_theme_name=request.css_theme,
            json_theme_name=request.json_theme
        )
        
        if not result:
            raise HTTPException(status_code=400, detail=f"Failed to generate chart: {error_output}")
        
        # Return the file
        return FileResponse(
            output_path,
            media_type=f"image/{output_format}" if output_format != "pdf" else "application/pdf",
            filename=f"chart.{output_format}"
        )
    finally:
        # Clean up temporary files
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if config_path and os.path.exists(config_path):
            os.unlink(config_path)
        if css_path and request.css and os.path.exists(css_path):
            os.unlink(css_path)
        # Don't delete output_path as it's being returned


@app.post("/generate")
async def generate_chart_auto(request: MermaidRequest):
    """Generate a chart image without explicitly specifying chart type"""
    # Automatically determine chart type from the input
    chart_type = None
    for line in request.input.splitlines():
        line = line.strip()
        if line and not line.startswith("%%"):
            if "graph " in line or "flowchart " in line:
                chart_type = "flowchart"
            elif "sequenceDiagram" in line:
                chart_type = "sequence"
            elif "classDiagram" in line:
                chart_type = "class"
            elif "stateDiagram" in line or "stateDiagram-v2" in line:
                chart_type = "state"
            elif "erDiagram" in line:
                chart_type = "er"
            elif "gantt" in line:
                chart_type = "gantt"
            elif "pie" in line:
                chart_type = "pie"
            # Add more chart types as needed
            break
    
    if not chart_type:
        raise HTTPException(status_code=400, detail="Could not determine chart type from input")
    
    return await generate_chart(chart_type, request)


@app.post("/download/{chart_type}")
async def download_chart(chart_type: str, request: MermaidRequest):
    """Generate and download a chart of the specified type"""
    # Get download directory from environment or use default
    download_dir = get_download_dir()
    
    # Check if chart type is valid
    if not is_valid_chart_type(chart_type):
        raise HTTPException(status_code=400, detail=f"Invalid chart type: {chart_type}")
    
    # Create a temporary file with the mermaid content
    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False) as tmp:
        tmp.write(request.input)
        tmp_path = tmp.name
    
    # Determine output format and filename
    output_format = "svg"
    filename = f"chart_{chart_type}"
    
    if request.output:
        if "." in request.output:
            filename, ext = os.path.splitext(os.path.basename(request.output))
            ext = ext.lstrip(".")
            if ext in ["svg", "png", "pdf"]:
                output_format = ext
        else:
            filename = request.output
    
    output_file = f"{filename}.{output_format}"
    output_path = os.path.join(download_dir, output_file)
    
    try:
        # Create a config file if provided
        config_path = None
        if request.config:
            with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as cfg:
                json.dump(request.config, cfg)
                config_path = cfg.name
        
        # Handle CSS - either direct CSS or theme
        css_path = None
        if request.css:
            with tempfile.NamedTemporaryFile(suffix=".css", mode="w", delete=False) as css:
                css.write(request.css)
                css_path = css.name
        
        # Run mmdc to generate the chart
        result, error_output = run_mmdc(
            tmp_path, 
            output_path=output_path, 
            config_file=config_path, 
            css_file=css_path,
            background_color=request.background_color,
            css_theme_name=request.css_theme,
            json_theme_name=request.json_theme
        )
        
        if not result:
            raise HTTPException(status_code=400, detail=f"Failed to generate chart: {error_output}")
        
        return {
            "success": True,
            "file_path": output_path,
            "file_name": output_file
        }
    finally:
        # Clean up temporary files
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if config_path and os.path.exists(config_path):
            os.unlink(config_path)
        if css_path and request.css and os.path.exists(css_path):
            os.unlink(css_path)


@app.post("/download")
async def download_chart_auto(request: MermaidRequest):
    """Generate and download a chart without explicitly specifying chart type"""
    # Automatically determine chart type from the input
    chart_type = None
    for line in request.input.splitlines():
        line = line.strip()
        if line and not line.startswith("%%"):
            if "graph " in line or "flowchart " in line:
                chart_type = "flowchart"
            elif "sequenceDiagram" in line:
                chart_type = "sequence"
            elif "classDiagram" in line:
                chart_type = "class"
            elif "stateDiagram" in line or "stateDiagram-v2" in line:
                chart_type = "state"
            elif "erDiagram" in line:
                chart_type = "er"
            elif "gantt" in line:
                chart_type = "gantt"
            elif "pie" in line:
                chart_type = "pie"
            # Add more chart types as needed
            break
    
    if not chart_type:
        raise HTTPException(status_code=400, detail="Could not determine chart type from input")
    
    return await download_chart(chart_type, request)


@app.get("/help/{chart_type}")
async def chart_help(chart_type: str):
    """Get help information for a specific chart type"""
    # Check if chart type is valid
    if not is_valid_chart_type(chart_type):
        raise HTTPException(status_code=400, detail=f"Invalid chart type: {chart_type}")
    
    # Get chart info
    chart_info = find_chart_info(chart_type)
    if not chart_info:
        raise HTTPException(status_code=404, detail=f"Help not available for chart type: {chart_type}")
    
    return {
        "chart_type": chart_type,
        "description": chart_info.get("description", ""),
        "required_input": chart_info.get("required_input", ""),
        "example": chart_info.get("example", "")
    }


@app.get("/help")
async def general_help():
    """Get general help information and a list of available charts"""
    chart_types = []
    examples = {}
    
    # Get all chart types from the chart_info module
    from mermaid_mcp.chart_info import CHART_TYPES
    
    for chart_type, info in CHART_TYPES.items():
        chart_types.append(chart_type)
        examples[chart_type] = info.get("example", "")
    
    return {
        "chart_types": chart_types,
        "examples": examples,
        "description": "Mermaid is a JavaScript-based diagramming and charting tool that renders Markdown-inspired text definitions to create diagrams."
    }


@app.get("/themes")
async def list_themes():
    """List all available CSS themes and JSON theme configurations"""
    from mermaid_mcp.utils import (
        list_css_themes, read_css_theme, css_to_theme_variables,
        list_json_themes, load_json_theme, DEBUG_THEMES
    )
    
    # Get CSS themes
    css_themes = list_css_themes()
    logger.info(f"Detected CSS themes: {list(css_themes.keys())}")
    
    # Get JSON themes
    json_themes = list_json_themes()
    logger.info(f"Detected JSON themes: {list(json_themes.keys())}")
    
    result = {
        "available_css_themes": list(css_themes.keys()),
        "available_json_themes": list(json_themes.keys()),
        "built_in_themes": ["default", "forest", "dark", "neutral", "base"],
        "css_themes_details": {},
        "json_themes_details": {}
    }
    
    # Process CSS themes
    for theme_name, theme_path in css_themes.items():
        css_content = read_css_theme(theme_name)
        if css_content:
            theme_variables = css_to_theme_variables(css_content)
            
            # Get a sample of the CSS
            css_preview = css_content[:200] + "..." if len(css_content) > 200 else css_content
            
            result["css_themes_details"][theme_name] = {
                "path": theme_path,
                "preview": css_preview,
                "variables": theme_variables,
                "variable_count": len(theme_variables)
            }
            
            if DEBUG_THEMES:
                logger.info(f"CSS theme {theme_name}: {len(theme_variables)} variables mapped")
    
    # Process JSON themes
    for theme_name, theme_path in json_themes.items():
        theme_data = load_json_theme(theme_name)
        if theme_data:
            # Extract variables if present
            theme_variables = theme_data.get("themeVariables", {})
            
            result["json_themes_details"][theme_name] = {
                "path": theme_path,
                "theme": theme_data.get("theme", "base"),
                "variables": theme_variables,
                "variable_count": len(theme_variables)
            }
            
            if DEBUG_THEMES:
                logger.info(f"JSON theme {theme_name}: {len(theme_variables)} variables defined")
    
    return result


def start_server(protocol: str = "http", port: int = 27312, log_dir: Optional[str] = None) -> int:
    """Start the MCP server with the specified protocol and port."""
    if protocol == "http":
        logger.info(f"Starting HTTP server on port {port}")
        try:
            uvicorn.run(app, host="0.0.0.0", port=port)
            return 0
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return 1
    else:
        logger.error(f"Protocol {protocol} not yet implemented")
        return 1 