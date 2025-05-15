"""
Utility functions for the Mermaid MCP server and CLI
"""

import os
import sys
import subprocess
import tempfile
import logging
import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any, Union

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mermaid-mcp.utils")

# Enable more verbose debugging
DEBUG_THEMES = True


def css_to_theme_variables(css_content: str) -> Dict[str, Any]:
    """Convert CSS variables to Mermaid theme variables
    
    Args:
        css_content: The content of a CSS file with variables
        
    Returns:
        Dict[str, Any]: Theme variables for Mermaid config
    """
    theme_variables = {}
    # CSS variable mapping to Mermaid theme variables
    variable_mapping = {
        # General theme variables
        "--mermaid-primary-color": "primaryColor",
        "--mermaid-primary-border-color": "primaryBorderColor",
        "--mermaid-primary-text-color": "primaryTextColor",
        "--mermaid-secondary-color": "secondaryColor",
        "--mermaid-secondary-border-color": "secondaryBorderColor",
        "--mermaid-secondary-text-color": "secondaryTextColor",
        "--mermaid-tertiary-color": "tertiaryColor",
        "--mermaid-tertiary-border-color": "tertiaryBorderColor",
        "--mermaid-tertiary-text-color": "tertiaryTextColor",
        "--mermaid-font-family": "fontFamily",
        "--mermaid-font-size": "fontSize",
        "--mermaid-line-color": "lineColor",
        "--mermaid-background-color": "background",
        
        # Note styling
        "--mermaid-note-bkg-color": "noteBkgColor",
        "--mermaid-note-border-color": "noteBorderColor",
        "--mermaid-note-text-color": "noteTextColor",
        
        # Activation styling
        "--mermaid-active-bkg-color": "activationBkgColor",
        "--mermaid-active-text-color": "activationTextColor",
        
        # Sequence diagram
        "--mermaid-sequence-actor-background": "actorBkg",
        "--mermaid-sequence-actor-border": "actorBorder",
        "--mermaid-sequence-actor-text": "actorTextColor",
        "--mermaid-sequence-note-background": "noteBkgColor",
        "--mermaid-sequence-note-border": "noteBorderColor",
        "--mermaid-sequence-activation-background": "activationBkgColor",
        "--mermaid-sequence-activation-border": "activationBorderColor",
        
        # Class diagram
        "--mermaid-class-border": "classBorder",
        "--mermaid-class-background": "classBkg",
        "--mermaid-class-text": "classText",
        
        # Generic node styling (critical for flowcharts)
        "--mermaid-node-border": "nodeBorder",
        "--mermaid-node-background": "nodeBkg",
        "--mermaid-node-text": "nodeTextColor",
        
        # Flowchart specific
        "--mermaid-flowchart-node-border": "nodeBorder",
        "--mermaid-flowchart-node-background": "nodeBkg",
        "--mermaid-flowchart-node-text": "nodeTextColor",
        
        # Edge styling
        "--mermaid-edge-color": "edgeColor",
        "--mermaid-edge-label-background": "labelBackgroundColor",
        "--mermaid-edge-label-text": "labelTextColor",
        
        # Arrowheads
        "--mermaid-arrow-head-color": "arrowheadColor",
        
        # Cluster/subgraph styling
        "--mermaid-cluster-background": "clusterBkg",
        "--mermaid-cluster-border": "clusterBorder",
        
        # State diagram
        "--mermaid-state-border": "stateBorder",
        "--mermaid-state-background": "stateBkg",
        "--mermaid-state-text": "stateTextColor",
        "--mermaid-state-transition-color": "transitionColor",
        
        # Entity relationship
        "--mermaid-er-entity-color": "entityBkg",
        "--mermaid-er-entity-border": "entityBorder",
        "--mermaid-er-entity-text": "entityTextColor",
        "--mermaid-er-relationship-color": "relationshipBkg",
        
        # Additional mappings for compatibility
        "--mermaid-primary-color": "mainBkg",  # Map primary color to mainBkg as well
        "--mermaid-primary-border-color": "borderColor",
        "--mermaid-primary-text-color": "textColor",
    }
    
    # Extract variables using regex
    css_var_pattern = r'--mermaid-[\w-]+:\s*([^;]+);'
    matches = re.findall(r'(--mermaid-[\w-]+):\s*([^;]+);', css_content)
    
    if DEBUG_THEMES:
        logger.info(f"Found {len(matches)} CSS variables")
    
    # Track which variables were processed
    processed_vars = set()
    
    for var_name, var_value in matches:
        for css_var, mermaid_var in variable_mapping.items():
            if var_name == css_var:
                theme_variables[mermaid_var] = var_value.strip()
                processed_vars.add(var_name)
                if DEBUG_THEMES:
                    logger.info(f"Mapping CSS {var_name} -> Mermaid {mermaid_var} = {var_value.strip()}")
                
    if DEBUG_THEMES:
        for var_name, _ in matches:
            if var_name not in processed_vars:
                logger.warning(f"No mapping found for CSS variable: {var_name}")
        
        if not theme_variables:
            logger.warning("No CSS variables were mapped to Mermaid theme variables")
    
    return theme_variables


