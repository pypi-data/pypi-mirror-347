# 🔧 LogicTools

## 🧠 Overview

**LogicTools** is a Python package that provides utility functions for **string** and **mathematical** operations.
It simplifies common tasks like text manipulation and basic calculations for developers.

---

## ✨ Features

### 🔤 String Utilities

* 🔠 Convert strings to **uppercase**
* 🔄 Reverse strings
* 🔢 Count characters in a string

### ➗ Mathematical Utilities

* 🧮 Calculate **factorials**
* 🛡️ Perform division with **proper error handling**

---

## 📦 Installation

Install LogicTools using pip:

```bash
pip install logictools
```

---

## 🚀 Usage

### 🔤 String Utilities

```python
from logictools import convert_to_uppercase, reverse_string, character_count

text = "Hello"
print(convert_to_uppercase(text))  # Output: HELLO
print(reverse_string(text))        # Output: olleH
print(character_count(text))       # Output: 5
```

### ➗ Mathematical Utilities

```python
from logictools import factorial, divide

# Factorial calculation
print(factorial(5))   # Output: 120

# Division with error handling
print(divide(10, 2))  # Output: 5.0

try:
    print(divide(10, 0))  # Raises ZeroDivisionError
except ZeroDivisionError as e:
    print(f"Error: {e}")
```

---

## 📁 Project Structure

```bash
logictools/
│—— logictools/            
│   ├— __init__.py        
│   ├— math_utils.py      # Math functions (factorial, divide)
│   └— string_utils.py    # String functions
│
│—— tests/                 # Unit tests
│   ├— test_math_utils.py
│   └— test_string_utils.py
│
│—— .github/               # GitHub Actions CI/CD
│   └— workflows/
│       └— python-package.yml
│
│—— .gitignore             
│—— pyproject.toml         
│—— README.md              
│—— LICENSE                
│—— requirements.txt       
```

---

## 🧪 Development

### ✅ Running Tests

```bash
poetry install --with dev
poetry run pytest
```

### 🛠️ Building the Package

```bash
python -m build
```

---

## 🚀 Publishing

📦 **Create a GitHub release**
✅ The CI/CD pipeline will **automatically publish to PyPI**

---

## ⚠️ Error Handling

The `divide` function includes:

* ❌ Division by zero → `ZeroDivisionError`
* 🗾 Invalid input types → `TypeError`

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](./LICENSE) file for details.

---

## 👤 Contact

* **Author:** RANGDAL PAVANSAI
* 📧 Email: [psai49779@gmail.com](mailto:psai49779@gmail.com)
* 🐙 GitHub: [Pavansai20054](https://github.com/Pavansai20054)
* 💼 LinkedIn: [rangdal-pavansai](https://www.linkedin.com/in/rangdal-pavansai)

---

> 🔍 *Simplify your logic. One tool at a time — LogicTools.*
