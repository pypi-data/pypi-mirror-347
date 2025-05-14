#!/usr/bin/env python
"""
009_generate_template_one_line.py - Generate Template in One Line

This example demonstrates:
1. Generating a default template with a single line of Python code
2. Using it to create consistently styled presentations
"""

from pathlib import Path

from easypptx import Presentation, generate_template_with_comments

# Example of generating a template with a single line of code:
# generate_template_with_comments("path/to/your/template.toml")


def main():
    """Run the example."""
    print("Generating a default template with a single line of code...")
    
    # Set up paths
    output_dir = Path("output/templates")
    output_dir.mkdir(exist_ok=True, parents=True)
    template_path = output_dir / "one_line_template.toml"
    
    # ONE LINE TO GENERATE A TEMPLATE:
    generate_template_with_comments(template_path)
    
    print(f"Template generated at: {template_path}")
    print(f"Template includes global defaults and commented sections for customization")
    
    # Now use the template to create a presentation
    print("\nCreating a presentation using the generated template...")
    
    # Create a presentation
    presentation = Presentation()
    
    # Load the template into the presentation
    template_name = presentation.template_manager.load(str(template_path))
    presentation._default_template = template_name
    
    # Add a slide using template defaults
    slide1, grid1 = presentation.add_grid_slide(
        title="Created with One-Line Template",
        subtitle="All styling comes from the template",
        rows=2,
        cols=2
    )
    
    # Add content to the grid cells
    for row in range(2):
        for col in range(2):
            grid1.add_to_cell(
                row=row,
                col=col,
                content_func=slide1.add_text,
                text=f"Cell ({row},{col}) with template styling"
            )
    
    # Save the presentation
    output_path = Path("output") / "one_line_template_example.pptx"
    presentation.save(output_path)
    print(f"Presentation saved to: {output_path}")
    print("This presentation uses styling from the template generated with one line of code")


if __name__ == "__main__":
    main()