def list_json_themes() -> Dict[str, str]:
    """List all available JSON theme configurations in the themes directory
    
    Returns:
        Dict[str, str]: A dictionary mapping theme names to file paths
    """
    themes = {}
    themes_dir = Path(__file__).parent / "themes"
    
    if themes_dir.exists() and themes_dir.is_dir():
        for file in themes_dir.glob("*.json"):
            theme_name = file.stem
            themes[theme_name] = str(file)
    
    return themes


def get_json_theme_path(theme_name: str) -> Optional[str]:
    """Get the path to a JSON theme configuration file
    
    Args:
        theme_name: The name of the theme (without .json extension)
        
    Returns:
        Optional[str]: The path to the theme file or None if not found
    """
    if not theme_name:
        return None
        
    themes_dir = Path(__file__).parent / "themes"
    theme_path = themes_dir / f"{theme_name}.json"
    
    if theme_path.exists() and theme_path.is_file():
        return str(theme_path)
    
    return None


def load_json_theme(theme_name: str) -> Optional[Dict[str, Any]]:
    """Load a JSON theme configuration
    
    Args:
        theme_name: The name of the theme (without .json extension)
        
    Returns:
        Optional[Dict[str, Any]]: The theme configuration or None if not found
    """
    theme_path = get_json_theme_path(theme_name)
    
    if theme_path:
        try:
            with open(theme_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON theme file: {e}")
    
    return None


def run_mmdc(
    input_file: str,
    output_path: Optional[str] = None,
    config_file: Optional[str] = None,
    css_file: Optional[str] = None,
    background_color: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    theme: Optional[str] = None,
    css_theme_name: Optional[str] = None,
    json_theme_name: Optional[str] = None,
    validate: bool = False
) -> Tuple[bool, str]:
    """Run the mmdc command-line tool to generate or validate a chart"""
    # Build the command
    cmd = ["mmdc", "-i", input_file]
    
    if not validate and output_path:
        cmd.extend(["-o", output_path])
    
    # Handle theme configuration
    final_config_file = config_file
    temp_config_file = None
    
    if DEBUG_THEMES:
        logger.info(f"Theme parameters: css_theme={css_theme_name}, json_theme={json_theme_name}, theme={theme}")
    
    # Priority: json_theme > css_theme > config_file
    if json_theme_name:
        json_theme = load_json_theme(json_theme_name)
        if json_theme:
            # Write the theme to a temporary file
            temp_config_file = tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False)
            json.dump(json_theme, temp_config_file)
            temp_config_file.close()
            
            final_config_file = temp_config_file.name
            if DEBUG_THEMES:
                logger.info(f"Created config with JSON theme: {final_config_file}")
                logger.info(f"JSON theme content: {json.dumps(json_theme, indent=2)}")
    elif css_theme_name:
        css_content = read_css_theme(css_theme_name)
        if css_content:
            # Create a temporary configuration file that includes the theme variables
            config_data = {}
            
            # If a config file was specified, read it first
            if config_file:
                try:
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                        if DEBUG_THEMES:
                            logger.info(f"Loaded existing config: {json.dumps(config_data, indent=2)}")
                except Exception as e:
                    logger.error(f"Error reading config file: {e}")
            
            # Convert CSS variables to Mermaid theme variables
            theme_variables = css_to_theme_variables(css_content)
            
            # Set theme to base to allow theme variables to work
            config_data["theme"] = "base"
            
            # Add theme variables to config
            if "themeVariables" not in config_data:
                config_data["themeVariables"] = {}
                
            config_data["themeVariables"].update(theme_variables)
            
            # Explicitly set additional variables to ensure theme works
            if theme_variables.get("nodeBkg") and "primaryColor" in theme_variables:
                # Ensure the mainBkg is set for flowcharts
                config_data["themeVariables"]["mainBkg"] = theme_variables.get("primaryColor")
                
                # Set text color if we have primaryTextColor
                if "primaryTextColor" in theme_variables:
                    config_data["themeVariables"]["textColor"] = theme_variables.get("primaryTextColor")
                
                # Set edge/line color
                if "lineColor" in theme_variables:
                    config_data["themeVariables"]["edgeColor"] = theme_variables.get("lineColor")
                
                if DEBUG_THEMES:
                    logger.info("Added additional theme mappings for flowchart compatibility")
            
            # Explicitly set darkMode if we detect it's a dark theme
            if "primaryColor" in theme_variables:
                primary_color = theme_variables["primaryColor"].lower()
                # Check if primary color is dark
                if primary_color.startswith("#"):
                    # Convert hex to RGB and check brightness
                    if len(primary_color) == 4:  # #RGB
                        r = int(primary_color[1], 16) * 16
                        g = int(primary_color[2], 16) * 16
                        b = int(primary_color[3], 16) * 16
                    else:  # #RRGGBB
                        r = int(primary_color[1:3], 16)
                        g = int(primary_color[3:5], 16)
                        b = int(primary_color[5:7], 16)
                    
                    brightness = (r * 299 + g * 587 + b * 114) / 1000
                    if brightness < 128:
                        config_data["themeVariables"]["darkMode"] = True
                        if DEBUG_THEMES:
                            logger.info(f"Setting darkMode=true based on dark primaryColor {primary_color} (brightness: {brightness})")
            
            # Write the updated configuration to a temporary file
            temp_config_file = tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False)
            json.dump(config_data, temp_config_file)
            temp_config_file.close()
            
            final_config_file = temp_config_file.name
            if DEBUG_THEMES:
                logger.info(f"Created custom config with theme variables: {final_config_file}")
                logger.info(f"Final config: {json.dumps(config_data, indent=2)}")
    
    if final_config_file:
        cmd.extend(["-c", final_config_file])
    
    if css_file:
        cmd.extend(["-C", css_file])
    
    if background_color:
        cmd.extend(["-b", background_color])
    
    if width:
        cmd.extend(["-w", str(width)])
    
    if height:
        cmd.extend(["-H", str(height)])
    
    if theme:
        cmd.extend(["-t", theme])
    
    # Run command and capture output
    try:
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return True, ""
        else:
            error_output = result.stderr.strip() or result.stdout.strip()
            logger.error(f"Command failed: {error_output}")
            return False, error_output
    except Exception as e:
        logger.exception("Error running mmdc command")
        return False, str(e)
    finally:
        # Clean up temporary files
        if temp_config_file and os.path.exists(temp_config_file.name):
            try:
                os.unlink(temp_config_file.name)
            except Exception as e:
                logger.error(f"Error removing temporary config file: {e}")


