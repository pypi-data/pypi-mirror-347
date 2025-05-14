#!/usr/bin/env python
"""
005_template_toml_reference_final.py - TOML Templates with Reference PPTX

This example demonstrates:
1. Loading a template from a TOML file
2. Creating slides based on this template
3. Handling the list-to-tuple conversion for colors
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
    print("Creating a presentation with a TOML template that specifies a reference PPTX...")

    # Path to the TOML template file
    template_file = TEMPLATE_DIR / "custom_reference_template_fixed.toml"
    
    # Read the template data from TOML
    with open(template_file, "rb") as f:
        template_data = tomli.load(f)
    
    # Convert bg_color from list to tuple if present
    if "bg_color" in template_data and isinstance(template_data["bg_color"], list):
        template_data["bg_color"] = tuple(template_data["bg_color"])
    
    # Create a new presentation
    presentation = Presentation()
    
    # Load and register the template with our modified data
    template_manager = TemplateManager()
    template_manager.register("custom_template", template_data)
    
    # Set reference PPTX if specified
    if "reference_pptx" in template_data:
        # Get absolute path to reference PPTX
        ref_path = template_data["reference_pptx"]
        if not Path(ref_path).is_absolute():
            ref_path = str(TEMPLATE_DIR / ref_path)
        
        # Register the reference PPTX with the template manager
        template_manager.template_references["custom_template"] = ref_path
    
    # Integrate the template manager with the presentation
    presentation.template_manager = template_manager
    
    # Now add a slide using our registered template
    slide = presentation.add_slide_from_template("custom_template")
    
    # Add some additional content to the slide
    slide.add_text(
        text="This slide uses a custom reference PPTX file specified in the TOML template",
        x="10%",
        y="70%",
        width="80%",
        height="10%",
        font_size=18,
        align="center",
    )

    # Add another slide
    slide2 = presentation.add_slide_from_template("custom_template")
    slide2.add_text(
        text="This is a second slide using the same reference PPTX",
        x="10%",
        y="40%",
        width="80%",
        height="20%",
        font_size=32,
        align="center",
    )

    # Save the presentation
    output_path = OUTPUT_DIR / "005_template_toml_reference_final.pptx"
    presentation.save(output_path)
    print(f"Saved presentation to: {output_path}")


if __name__ == "__main__":
    main()