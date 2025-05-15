"""
CLI module for Mermaid MCP
Implements the CLI functions for chart generation and validation
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Union

from mermaid_mcp.utils import run_mmdc, is_valid_chart_type, get_temp_dir

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mermaid-mcp.cli")


def generate_chart(
    chart_type: str,
    input_path: str,
    output_path: Optional[str] = None,
    config_file: Optional[str] = None,
    css_file: Optional[str] = None,
    css_str: Optional[str] = None,
    background_color: Optional[str] = None,
    css_theme_name: Optional[str] = None,
    json_theme_name: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    theme: Optional[str] = None
) -> bool:
    """
    Generate a chart using the mmdc CLI
    
    Args:
        chart_type: Type of chart (flowchart, sequence, etc.)
        input_path: Path to input .mmd file or raw mermaid string or - for stdin
        output_path: Path to output file (will derive from input_path if not provided)
        config_file: Path to config file
        css_file: Path to CSS file
        css_str: CSS string
        background_color: Background color for the diagram
        css_theme_name: Name of a CSS theme to use
        json_theme_name: Name of a JSON theme to use
        width: Width of the output image
        height: Height of the output image
        theme: Built-in theme name (default, forest, dark, neutral)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Validate chart type
    if not is_valid_chart_type(chart_type):
        logger.error(f"Invalid chart type: {chart_type}")
        return False
    
    # Handle input from various sources
    input_file_path = None
    is_temp_input = False
    
    if input_path == '-':
        # Read from stdin
        input_content = sys.stdin.read()
        # Create temp file with the stdin content
        temp_dir = get_temp_dir()
        input_file_path = os.path.join(temp_dir, "stdin_input.mmd")
        with open(input_file_path, "w") as f:
            f.write(input_content)
        is_temp_input = True
    elif os.path.exists(input_path):
        # It's a file path
        input_file_path = input_path
    else:
        # Assume it's a string with Mermaid content
        temp_dir = get_temp_dir()
        input_file_path = os.path.join(temp_dir, "string_input.mmd")
        with open(input_file_path, "w") as f:
            f.write(input_path)
        is_temp_input = True
    
    # Derive output path if not provided
    if not output_path:
        if os.path.exists(input_path) and input_path != '-':
            output_path = os.path.splitext(input_path)[0] + ".svg"
        else:
            output_path = os.path.join(get_temp_dir(), "output.svg")
    
    # Handle CSS string
    css_file_path = css_file
    is_temp_css = False
    if css_str and not css_file:
        temp_dir = get_temp_dir()
        css_file_path = os.path.join(temp_dir, "style.css")
        with open(css_file_path, "w") as f:
            f.write(css_str)
        is_temp_css = True
    
    # Run mmdc
    try:
        result, error = run_mmdc(
            input_file=input_file_path,
            output_path=output_path,
            config_file=config_file,
            css_file=css_file_path,
            background_color=background_color,
            css_theme_name=css_theme_name,
            json_theme_name=json_theme_name,
            width=width,
            height=height,
            theme=theme
        )
        
        if not result:
            logger.error(f"Failed to generate chart: {error}")
            return False
        
        logger.info(f"Chart generated: {output_path}")
        return True
        
    finally:
        # Clean up temp files if we created them
        if is_temp_input and os.path.exists(input_file_path):
            try:
                os.unlink(input_file_path)
            except Exception as e:
                logger.warning(f"Failed to remove temporary input file: {e}")
        
        if is_temp_css and os.path.exists(css_file_path):
            try:
                os.unlink(css_file_path)
            except Exception as e:
                logger.warning(f"Failed to remove temporary CSS file: {e}")


def validate_chart(
    chart_type: str,
    input_path: str,
    config_file: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Validate a chart using the mmdc CLI
    
    Args:
        chart_type: Type of chart (flowchart, sequence, etc.)
        input_path: Path to input .mmd file or raw mermaid string or - for stdin
        config_file: Path to config file
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Validate chart type
    if not is_valid_chart_type(chart_type):
        return False, f"Invalid chart type: {chart_type}"
    
    # Handle input from various sources
    input_file_path = None
    is_temp_input = False
    
    if input_path == '-':
        # Read from stdin
        input_content = sys.stdin.read()
        # Create temp file with the stdin content
        temp_dir = get_temp_dir()
        input_file_path = os.path.join(temp_dir, "stdin_input.mmd")
        with open(input_file_path, "w") as f:
            f.write(input_content)
        is_temp_input = True
    elif os.path.exists(input_path):
        # It's a file path
        input_file_path = input_path
    else:
        # Assume it's a string with Mermaid content
        temp_dir = get_temp_dir()
        input_file_path = os.path.join(temp_dir, "string_input.mmd")
        with open(input_file_path, "w") as f:
            f.write(input_path)
        is_temp_input = True
    
    try:
        # Run mmdc for validation
        result, error = run_mmdc(
            input_file=input_file_path,
            validate=True,
            config_file=config_file
        )
        
        if result:
            return True, ""
        else:
            return False, error
            
    finally:
        # Clean up temp file if we created it
        if is_temp_input and os.path.exists(input_file_path):
            try:
                os.unlink(input_file_path)
            except Exception as e:
                logger.warning(f"Failed to remove temporary file: {e}") 