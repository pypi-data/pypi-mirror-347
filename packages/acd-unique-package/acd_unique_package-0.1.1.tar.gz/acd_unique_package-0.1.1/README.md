# Python Packaging Example

This is a simple Python package that demonstrates how to set up and install a Python project in **editable mode**. Editable mode allows you to make changes to the source code and immediately see the effects without reinstalling the package.

## What is Editable Mode?

When you install a Python package in editable mode using:

```bash
pip install -e .
```

The package is not copied into the `site-packages` directory. Instead, a reference (via a `.pth` file) is created, pointing to the source code directory. This is particularly useful during development, as it allows you to:

- Modify the source code directly.
- Test changes without needing to reinstall the package.

## Installation

To install this package in editable mode, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/python-packaging.git
   cd python-packaging-01/my_package
   ```

2. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Usage

After installation, you can import and use the package in your Python scripts. For example:

```python
import your_package_name

# Example usage
your_package_name.some_function()
```