def find_chart_info(chart_type: str) -> Dict[str, Any]:
    """Get information about a specific chart type"""
    from mermaid_mcp.chart_info import CHART_TYPES
    
    # Handle aliases
    if chart_type == "flow" or chart_type == "graph":
        chart_type = "flowchart"
    elif chart_type == "seq":
        chart_type = "sequence"
    
    return CHART_TYPES.get(chart_type, {})


def is_valid_chart_type(chart_type: str) -> bool:
    """Check if a chart type is valid"""
    from mermaid_mcp.chart_info import CHART_TYPES
    
    # Handle aliases
    if chart_type in ["flow", "graph"]:
        chart_type = "flowchart"
    elif chart_type == "seq":
        chart_type = "sequence"
    
    return chart_type in CHART_TYPES


def get_download_dir() -> str:
    """Get the download directory from environment or use default"""
    download_dir = os.environ.get("DOWNLOAD_DIR")
    
    if not download_dir:
        # Use user's Downloads directory
        download_dir = str(Path.home() / "Downloads")
        
    # Ensure the directory exists
    os.makedirs(download_dir, exist_ok=True)
    
    return download_dir


def get_temp_dir() -> str:
    """Get a temporary directory for storing files"""
    temp_dir = os.path.join(tempfile.gettempdir(), "mermaid-mcp")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def parse_config_file(config_path: str) -> Dict[str, Any]:
    """Parse a configuration file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse config file: {e}")
        return {}


def list_css_themes() -> Dict[str, str]:
    """List all available CSS themes in the css directory
    
    Returns:
        Dict[str, str]: A dictionary mapping theme names to file paths
    """
    themes = {}
    css_dir = Path(__file__).parent / "css"
    
    if DEBUG_THEMES:
        logger.info(f"Looking for CSS themes in: {css_dir}")
    
    if css_dir.exists() and css_dir.is_dir():
        for file in css_dir.glob("*.css"):
            theme_name = file.stem
            themes[theme_name] = str(file)
            if DEBUG_THEMES:
                logger.info(f"Found CSS theme: {theme_name} at {file}")
    else:
        logger.warning(f"CSS theme directory does not exist: {css_dir}")
    
    return themes


def get_css_theme_path(theme_name: str) -> Optional[str]:
    """Get the path to a CSS theme file
    
    Args:
        theme_name: The name of the theme (without .css extension)
        
    Returns:
        Optional[str]: The path to the theme file or None if not found
    """
    if not theme_name:
        return None
        
    css_dir = Path(__file__).parent / "css"
    theme_path = css_dir / f"{theme_name}.css"
    
    if theme_path.exists() and theme_path.is_file():
        return str(theme_path)
    
    return None


def read_css_theme(theme_name: str) -> Optional[str]:
    """Read the content of a CSS theme file
    
    Args:
        theme_name: The name of the theme (without .css extension)
        
    Returns:
        Optional[str]: The content of the theme file or None if not found
    """
    theme_path = get_css_theme_path(theme_name)
    
    if theme_path:
        try:
            with open(theme_path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read CSS theme file: {e}")
    
    return None


def get_launch_agent_plist_path() -> Path:
    """Get the path to the user's LaunchAgents directory."""
    home_dir = Path.home()
    return home_dir / "Library" / "LaunchAgents" / "com.mermaid-mcp.server.plist"


