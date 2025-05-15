# LogicTools

## Overview
LogicTools is a Python package that provides utility functions for string and mathematical operations. It is designed to simplify common tasks such as string manipulation and basic mathematical calculation.

## Features
- Convert strings to uppercase
- Reverse strings
- Count characters in a string
- Perform basic mathematical operations (factorial calculation)

## Installation
Install LogicTools using pip:

```sh
pip install logictools
```

## Usage
### String Utilities

```python
from logictools import convert_to_uppercase, reverse_string, character_count

text = "Hello"
print(convert_to_uppercase(text))  # Output: HELLO
print(reverse_string(text))        # Output: olleH
print(character_count(text))       # Output: 5
```

### Mathematical Utilities

```python
from logictools import factorial

print(factorial(5))   # Output: 120
```

## Project Structure

```bash
logictools/
│── logictools/            # Package source code
│   ├── __init__.py        # Required for a Python package
│   ├── math_utils.py      # Math functions
│   ├── string_utils.py    # String functions
│
│── tests/                 # Unit tests
│   ├── test_math_utils.py
│   ├── test_string_utils.py
│
│── .github/               # GitHub Actions CI/CD
│   ├── workflows/
│       ├── python-package.yml
│
│── .gitignore             # Ignore unnecessary files
│── pyproject.toml         # Modern package configuration
│── README.md              # Documentation
│── LICENSE                # License file
│── requirements.txt       # Dependencies
```

## Steps to Build and Deploy

### 1️⃣ Set Up the Project

```sh
mkdir logictools && cd logictools
mkdir logictools tests .github/workflows
```

Create essential files:

```sh
touch logictools/__init__.py logictools/math_utils.py logictools/string_utils.py
```

### 2️⃣ Implement Functions
Example `math_utils.py`:

```python
#Calculates the factorial of a number.
def factorial(n):
    try:
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    except ValueError as e:
        return f"{e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
```

Example `string_utils.py`:

```python
def convert_to_uppercase(text):
    return text.upper()  # Converts a string to uppercase.

def reverse_string(text):
    return text[::-1]  # Reverses a given string.

def character_count(text):
    return len(text)  # Returns the length of the string.
```
### 🔹Now add the created files inside `__init__.py`
```python
from .string_utils import convert_to_uppercase, reverse_string, character_count
from .math_utils import factorial
```

### 3️⃣ Code Test
  - Now, after writing the code we must test it by Unit Test:
    - You must test for all files.
    - Here is the test code for `math_utils.py` file.
    ```python
    import pytest
    from logictools import math_utils

    def test_factorial():
        assert math_utils.factorial(5) == 120
        assert math_utils.factorial(0) == 1
    ```

    - Here is the test code for `string_util.py` file.
  
    ```python
    import pytest
    from logictools import string_utils

    def test_convert_to_uppercase():
        assert string_utils.convert_to_uppercase("hello") == "HELLO"

    def test_reverse_string():
        assert string_utils.reverse_string("hello") == "olleh"

    def test_character_count():
        assert string_utils.character_count("Hello") == 5
    ```

### 4️⃣ Create `pyproject.toml` file
  - This is the modern way to define a package.
  
```toml
[tool.poetry]
name = "logictools"           # Name of your package
version = "0.1.3"             # Current version of your package
description = "A simple utility package for string and math functions"
authors = ["RANGDAL PAVANSAI <psai49779@gmail.com>"]
license = "MIT"               # License type (MIT in this case)
readme = "README.md"          # Points to your README file

[tool.poetry.dependencies]
python = "^3.7"               # Your package supports Python 3.7 and later.

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"               # Your package requires pytest version 7.0 or higher for testing.

[build-system]
requires = ["poetry-core>=1.0.0"]       # Specifies that poetry-core (version 1.0.0 or later) is required to build the package.
build-backend = "poetry.core.masonry.api"    # Uses poetry.core.masonry.api as the build system.
```

### 5️⃣ Create `requirement.txt`
- This lists dependencies

  ```sh
  touch requirements.txt
  ```

- In `requirements.txt` add the packages that are required or your project to run.

### 6️⃣ Create `.gitignore`
- To ignore unnecessary files:

```sh
# Ignore Python cache & build files
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
build/
dist/
venv/
```
### 7️⃣ Build & Test Your Package Locally

1. Install `build` Tool
   
    ```cmd
    pip install build
    ```

2. Build your package

    ```cmd
    python -m build
    ```

  - This creates a `dist/` folder containing:

    ```python
    dist/
      my_package-0.1.0-py3-none-any.whl
      my_package-0.1.0.tar.gz
    ```

3. Test Your Package

```python
pip install dist/NAME-OF-YOUR-PACKAGE-0.1.0-py3-none-any.whl
python -c "import NAME-OF-YOUR-PACKAGE; print(NAME-OF-YOUR-PACKAGE.factorial(5))"
```

### 8️⃣ Set Up GitHub Actions for CI/CD
1. Create `.github/workflows/python-package.yml`:

```yaml
name: Python Package CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  release:
    types: [created]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: pytest

  build:
    name: Build and Publish Package
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'release'
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install Build Tools
        run: |
          pip install --upgrade pip
          pip install build twine
      - name: Build Package
        run: python -m build
      - name: Publish to PyPI
        env:
          PYPI_USERNAME: ${{ secrets.PYPI_USERNAME }}
          PYPI_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
        run: twine upload dist/* -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD"
```

### 9️⃣ Securely Store PyPI Credentials
1. Go to **GitHub repo → Settings → Secrets and variables → Actions**
2. Add:
   - `PYPI_USERNAME`: Your PyPI username
   - `PYPI_PASSWORD`: Your PyPI API Token

### 🔟 Publish Package to PyPI
1. Push your code:

```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/logictools.git
git push -u origin main
```
2. Create a GitHub release matching `pyproject.toml` version.
3. The package will automatically be built and published to PyPI.

### 11. Install, and Use

```sh
pip install logictools
python -c "from logictools import factorial; print(factorial(5))"
```

## Note: 
  - Everytime you commit new file you much change the version of your package in pyproject.toml

## License
This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

## Contact
- **Email:** psai49779@example.com
- **GitHub:** https://www.linkedin.com/in/rangdal-pavansai/
- **LinkedIn:** https://github.com/Pavansai20054