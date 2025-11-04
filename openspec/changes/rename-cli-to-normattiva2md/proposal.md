# Rename CLI from akoma2md to normattiva2md

## Summary
Rename the command-line interface from `akoma2md` to `normattiva2md` to better reflect the tool's focus on Italian legal documents from normattiva.it.

## Motivation
The current CLI name `akoma2md` is generic and doesn't clearly indicate the tool's specialization in converting Italian legal documents from normattiva.it. A more descriptive name like `normattiva2md` would:
- Better communicate the tool's purpose
- Improve discoverability for Italian legal professionals
- Align with the domain-specific nature of the tool

## Impact
- **Breaking change**: Existing users will need to update their scripts/commands
- **Documentation**: README and all usage examples need updates
- **Packaging**: Entry points in setup.py and pyproject.toml need modification
- **Backward compatibility**: Consider providing a transition period with both names

## Alternatives Considered
1. Keep current name `akoma2md` - maintains generic appeal but less descriptive
2. Use `italaw2md` - shorter but less specific to the data source
3. Keep both names during transition - provides backward compatibility

## Implementation Plan
1. Update entry points in packaging files
2. Update all documentation and examples
3. Update build scripts and CI configuration
4. Consider deprecation warnings for old name during transition