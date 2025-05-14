# PyCodar: A Radar for Your Code
**A simple tool for auditing and understanding your codebase.**

## Requirements
- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Quick Install
The easiest way to install PyCodar is using pip:
```bash
pip install pycodar
```

After installation, you should be able to use the `pycodar` command from anywhere in your terminal.

### Development Install
If you want to contribute to PyCodar or run it from source:
```bash
# Clone the repository
git clone https://github.com/QuentinWach/pycodar.git
cd pycodar

# Install in development mode
pip install -e .
```

## Usage
After installation, you can use PyCodar from the command line:
```bash
pycodar stats [directory]
```

Below, you can see the result for PyCodar when we use `pycodar stats`. Note that PyCodar ingores files and directories specified in `.gitignore` and `.codarignore` (where you can optionally ignore gitignore).

```