def create_launch_agent(port: int = 27312, log_dir: Optional[str] = None) -> Tuple[bool, str]:
    """
    Create a macOS launch agent plist file for auto-starting the server.
    
    Args:
        port: Port to run the server on
        log_dir: Directory for logs (if None, default temp directory will be used)
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        # Set up log directory
        if not log_dir:
            log_dir = get_temp_dir()
        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Get the path to the executable
        executable_path = sys.executable
        
        # Get the module path
        module_path = os.path.dirname(os.path.abspath(__file__))
        
        # Create the plist content
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mermaid-mcp.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>{executable_path}</string>
        <string>-m</string>
        <string>mermaid_mcp.entry</string>
        <string>server</string>
        <string>start</string>
        <string>--port</string>
        <string>{port}</string>
        <string>--log_dir</string>
        <string>{log_dir}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{log_dir}/mermaid-mcp.log</string>
    <key>StandardErrorPath</key>
    <string>{log_dir}/mermaid-mcp.error.log</string>
    <key>WorkingDirectory</key>
    <string>{module_path}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
'''
        
        # Write the plist file
        plist_path = get_launch_agent_plist_path()
        with open(plist_path, 'w') as f:
            f.write(plist_content)
            
        return True, f"Launch agent created at {plist_path}"
    except Exception as e:
        return False, f"Failed to create launch agent: {str(e)}"


def install_launch_agent(port: int = 27312, log_dir: Optional[str] = None) -> Tuple[bool, str]:
    """
    Install and load the macOS launch agent.
    
    Args:
        port: Port to run the server on
        log_dir: Directory for logs
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    # First create the launch agent plist
    success, message = create_launch_agent(port, log_dir)
    if not success:
        return False, message
        
    # Load the launch agent
    try:
        plist_path = get_launch_agent_plist_path()
        subprocess.run(['launchctl', 'unload', str(plist_path)], capture_output=True, check=False)
        result = subprocess.run(['launchctl', 'load', str(plist_path)], capture_output=True, text=True, check=True)
        
        return True, f"Launch agent installed and loaded successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to load launch agent: {e.stderr}"
    except Exception as e:
        return False, f"Failed to install launch agent: {str(e)}"


