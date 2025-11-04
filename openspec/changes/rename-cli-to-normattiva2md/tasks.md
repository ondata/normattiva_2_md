# Tasks for CLI Rename: akoma2md → normattiva2md

## Phase 1: Core Implementation
- [ ] Update console_scripts entry point in setup.py from `akoma2md=convert_akomantoso:main` to `normattiva2md=convert_akomantoso:main`
- [ ] Update project.scripts entry in pyproject.toml from `akoma2md = "convert_akomantoso:main"` to `normattiva2md = "convert_akomantoso:main"`
- [ ] Update PyInstaller spec file name from `akoma2md` to `normattiva2md` (if exists)

## Phase 2: Documentation Updates
- [ ] Update README.md title from "Akoma2MD" to "Normattiva2MD"
- [ ] Replace all `akoma2md` command references with `normattiva2md` in README.md
- [ ] Update installation examples in README.md
- [ ] Update usage examples and help text in README.md
- [ ] Update CLI help text in convert_akomantoso.py if hardcoded

## Phase 3: Build and Distribution
- [ ] Update GitHub Actions workflow file names from `akoma2md-*` to `normattiva2md-*`
- [ ] Update Makefile build targets if they reference the old name
- [ ] Update any shell scripts that reference `akoma2md`
- [ ] Test PyInstaller binary generation with new name

## Phase 4: Testing and Validation
- [ ] Run existing test suite to ensure functionality unchanged
- [ ] Test CLI installation with `pip install -e .` and verify `normattiva2md --help` works
- [ ] Test PyInstaller build process produces correct binary name
- [ ] Verify all URL and file processing functionality works with new CLI name

## Phase 5: Backward Compatibility (Optional)
- [ ] Consider adding deprecated `akoma2md` entry point that shows warning and calls `normattiva2md`
- [ ] Update README with migration notes for existing users