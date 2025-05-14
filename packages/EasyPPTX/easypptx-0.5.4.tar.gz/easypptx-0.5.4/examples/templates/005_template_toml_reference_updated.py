#!/usr/bin/env python
"""
005_template_toml_reference_updated.py - Fixed TOML Templates with Reference PPTX

This example demonstrates:
1. Loading a template from a TOML file that specifies a reference PPTX
2. Creating slides based on this template
3. The reference PPTX specified in the TOML provides layouts and styling
"""

from pathlib import Path

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

    # Initialize the template manager
    template_manager = TemplateManager(template_dir=str(TEMPLATE_DIR))

    # Load our custom template that specifies a reference PPTX
    template_file = TEMPLATE_DIR / "custom_reference_template.toml"
    template_name = template_manager.load(str(template_file))
    print(f"Loaded template: {template_name}")

    # Get the reference PPTX file path from the template
    reference_pptx = template_manager.get_reference_pptx(template_name)
    blank_layout_index = template_manager.get_blank_layout_index(template_name)

    print(f"Template specifies reference PPTX: {reference_pptx}")
    print(f"Template specifies blank layout index: {blank_layout_index}")

    # Create a new presentation
    presentation = Presentation()
    
    # Register the template with the presentation's template manager
    # This is the key step that was missing in the original example
    template_data = template_manager.get(template_name)
    presentation.template_manager.register(template_name, template_data)
    
    # Register the reference PPTX with the presentation's template manager
    if reference_pptx:
        presentation.template_manager.template_references[template_name] = reference_pptx

    # Add a slide using the template
    # This will automatically use the reference PPTX specified in the template
    slide = presentation.add_slide_from_template(template_name)

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

    # Add another slide to demonstrate that the reference PPTX is still being used
    slide2 = presentation.add_slide_from_template(template_name)
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
    output_path = OUTPUT_DIR / "005_template_toml_reference_updated.pptx"
    presentation.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()