def uninstall_launch_agent() -> Tuple[bool, str]:
    """
    Uninstall (unload and remove) the macOS launch agent.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        plist_path = get_launch_agent_plist_path()
        
        # Check if the plist file exists
        if not plist_path.exists():
            return True, "Launch agent is not installed"
            
        # Unload the launch agent
        subprocess.run(['launchctl', 'unload', str(plist_path)], capture_output=True, check=False)
        
        # Remove the plist file
        plist_path.unlink()
        
        return True, "Launch agent uninstalled successfully"
    except Exception as e:
        return False, f"Failed to uninstall launch agent: {str(e)}"


def check_launch_agent_status() -> Tuple[bool, bool, str]:
    """
    Check if the launch agent is installed and running.
    
    Returns:
        Tuple[bool, bool, str]: (is_installed, is_running, message)
    """
    try:
        plist_path = get_launch_agent_plist_path()
        
        # Check if plist file exists
        is_installed = plist_path.exists()
        if not is_installed:
            return False, False, "Launch agent is not installed"
        
        # Check if it's loaded/running
        result = subprocess.run(['launchctl', 'list'], capture_output=True, text=True)
        is_running = "com.mermaid-mcp.server" in result.stdout
        
        status_msg = "running" if is_running else "installed but not running"
        return True, is_running, f"Launch agent is {status_msg}"
        
    except Exception as e:
        return False, False, f"Error checking launch agent status: {str(e)}"


def stop_launch_agent() -> Tuple[bool, str]:
    """
    Stop the launch agent without uninstalling it.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        installed, running, _ = check_launch_agent_status()
        
        if not installed:
            return False, "Launch agent is not installed"
            
        if not running:
            return True, "Launch agent is already stopped"
            
        # Stop the launch agent
        result = subprocess.run(['launchctl', 'unload', str(get_launch_agent_plist_path())], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, "Launch agent stopped successfully"
        else:
            return False, f"Failed to stop launch agent: {result.stderr}"
    except Exception as e:
        return False, f"Error stopping launch agent: {str(e)}"


def restart_launch_agent(port: int = 27312, log_dir: Optional[str] = None) -> Tuple[bool, str]:
    """
    Restart the launch agent.
    
    Args:
        port: Port to run the server on (for reinstallation)
        log_dir: Directory for logs (for reinstallation)
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        installed, _, _ = check_launch_agent_status()
        
        if not installed:
            # If not installed, just install it
            return install_launch_agent(port, log_dir)
            
        # Otherwise, unload and reload it
        stop_success, stop_message = stop_launch_agent()
        if not stop_success:
            return False, f"Failed to stop launch agent during restart: {stop_message}"
            
        # Reload the launch agent
        result = subprocess.run(['launchctl', 'load', str(get_launch_agent_plist_path())], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, "Launch agent restarted successfully"
        else:
            return False, f"Failed to restart launch agent: {result.stderr}"
    except Exception as e:
        return False, f"Error restarting launch agent: {str(e)}" 