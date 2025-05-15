"""
Test file for Mermaid MCP
Includes tests for diagram generation and theme application
"""

import os
import sys
import pytest
import logging
import requests
import subprocess
from pathlib import Path

# Add the parent directory to the sys.path so we can import the package
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mermaid-test")

# Sample diagrams for testing
FLOWCHART = """
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
"""

SEQUENCE = """
sequenceDiagram
    participant User
    participant System
    participant DB
    
    User->>System: Request data
    System->>DB: Query data
    DB-->>System: Return results
    System-->>User: Display results
"""

class TestMermaidDiagrams:
    """Tests for diagram generation"""
    
    def test_flowchart_generation(self, output_dir, mmdc_available):
        """Test basic flowchart generation"""
        if not mmdc_available:
            pytest.skip("mmdc not available")
            
        diagram_file = output_dir / "flowchart_test.mmd"
        output_file = output_dir / "flowchart_test.svg"
        
        with open(diagram_file, "w") as f:
            f.write(FLOWCHART)
        
        # Use subprocess to call mmdc directly for testing
        result = subprocess.run(
            ["mmdc", "-i", str(diagram_file), "-o", str(output_file)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert output_file.exists()
    
    def test_sequence_generation(self, output_dir, mmdc_available):
        """Test basic sequence diagram generation"""
        if not mmdc_available:
            pytest.skip("mmdc not available")
            
        diagram_file = output_dir / "sequence_test.mmd"
        output_file = output_dir / "sequence_test.svg"
        
        with open(diagram_file, "w") as f:
            f.write(SEQUENCE)
        
        # Use subprocess to call mmdc directly for testing
        result = subprocess.run(
            ["mmdc", "-i", str(diagram_file), "-o", str(output_file)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert output_file.exists()

class TestThemes:
    """Tests for theme application"""
    
    def get_available_themes(self, server_url):
        """Get all available themes from the server"""
        try:
            response = requests.get(f"{server_url}/themes")
            if response.status_code == 200:
                result = response.json()
                return {
                    "css_themes": result.get("available_css_themes", []),
                    "json_themes": result.get("available_json_themes", []),
                    "built_in_themes": result.get("built_in_themes", [])
                }
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                return {"css_themes": [], "json_themes": [], "built_in_themes": []}
        except Exception as e:
            logger.error(f"Error getting themes: {e}")
            return {"css_themes": [], "json_themes": [], "built_in_themes": []}
    
    def test_builtin_themes(self, output_dir, server_url, check_server, mmdc_available):
        """Test built-in themes (requires server running)"""
        if not check_server or not mmdc_available:
            pytest.skip("Server not running or mmdc not available")
            
        diagram_file = output_dir / "theme_test.mmd"
        
        with open(diagram_file, "w") as f:
            f.write(FLOWCHART)
        
        # Get built-in themes
        themes = self.get_available_themes(server_url)
        built_in_themes = themes.get("built_in_themes", ["default"])
        
        for theme in built_in_themes[:1]:  # Test only one theme for brevity
            output_file = output_dir / f"flowchart_builtin_{theme}.svg"
            
            # Use subprocess to call mmdc directly
            result = subprocess.run(
                ["mmdc", "-i", str(diagram_file), "-o", str(output_file), "-t", theme],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert output_file.exists()
    
    def test_css_themes(self, output_dir, server_url, check_server, mmdc_available):
        """Test CSS themes (requires server running)"""
        if not check_server or not mmdc_available:
            pytest.skip("Server not running or mmdc not available")
            
        diagram_file = output_dir / "css_theme_test.mmd"
        
        with open(diagram_file, "w") as f:
            f.write(FLOWCHART)
        
        # Get CSS themes
        themes = self.get_available_themes(server_url)
        css_themes = themes.get("css_themes", [])
        
        if not css_themes:
            logger.warning("No CSS themes available to test")
            pytest.skip("No CSS themes available")
            return
        
        # Test only one theme for brevity
        if css_themes:
            theme = css_themes[0]
            output_file = output_dir / f"flowchart_css_{theme}.svg"
            
            # Test directly via API
            url = f"{server_url}/generate/flowchart"
            payload = {
                "input": FLOWCHART,
                "output": f"flowchart_css_{theme}.svg",
                "css_theme": theme
            }
            
            response = requests.post(url, json=payload)
            
            assert response.status_code == 200
            
            # Save the response
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            assert output_file.exists()
    
    def test_json_themes(self, output_dir, server_url, check_server, mmdc_available):
        """Test JSON themes (requires server running)"""
        if not check_server or not mmdc_available:
            pytest.skip("Server not running or mmdc not available")
            
        diagram_file = output_dir / "json_theme_test.mmd"
        
        with open(diagram_file, "w") as f:
            f.write(FLOWCHART)
        
        # Get JSON themes
        themes = self.get_available_themes(server_url)
        json_themes = themes.get("json_themes", [])
        
        if not json_themes:
            logger.warning("No JSON themes available to test")
            pytest.skip("No JSON themes available")
            return
        
        # Test only one theme for brevity
        if json_themes:
            theme = json_themes[0]
            output_file = output_dir / f"flowchart_json_{theme}.svg"
            
            # Test directly via API
            url = f"{server_url}/generate/flowchart"
            payload = {
                "input": FLOWCHART,
                "output": f"flowchart_json_{theme}.svg",
                "json_theme": theme
            }
            
            response = requests.post(url, json=payload)
            
            assert response.status_code == 200
            
            # Save the response
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            assert output_file.exists()

if __name__ == "__main__":
    # Run tests directly if this file is executed
    from conftest import OUTPUT_DIR
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Check server availability
    server_available = False
    try:
        response = requests.get("http://localhost:27312/")
        server_available = response.status_code == 200
    except:
        print("Warning: Server not running, skipping theme tests")
    
    # Check mmdc availability
    mmdc_available = False
    try:
        result = subprocess.run(
            ["mmdc", "--version"],
            capture_output=True,
            text=True
        )
        mmdc_available = result.returncode == 0
    except:
        print("Warning: mmdc not available, skipping CLI tests")
    
    if mmdc_available:
        test_diagrams = TestMermaidDiagrams()
        test_diagrams.test_flowchart_generation(OUTPUT_DIR, True)
        test_diagrams.test_sequence_generation(OUTPUT_DIR, True)
        print("✅ Diagram generation tests passed")
    
    if server_available and mmdc_available:
        test_themes = TestThemes()
        test_themes.test_builtin_themes(OUTPUT_DIR, "http://localhost:27312", True, True)
        test_themes.test_css_themes(OUTPUT_DIR, "http://localhost:27312", True, True)
        test_themes.test_json_themes(OUTPUT_DIR, "http://localhost:27312", True, True)
        print("✅ Theme tests passed")
    
    print("All tests completed!") 