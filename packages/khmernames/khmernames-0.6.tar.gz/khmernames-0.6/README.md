# Khmer Names Pro 🇰🇭

Generate unlimited Khmer names with duplicate filtering and clean output.

## Installation

```bash
pip install khmernames
```

## Usage

```python
from khmernames import generate_unlimited_names

names = generate_unlimited_names(1000)

with open("names.txt", "w", encoding="utf-8") as f:
    for name in names:
        f.write(name + "\n")
```
