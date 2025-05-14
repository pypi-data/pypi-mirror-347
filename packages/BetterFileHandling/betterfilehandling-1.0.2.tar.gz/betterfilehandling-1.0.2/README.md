# BetterFileHandling  
**A Modular Python Library for Efficient and Secure File Operations**

**BetterFileHandling** is a developer-focused utility library that simplifies and streamlines common file operations in Python. Designed for clarity, reliability, and modularity, this package offers well-structured methods for reading, writing, encoding, and managing files with clean exception handling.

---

## Features

- Modular and extensible architecture  
- Read/write support for plain text and JSON  
- Line-by-line and range-based reading  
- Base64 and plain encoding/decoding  
- Detailed file metadata inspection  
- Safe file operations: copy, move, rename, delete  
- File listing with filtering  
- Consistent error handling

---

## Module Overview

| Module | Description | Key Functions |
|--------|-------------|----------------|
| `reading.py` | Flexible file reading methods | `read_text()`, `readline()`, `read_lines()`, `read_all_lines()`, `read_until()` |
| `writing.py` | Structured file writing methods | `write_text()`, `write_lines()`, `write_json()` |
| `security.py` | File encoding and decoding | `encode_file()`, `decode_file()`, `encode_file_base64()`, `decode_file_base64()` |
| `file_management.py` | File and directory operations | `get_file_info()`, `copy_file()`, `move_file()`, `rename_file()`, `list_files_in_directory()` |

---

## Installation

BetterFileHandling is published on PyPI. Install it using pip:

```bash
pip install BetterFileHandling
```

To use specific modules:

```python
from reading import read_text
from writing import write_json
from file_management import get_file_info
from security import encode_file_base64
```

---

## Usage Examples

**Read a specific line:**
```python
from reading import readline

line = readline('example.txt', 3)
print(line)
```

**Write multiple lines to a file:**
```python
from writing import write_lines

write_lines('log.txt', ['Process started.', 'Success.'], clear=True)
```

**Encode file contents to Base64:**
```python
from security import encode_file_base64

encoded = encode_file_base64('data.txt')
```

**Move a file safely:**
```python
from file_management import move_file

move_file('data.csv', 'backup/data.csv')
```

---

## Error Handling Philosophy

All functions are designed to provide:

- Clear, consistent error messages  
- Meaningful exceptions  
- Safe defaults that prevent destructive actions  

This ensures predictable behavior and safer integration into automation scripts or production systems.

---

## Compatibility

- Python 3.8 and above  
- Cross-platform support: Linux, Windows, macOS

---

## License

This project is released under the MIT License. See the `LICENSE` file for details.

---

## Author

**Aksh**  
Front-End Engineer, UI/UX Designer, and Python Developer  
Created and maintained by a passionate 9th-grade developer from Delhi.
