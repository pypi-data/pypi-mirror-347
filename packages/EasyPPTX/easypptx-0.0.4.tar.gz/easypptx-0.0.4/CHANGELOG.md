# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2025-05-12

### Added
- New Grid Features
  - Enhanced row-level Grid access API with `grid[row].add_xxx()` methods
  - Added `reset()` method to GridRowProxy to allow reusing rows
  - Implemented convenient `add_textbox()` alias for consistent API
- New Slide Creation Methods with Consistent API
  - Added `add_grid_slide` for creating slides with grid layouts
  - Added `add_pyplot_slide` for creating slides with matplotlib/seaborn figures
  - Added `add_image_gen_slide` for creating slides with images
  - All methods support title, subtitle, and flexible positioning
  - Consistent parameter naming and return value patterns
  - Return both the slide and the content object for easy customization
- Updated add_autogrid_slide method to support empty grids
- Added examples demonstrating all the new features
- Comprehensive tests for the new functionality

## [0.0.3] - 2025-05-12

### Added
- Enhanced Grid access API with intuitive syntax
  - Added `grid[row, col].add_xxx()` for direct cell access
  - Added `grid[row].add_xxx()` for sequential row operations
- Added GridCellProxy and GridRowProxy classes to support new functionality
- Added example file demonstrating enhanced grid access patterns
- Updated documentation to reflect new features

## [0.0.2] - Previous release

### Added
- Initial project structure
- Basic PowerPoint presentation creation functionality
- Grid layout system
- Basic examples

[0.0.4]: https://github.com/Ameyanagi/easypptx/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/Ameyanagi/easypptx/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/Ameyanagi/easypptx/releases/tag/v0.0.2
