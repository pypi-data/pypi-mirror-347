# Publishing ci-cerberus to PyPI

This document contains instructions for publishing ci-cerberus to PyPI.

## Prerequisites

1. Create accounts:
   - Create an account on [PyPI](https://pypi.org/)
   - Create an account on [TestPyPI](https://test.pypi.org/) (for testing)

2. Install required tools:
   ```bash
   pip install build twine
   ```

## Publishing Steps

1. **Update Version Number**
   - Update the version in `pyproject.toml` before each release
   - Follow semantic versioning (MAJOR.MINOR.PATCH)

2. **Build the Distribution**
   ```bash
   python -m build
   ```
   This will create both wheel and source distribution in the `dist/` directory

3. **Test on TestPyPI First (Recommended)**
   ```bash
   # Upload to TestPyPI
   python -m twine upload --repository testpypi dist/*
   
   # Test installation from TestPyPI
   pip install --index-url https://test.pypi.org/simple/ ci-cerberus
   ```

4. **Upload to PyPI**
   ```bash
   python -m twine upload dist/*
   ```

5. **Verify Installation**
   ```bash
   pip install ci-cerberus
   ```

## Notes

- Always test the package on TestPyPI before publishing to the main PyPI
- Make sure all dependencies are correctly listed in `pyproject.toml`
- Ensure the README.md is up-to-date as it will be shown on the PyPI page
- Consider adding a CHANGELOG.md to track version changes

## Common Issues

1. If upload fails:
   - Check that you have the correct credentials
   - Ensure the version number is unique (PyPI doesn't allow overwriting versions)
   - Verify that the package name is available on PyPI

2. If installation fails:
   - Check that all dependencies are correctly specified
   - Verify that the package is compatible with the Python version

## Maintenance

After publishing:
1. Create a new GitHub release with the same version number
2. Tag the commit with the version number
3. Update the documentation if needed 