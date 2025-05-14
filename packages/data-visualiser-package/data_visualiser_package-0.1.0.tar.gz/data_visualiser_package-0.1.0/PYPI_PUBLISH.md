# PyPI Publishing Guide

This guide outlines how to build and publish the data-visualiser-package to PyPI.

## Prerequisites

Ensure you have the necessary tools:

```bash
pip install build twine
```

## Building the Package

1. Navigate to the root directory of the project:

```bash
cd /path/to/data_visualiser_package
```

2. Build the distribution packages:

```bash
python -m build
```

This will create both source and wheel distributions in the `dist/` directory.

## Publishing to PyPI

### Publishing to Test PyPI (Recommended for testing)

1. Upload to Test PyPI:

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

2. Install from Test PyPI to verify:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ data-visualiser-package
```

### Publishing to PyPI

Once you've confirmed everything works on TestPyPI, you can publish to the main PyPI:

```bash
python -m twine upload dist/*
```

## Versioning

When releasing a new version:

1. Update the version number in:
   - `pyproject.toml`
   - `setup.py`
   - `src/data_visualiser_package/__init__.py`

2. Add release notes to the README.md or CHANGELOG.md file.

## Cleaning Up

Remove build directories before rebuilding:

```bash
rm -rf build/ dist/ *.egg-info/
```
