#!/usr/bin/env python
"""
007_template_defaults.py - Using Template Defaults for Consistent Styling

This example demonstrates:
1. Loading a template with default method arguments
2. Creating slides that use these defaults for consistent styling
3. Overriding specific defaults when needed
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
    print("Creating a presentation with template defaults...")

    # Path to the template TOML file with defaults
    template_file = TEMPLATE_DIR / "grid_defaults.toml"
    
    # Initialize template manager and load our template
    template_manager = TemplateManager()
    template_name = template_manager.load(str(template_file))
    print(f"Loaded template: {template_name}")
    
    # Create a new presentation
    presentation = Presentation()
    
    # Register the template with the presentation to use its defaults
    template_data = template_manager.get(template_name)
    presentation.template_manager.register(template_name, template_data)
    presentation._default_template = template_name
    
    # Slide 1: Use all defaults from template
    print("Creating slide 1 with default template settings...")
    slide1, grid1 = presentation.add_grid_slide(
        rows=2,
        cols=2,
        title="Using Template Defaults",
        subtitle="All styling comes from the template"
    )
    
    # Add content to grid - the positioning and styling will use defaults
    grid1.add_to_cell(
        row=0, 
        col=0, 
        content_func=slide1.add_text,
        text="This text uses default font, size, and alignment"
    )
    
    grid1.add_to_cell(
        row=0, 
        col=1, 
        content_func=slide1.add_text,
        text="No need to specify background color"
    )
    
    grid1.add_to_cell(
        row=1, 
        col=0, 
        content_func=slide1.add_text,
        text="Default positioning is applied"
    )
    
    grid1.add_to_cell(
        row=1, 
        col=1, 
        content_func=slide1.add_text,
        text="Consistent padding from template"
    )
    
    # Slide 2: Override some defaults
    print("Creating slide 2 with some overridden settings...")
    slide2, grid2 = presentation.add_grid_slide(
        rows=2,
        cols=2,
        title="Overriding Template Defaults",
        subtitle="Selectively change specific settings",
        title_align="center",  # Override the default left alignment
        padding=12.0,          # Override default padding
    )
    
    # Add content with some overrides
    grid2.add_to_cell(
        row=0, 
        col=0, 
        content_func=slide1.add_text,
        text="Left-aligned text (template default)",
    )
    
    grid2.add_to_cell(
        row=0, 
        col=1, 
        content_func=slide1.add_text,
        text="Center-aligned text (override)",
        align="center",  # Override default alignment
    )
    
    grid2.add_to_cell(
        row=1, 
        col=0, 
        content_func=slide1.add_text,
        text="Default font size (from template)",
    )
    
    grid2.add_to_cell(
        row=1, 
        col=1, 
        content_func=slide1.add_text,
        text="Larger font (override)",
        font_size=22,  # Override default font size
        font_bold=True,  # Override default bold setting
    )
    
    # Slide 3: Create a slide with a different grid layout
    print("Creating slide 3 with a different grid configuration...")
    slide3, grid3 = presentation.add_grid_slide(
        rows=3,
        cols=3,
        title="Grid With More Cells",
        subtitle="Still using template defaults"
    )

    # Add text to every other cell in a checkerboard pattern
    for row in range(3):
        for col in range(3):
            if (row + col) % 2 == 0:  # Checkerboard pattern
                grid3.add_to_cell(
                    row=row,
                    col=col,
                    content_func=slide3.add_text,
                    text=f"Cell ({row},{col})",
                    align="center",
                    vertical="middle",
                    color=[0, 0, 150]  # Dark blue text color
                )
    
    # Save the presentation
    output_path = OUTPUT_DIR / "007_template_defaults.pptx"
    presentation.save(output_path)
    print(f"Saved presentation with template defaults to: {output_path}")


if __name__ == "__main__":
    main()