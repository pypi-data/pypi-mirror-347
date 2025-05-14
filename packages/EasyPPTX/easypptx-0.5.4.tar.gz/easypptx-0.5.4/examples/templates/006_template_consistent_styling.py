#!/usr/bin/env python
"""
006_template_consistent_styling.py - Consistent Slide Styling with Templates

This example demonstrates:
1. Creating a TOML template with specific styling preferences (title padding, alignment)
2. Using the template to create slides with consistent styling
3. Adding different types of slides that all use the same styling from the template
"""

from pathlib import Path
import tomli_w

from easypptx import Presentation
from easypptx.template import TemplateManager

# Set up paths
CURRENT_DIR = Path(__file__).parent
ROOT_DIR = CURRENT_DIR.parent.parent
TEMPLATE_DIR = ROOT_DIR / "templates"
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Create template output directory
TEMPLATE_OUTPUT_DIR = OUTPUT_DIR / "templates"
TEMPLATE_OUTPUT_DIR.mkdir(exist_ok=True)


def create_custom_template():
    """Create a custom template with specific styling preferences."""
    # Define a template with left-aligned titles and consistent title padding
    custom_template = {
        # Background color (RGB tuple as list for TOML compatibility)
        "bg_color": [245, 245, 245],  # Light gray background
        # Title configuration - left-aligned with padding
        "title": {
            "text": "Default Title",
            "position": {"x": "10%", "y": "10%", "width": "80%", "height": "15%"},
            "font": {"name": "Arial", "size": 32, "bold": True},
            "align": "left",  # Left alignment for all titles
            "vertical": "middle",
            "color": [50, 62, 79],  # Dark blue color
            "padding": {"top": "2%", "left": "5%"},  # Title padding
        },
        # Content area configuration
        "content_area": {
            "position": {"x": "10%", "y": "30%", "width": "80%", "height": "60%"},
            "align": "left",  # Left alignment for content
        },
        # Footer configuration
        "footer": {
            "text": "Created with EasyPPTX",
            "position": {"x": "5%", "y": "90%", "width": "90%", "height": "5%"},
            "font": {"name": "Arial", "size": 12, "bold": False},
            "align": "right",
            "color": [100, 100, 100],  # Gray color for footer
        },
    }

    # Save the template
    template_path = TEMPLATE_OUTPUT_DIR / "consistent_styling.toml"
    with open(template_path, "wb") as f:
        tomli_w.dump(custom_template, f)

    return template_path


def main():
    """Run the example."""
    print("Creating and using a custom template for consistent slide styling...")

    # Create custom template
    template_path = create_custom_template()
    print(f"Created custom template: {template_path}")

    # Initialize template manager and load our template
    template_manager = TemplateManager()
    template_name = template_manager.load(str(template_path))

    # Create presentation with our custom template
    presentation = Presentation()

    # Register the template with the presentation's template manager
    presentation.template_manager.register(template_name, template_manager.get(template_name))

    # Create slides using our template
    # Slide 1: Simple title slide
    slide1 = presentation.add_slide_from_template(template_name)
    # Update title text - all other styling comes from template
    slide1.add_text(
        text="Consistent Styling with Templates",
        x="10%",
        y="10%",
        width="80%",
        height="15%",
    )
    slide1.add_text(
        text="Using templates to ensure consistent formatting",
        x="10%",
        y="30%",
        width="80%",
        height="10%",
        font_size=24,
    )

    # Slide 2: Bullet points
    slide2 = presentation.add_slide_from_template(template_name)
    # Only specify the text - formatting comes from template
    slide2.add_text(
        text="Key Benefits of Templates",
        x="10%",
        y="10%",
        width="80%",
        height="15%",
    )
    slide2.add_text(
        text="• Consistent styling across all slides\n"
        "• Define defaults for colors, alignment, and fonts\n"
        "• Specify title padding and positioning once\n"
        "• Reduce repetitive formatting arguments\n"
        "• Easily update the entire presentation's look",
        x="10%",
        y="30%",
        width="80%",
        height="60%",
        font_size=24,
    )

    # Slide 3: Content with bullet points
    slide3 = presentation.add_slide_from_template(template_name)
    slide3.add_text(
        text="Working with Template Parameters",
        x="10%",
        y="10%",
        width="80%",
        height="15%",
    )

    # Left column
    slide3.add_text(
        text="Template Parameters:",
        x="10%",
        y="30%",
        width="35%",
        height="10%",
        font_size=20,
        font_bold=True,
    )
    slide3.add_text(
        text="• Title alignment\n• Title padding\n• Background color\n• Font settings\n• Default positioning",
        x="10%",
        y="40%",
        width="35%",
        height="40%",
        font_size=18,
    )

    # Right column
    slide3.add_text(
        text="Benefits:",
        x="55%",
        y="30%",
        width="35%",
        height="10%",
        font_size=20,
        font_bold=True,
    )
    slide3.add_text(
        text="• Shorter, cleaner code\n• Consistent look and feel\n• Easier maintenance\n• Professional appearance",
        x="55%",
        y="40%",
        width="35%",
        height="40%",
        font_size=18,
    )

    slide4, grid = presentation.add_grid_slide(title="test", cols=2, rows=1)

    # Save the presentation
    output_path = OUTPUT_DIR / "006_template_consistent_styling.pptx"
    presentation.save(output_path)
    print(f"Saved presentation with consistent styling to: {output_path}")


if __name__ == "__main__":
    main()
