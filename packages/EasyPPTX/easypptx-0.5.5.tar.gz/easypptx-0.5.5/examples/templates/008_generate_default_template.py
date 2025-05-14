#!/usr/bin/env python
"""
008_generate_default_template.py - Generate and Use Default Template

This example demonstrates:
1. Generating a comprehensive default template
2. Saving it to a TOML file
3. Loading and using it with Presentation
"""

from pathlib import Path

from easypptx import Presentation, generate_default_template

# Set up paths
CURRENT_DIR = Path(__file__).parent
ROOT_DIR = CURRENT_DIR.parent.parent
OUTPUT_DIR = ROOT_DIR / "output"
TEMPLATE_DIR = OUTPUT_DIR / "templates"
OUTPUT_DIR.mkdir(exist_ok=True)
TEMPLATE_DIR.mkdir(exist_ok=True)


def main():
    """Run the example."""
    print("Generating and using a comprehensive default template...")

    # Path to save the generated template
    template_path = TEMPLATE_DIR / "comprehensive_defaults.toml"
    
    # Generate the template and save it to a file
    template_data = generate_default_template(template_path)
    print(f"Generated template with {len(template_data)} top-level keys")
    print(f"Template includes defaults for {len(template_data['defaults'])} method types")
    
    # Create a presentation using the template
    presentation = Presentation()
    
    # Load the template into the presentation's template manager
    template_name = presentation.template_manager.load(str(template_path))
    presentation._default_template = template_name
    
    # Slide 1: Create a slide with minimal parameters
    print("Creating slide 1 with minimal parameters (using defaults)...")
    slide1, grid1 = presentation.add_grid_slide(
        rows=2,
        cols=2,
        title="Using Generated Template",
        subtitle="Most formatting comes from template defaults"
    )
    
    # Add content with minimal parameters, letting the template provide defaults
    grid1.add_to_cell(
        row=0,
        col=0,
        content_func=slide1.add_text,
        text="This cell uses default font and alignment"
    )
    
    grid1.add_to_cell(
        row=0,
        col=1,
        content_func=slide1.add_text,
        text="This cell also uses defaults",
    )
    
    grid1.add_to_cell(
        row=1,
        col=0,
        content_func=slide1.add_text,
        text="This cell has custom formatting",
        font_size=20,  # Override default font size
        font_bold=True,  # Override default bold setting
        color=(180, 0, 0)  # Override default color
    )
    
    grid1.add_to_cell(
        row=1,
        col=1,
        content_func=slide1.add_text,
        text="This cell has custom alignment",
        align="right",  # Override default alignment
        vertical="bottom"  # Override default vertical alignment
    )
    
    # Slide 2: Create a slide with more cells
    print("Creating slide 2 with larger grid...")
    slide2, grid2 = presentation.add_grid_slide(
        rows=3,
        cols=3,
        title="More Grid Cells",
        subtitle="Still using template defaults"
    )
    
    # Add content to every cell
    for row in range(3):
        for col in range(3):
            grid2.add_to_cell(
                row=row,
                col=col,
                content_func=slide2.add_text,
                text=f"Cell ({row},{col})"
            )
    
    # Save the presentation
    output_path = OUTPUT_DIR / "008_generated_template.pptx"
    presentation.save(output_path)
    print(f"Saved presentation using generated template to: {output_path}")


if __name__ == "__main__":
    main()