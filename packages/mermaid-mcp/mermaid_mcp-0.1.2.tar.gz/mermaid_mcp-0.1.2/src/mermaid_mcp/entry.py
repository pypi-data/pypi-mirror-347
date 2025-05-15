#!/usr/bin/env python3
"""
Mermaid Model Context Protocol (MCP) server
Entry point for the server and CLI modes
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

from mermaid_mcp.server import start_server
from mermaid_mcp.cli import generate_chart, validate_chart
from mermaid_mcp.utils import (
    list_css_themes, 
    list_json_themes, 
    install_launch_agent, 
    uninstall_launch_agent,
    stop_launch_agent,
    restart_launch_agent,
    check_launch_agent_status
)


def main() -> int:
    """Main entry point for the Mermaid MCP server/CLI."""
    parser = argparse.ArgumentParser(description='Mermaid Model Context Protocol (MCP) server')
    subparsers = parser.add_subparsers(dest='mode', help='Mode to run in')
    
    # Server mode
    server_parser = subparsers.add_parser('server', help='Run in server mode')
    server_subparsers = server_parser.add_subparsers(dest='command', help='Server command')
    
    # Server start command
    start_parser = server_subparsers.add_parser('start', help='Start the server')
    start_parser.add_argument('--sse', action='store_true', help='Use SSE protocol')
    start_parser.add_argument('--stdio', action='store_true', help='Use stdio protocol')
    start_parser.add_argument('--port', type=int, default=27312, help='Port to run on')
    start_parser.add_argument('--log_dir', type=str, default=None, help='Directory for logs')
    
    # Server stop command
    stop_parser = server_subparsers.add_parser('stop', help='Stop the server')
    
    # Server restart command
    restart_parser = server_subparsers.add_parser('restart', help='Restart the server')
    restart_parser.add_argument('--port', type=int, default=27312, help='Port to run on')
    restart_parser.add_argument('--log_dir', type=str, default=None, help='Directory for logs')
    
    # Server install command
    install_parser = server_subparsers.add_parser('install', help='Install the launch agent')
    install_parser.add_argument('--port', type=int, default=27312, help='Port to run on')
    install_parser.add_argument('--log_dir', type=str, default=None, help='Directory for logs')
    
    # Server uninstall command
    uninstall_parser = server_subparsers.add_parser('uninstall', help='Uninstall the launch agent')
    
    # Server status command
    status_parser = server_subparsers.add_parser('status', help='Check the status of the launch agent')
    
    # Server help command
    help_parser = server_subparsers.add_parser('help', help='Show help')
    
    # CLI mode
    cli_parser = subparsers.add_parser('cli', help='Run in CLI mode')
    
    # Add theme and output options directly to cli_parser
    cli_parser.add_argument('--config', type=str, help='Path to JSON configuration file')
    cli_parser.add_argument('--cssFile', type=str, help='Path to CSS file for styling')
    cli_parser.add_argument('--cssStr', type=str, help='CSS styling as a string')
    cli_parser.add_argument('--theme', type=str, help='Built-in theme (default, forest, dark, neutral, base)')
    cli_parser.add_argument('--cssTheme', type=str, help='CSS theme name from included themes')
    cli_parser.add_argument('--jsonTheme', type=str, help='JSON theme name from included themes')
    cli_parser.add_argument('--bgColor', type=str, help='Background color (e.g., transparent, red, #F0F0F0)')
    cli_parser.add_argument('--width', type=int, help='Width of the output image')
    cli_parser.add_argument('--height', type=int, help='Height of the output image')
    cli_parser.add_argument('--format', type=str, choices=['svg', 'png', 'pdf'], help='Output format, overrides extension in output file')
    
    # CLI subcommands
    cli_subparsers = cli_parser.add_subparsers(dest='command', help='CLI command')
    
    # CLI chart command
    chart_parser = cli_subparsers.add_parser('chart', help='Generate a chart')
    chart_parser.add_argument('chart_type', type=str, help='Chart type (e.g., flowchart, sequence, class)')
    chart_parser.add_argument('input', type=str, help='Input file path (.mmd, .md) or raw mermaid string. Use - for stdin.')
    chart_parser.add_argument('output', type=str, nargs='?', help='Output file path. If not specified, will use input filename with .svg extension or "output.svg" for string input.')
    # Duplicate arguments for command-specific usage
    chart_parser.add_argument('--theme', type=str, help='Built-in theme (default, forest, dark, neutral, base)')
    chart_parser.add_argument('--cssTheme', type=str, help='CSS theme name from included themes')
    chart_parser.add_argument('--jsonTheme', type=str, help='JSON theme name from included themes')
    chart_parser.add_argument('--config', type=str, help='Path to JSON configuration file')
    chart_parser.add_argument('--cssFile', type=str, help='Path to CSS file for styling')
    chart_parser.add_argument('--cssStr', type=str, help='CSS styling as a string')
    chart_parser.add_argument('--bgColor', type=str, help='Background color (e.g., transparent, red, #F0F0F0)')
    chart_parser.add_argument('--width', type=int, help='Width of the output image')
    chart_parser.add_argument('--height', type=int, help='Height of the output image')
    chart_parser.add_argument('--format', type=str, choices=['svg', 'png', 'pdf'], help='Output format, overrides extension in output file')
    
    # CLI validate command
    validate_parser = cli_subparsers.add_parser('validate', help='Validate a chart')
    validate_parser.add_argument('chart_type', type=str, help='Chart type (e.g., flowchart, sequence, class)')
    validate_parser.add_argument('input', type=str, help='Input file path (.mmd, .md) or raw mermaid string. Use - for stdin.')
    validate_parser.add_argument('--config', type=str, help='Path to JSON configuration file')
    
    # CLI themes command
    themes_parser = cli_subparsers.add_parser('themes', help='List available themes')
    themes_parser.add_argument('--detailed', action='store_true', help='Show detailed theme information')
    
    # CLI help command
    help_parser = cli_subparsers.add_parser('help', help='Show detailed help with examples')
    help_parser.add_argument('chart_type', type=str, nargs='?', help='Show help for specific chart type')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        return 1
        
    if args.mode == 'server':
        return handle_server_mode(args)
    elif args.mode == 'cli':
        return handle_cli_mode(args)
    
    return 0


def handle_server_mode(args) -> int:
    """Handle server mode commands."""
    if not args.command:
        print("Error: No command specified for server mode")
        return 1
        
    if args.command == 'start':
        protocol = 'sse' if args.sse else 'stdio' if args.stdio else 'http'
        port = args.port
        log_dir = args.log_dir
        return start_server(protocol, port, log_dir)
    elif args.command == 'stop':
        print("Stopping server...")
        success, message = stop_launch_agent()
        print(message)
        return 0 if success else 1
    elif args.command == 'restart':
        print("Restarting server...")
        success, message = restart_launch_agent(args.port, args.log_dir)
        print(message)
        return 0 if success else 1
    elif args.command == 'install':
        print(f"Installing launch agent with port={args.port}, log_dir={args.log_dir}...")
        success, message = install_launch_agent(args.port, args.log_dir)
        print(message)
        return 0 if success else 1
    elif args.command == 'uninstall':
        print("Uninstalling launch agent...")
        success, message = uninstall_launch_agent()
        print(message)
        return 0 if success else 1
    elif args.command == 'status':
        installed, running, message = check_launch_agent_status()
        print(message)
        return 0
    elif args.command == 'help':
        print("Server mode help:")
        print("  start    - Start the server")
        print("  stop     - Stop the server")
        print("  restart  - Restart the server")
        print("  install  - Install the launch agent")
        print("  uninstall - Uninstall the launch agent")
        print("  status   - Check the status of the launch agent")
        return 0
    
    print(f"Unknown command: {args.command}")
    return 1


def list_all_themes() -> Dict[str, List[str]]:
    """Get a list of all available themes."""
    # Get CSS themes
    css_themes = list_css_themes()
    
    # Get JSON themes
    json_themes = list_json_themes()
    
    # Built-in themes
    built_in_themes = ["default", "forest", "dark", "neutral", "base"]
    
    return {
        "css_themes": list(css_themes.keys()),
        "json_themes": list(json_themes.keys()),
        "built_in_themes": built_in_themes
    }


def handle_cli_mode(args) -> int:
    """Handle CLI mode commands."""
    if not args.command:
        print("Error: No command specified for CLI mode")
        return 1
        
    if args.command == 'chart':
        return handle_chart_command(args)
    elif args.command == 'validate':
        return handle_validate_command(args)
    elif args.command == 'themes':
        return handle_themes_command(args)
    elif args.command == 'help':
        return handle_help_command(args)
    
    return 1


def get_arg_value(args, arg_name, default=None):
    """Get argument value from args namespace."""
    # Check if the argument exists in args
    if hasattr(args, arg_name):
        value = getattr(args, arg_name)
        if value is not None:
            return value
    return default


def handle_chart_command(args) -> int:
    """Handle the chart generation command."""
    chart_type = args.chart_type
    input_path = args.input
    output_path = args.output
    
    # Handle stdin input
    if input_path == '-':
        # Read from stdin
        input_content = sys.stdin.read()
        input_path = input_content  # Pass the content directly
        
        # If output not specified, use default
        if not output_path:
            output_path = "output.svg"
    # Handle file input
    elif os.path.exists(input_path):
        # If output_path is not specified, derive from input
        if not output_path:
            output_format = get_arg_value(args, 'format', "svg")
            output_path = os.path.splitext(input_path)[0] + f".{output_format}"
    # Handle string input
    else:
        # If output_path is not specified, use default
        if not output_path:
            output_format = get_arg_value(args, 'format', "svg")
            output_path = f"output.{output_format}"
    
    # If format is specified, ensure it's used regardless of output extension
    format_value = get_arg_value(args, 'format')
    if format_value and output_path:
        base_name = os.path.splitext(output_path)[0]
        output_path = f"{base_name}.{format_value}"
            
    result = generate_chart(
        chart_type=chart_type, 
        input_path=input_path, 
        output_path=output_path, 
        config_file=get_arg_value(args, 'config'), 
        css_file=get_arg_value(args, 'cssFile'),
        css_str=get_arg_value(args, 'cssStr'),
        background_color=get_arg_value(args, 'bgColor'),
        css_theme_name=get_arg_value(args, 'cssTheme'),
        json_theme_name=get_arg_value(args, 'jsonTheme'),
        width=get_arg_value(args, 'width'),
        height=get_arg_value(args, 'height'),
        theme=get_arg_value(args, 'theme')
    )
    
    if result:
        print(f"Chart generated successfully: {output_path}")
        return 0
    else:
        print("Failed to generate chart")
        return 1


def handle_validate_command(args) -> int:
    """Handle the chart validation command."""
    chart_type = args.chart_type
    input_path = args.input
    
    # Handle stdin input
    if input_path == '-':
        # Read from stdin
        input_content = sys.stdin.read()
        input_path = input_content  # Pass the content directly
    
    is_valid, message = validate_chart(
        chart_type=chart_type, 
        input_path=input_path, 
        config_file=get_arg_value(args, 'config')
    )
    
    if is_valid:
        print("Chart is valid")
        return 0
    else:
        print(f"Chart is invalid: {message}")
        return 1


def handle_themes_command(args) -> int:
    """Handle the themes listing command."""
    themes = list_all_themes()
    
    print("\nAvailable Themes:")
    print("================")
    
    print("\nBuilt-in Themes:")
    for theme in themes['built_in_themes']:
        print(f"  - {theme}")
    
    if themes['css_themes']:
        print("\nCSS Themes:")
        for theme in themes['css_themes']:
            print(f"  - {theme}")
    else:
        print("\nNo CSS themes found.")
    
    if themes['json_themes']:
        print("\nJSON Themes:")
        for theme in themes['json_themes']:
            print(f"  - {theme}")
    else:
        print("\nNo JSON themes found.")
    
    print("\nUsage:")
    print("  To use a built-in theme:    --theme=<name>")
    print("  To use a CSS theme:         --cssTheme=<name>")
    print("  To use a JSON theme:        --jsonTheme=<name>")
    print("  To use a custom CSS file:   --cssFile=<path>")
    print("  To use custom CSS content:  --cssStr='<css-content>'")
    print("  To use a config file:       --config=<path>")
    
    return 0


def handle_help_command(args) -> int:
    """Handle the help command, showing detailed usage information."""
    from mermaid_mcp.utils import find_chart_info
    
    if hasattr(args, 'chart_type') and args.chart_type:
        # Show help for specific chart type
        chart_info = find_chart_info(args.chart_type)
        if not chart_info:
            print(f"Unknown chart type: {args.chart_type}")
            return 1
            
        # Add the chart_type key if it doesn't exist
        if 'chart_type' not in chart_info:
            chart_info['chart_type'] = args.chart_type
            
        print(f"\n{chart_info['chart_type']} - {chart_info['description']}")
        print("=" * (len(chart_info['chart_type']) + len(chart_info['description']) + 3))
        print(f"\nRequired Input: {chart_info['required_input']}")
        print("\nExample:")
        print(f"{chart_info['example']}")
        
        if 'config' in chart_info and chart_info['config']:
            print("\nConfiguration Options:")
            for key, value in chart_info['config'].items():
                print(f"  {key}: {value}")
                
        print("\nUsage Examples:")
        print(f"  mermaid-mcp cli chart {args.chart_type} input.mmd output.svg")
        print(f"  mermaid-mcp cli chart {args.chart_type} --theme dark input.mmd output.svg")
        print(f"  mermaid-mcp cli chart {args.chart_type} --cssTheme dracula-enhanced input.mmd output.svg")
    else:
        # Show general help
        print("\nMermaid MCP CLI")
        print("==============")
        print("\nCommands:")
        print("  chart <chart_type> <input> [output]  - Generate a chart")
        print("  validate <chart_type> <input>        - Validate a chart")
        print("  themes                               - List available themes")
        print("  help [chart_type]                    - Show detailed help")
        
        print("\nChart Types:")
        # List all chart types from chart_info module
        from mermaid_mcp.chart_info import CHART_TYPES
        for chart_type in CHART_TYPES:
            chart_info = find_chart_info(chart_type)
            if chart_info:
                print(f"  {chart_type:20} - {chart_info['description']}")
        
        print("\nExamples:")
        print("  mermaid-mcp cli chart flowchart diagram.mmd output.svg")
        print("  mermaid-mcp cli chart sequence 'sequenceDiagram\\n  A->B: Hello'")
        print("  mermaid-mcp cli validate flowchart diagram.mmd")
        print("  cat diagram.mmd | mermaid-mcp cli chart flowchart - output.png")
        print("  mermaid-mcp cli chart flowchart --theme dark diagram.mmd")
        print("  mermaid-mcp cli chart flowchart --cssTheme dracula-enhanced diagram.mmd")
        print("  mermaid-mcp cli chart flowchart --jsonTheme forest-night diagram.mmd")
        print("  mermaid-mcp cli chart flowchart --format png diagram.mmd output")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 