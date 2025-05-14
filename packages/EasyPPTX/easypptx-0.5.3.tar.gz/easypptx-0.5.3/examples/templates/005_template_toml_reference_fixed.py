#!/usr/bin/env python
"""
005_template_toml_reference_fixed.py - TOML Templates with Reference PPTX

This example demonstrates:
1. Loading a template from a TOML file directly in the Presentation constructor
2. Creating slides based on this template
3. The reference PPTX specified in the TOML provides layouts and styling
"""

from pathlib import Path

from easypptx import Presentation

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
    
    # Create a new presentation directly using the template_toml parameter
    # This automatically loads the template and makes it the default template
    presentation = Presentation(template_toml=str(template_file))
    
    print(f"Loaded template: custom_reference_template_fixed")
    
    # Add a slide - this should use the default template that was loaded in the constructor
    slide = presentation.add_slide()
    
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
    slide2 = presentation.add_slide()
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
    output_path = OUTPUT_DIR / "005_template_toml_reference_fixed.pptx"
    presentation.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()