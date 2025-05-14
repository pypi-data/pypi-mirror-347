#!/usr/bin/env python
"""
005_template_toml_reference_debug.py - Debugging template processing

This example explores how the template bg_color is processed to identify issues.
"""

from pathlib import Path
import tomli

from easypptx import Presentation
from easypptx.template import TemplateManager

# Set up paths
CURRENT_DIR = Path(__file__).parent
ROOT_DIR = CURRENT_DIR.parent.parent
TEMPLATE_DIR = ROOT_DIR / "templates"
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    """Run the example."""
    print("Debugging template loading...")

    # Path to the TOML template file
    template_file = TEMPLATE_DIR / "custom_reference_template_fixed.toml"
    
    # First, let's read the TOML file directly to see what format bg_color is in
    with open(template_file, "rb") as f:
        template_data = tomli.load(f)
    
    print(f"Direct from TOML - Background color: {template_data.get('bg_color')}")
    print(f"Background color type: {type(template_data.get('bg_color'))}")
    
    # Initialize the template manager and load the template
    template_manager = TemplateManager(template_dir=str(TEMPLATE_DIR))
    template_name = template_manager.load(str(template_file))
    
    # Get the template data
    template_data = template_manager.get(template_name)
    print(f"From TemplateManager - Background color: {template_data.get('bg_color')}")
    print(f"Background color type: {type(template_data.get('bg_color'))}")
    
    # Try creating a presentation with a hardcoded bg_color
    presentation = Presentation()
    slide = presentation.add_slide()
    
    # Test applying a bg_color in tuple format directly
    bg_color = (255, 255, 255)  # White as tuple
    print(f"Testing with hardcoded tuple: {bg_color}, type: {type(bg_color)}")
    try:
        slide.set_background_color(bg_color)
        print("Success with tuple format!")
    except Exception as e:
        print(f"Error with tuple format: {e}")
    
    # Save the presentation
    output_path = OUTPUT_DIR / "debug_bg_color.pptx"
    presentation.save(output_path)
    print(f"Saved debug presentation to: {output_path}")


if __name__ == "__main__":
    main()