from easypptx import Presentation

# Create a new presentation
pres = Presentation(template_toml="template.toml")

# Create a new slide with a title and grid layout
slide, grid = pres.add_grid_slide(title="Key Features", cols=3, rows=2, height="33%")

# Add content to the grid cells
grid[0].add_text(
    text="1. Easy-to-Use API",
    font_size=24,
    font_bold=True,
    align="left",
    vertical="top",
)

grid[1].add_text(
    text="2. Customizable Layouts",
    font_size=24,
    font_bold=True,
    align="left",
    vertical="top",
)

grid[2].add_text(
    text="3. Flexible Content Management",
    font_size=24,
    font_bold=True,
    align="left",
    vertical="top",
)

grid[3].add_text(
    text="4. Enhanced Row-Based API",
    font_size=24,
    font_bold=True,
    align="left",
    vertical="top",
)

grid[4].add_text(
    text="5. Enhanced Row-Based API",
    font_size=24,
    font_bold=True,
    align="left",
    vertical="top",
)

# Save the presentation
pres.save("presentation.pptx")
