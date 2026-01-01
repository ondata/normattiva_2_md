# Improve CLI Help Output with Rich

## Summary
Enhance the CLI help display by using the Rich library to provide a more readable, visually appealing, and organized help output when no arguments are provided or when `--help` is invoked.

## Motivation
- The current argparse help output is plain text and can be difficult to scan, especially with the extensive list of CLI options and examples
- Rich provides better formatting with syntax highlighting, colors, tables, and organized sections
- Improved readability makes it easier for users to discover and understand available options
- Professional help output improves user experience and tool discoverability

## Impact
- **CLI Interface**: Replace `argparse.RawDescriptionHelpFormatter` with Rich-based formatting
- **Dependencies**: Add Rich to `setup.py` and `pyproject.toml`
- **Code Changes**: Create new rich-based help formatter or integrate Rich directly in cli.py
- **Compatibility**: Maintain backward compatibility - same arguments and behavior, just improved display
- **Cross-platform**: Rich works on all platforms including Windows

## Open Questions / Risks
- Rich adds a new dependency - must evaluate if this aligns with minimal dependency policy
- Need to ensure help text remains readable when terminal doesn't support colors (Rich handles this automatically)
- Test that Rich formatting doesn't break PyInstaller builds for executables
