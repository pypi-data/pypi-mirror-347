# KhmerNames

A simple Python library to generate random Khmer names with options to export to Excel or TXT.

## Example Usage

```python
from khmernames import get_full_name, generate_bulk_names, export_to_excel

print(get_full_name('male'))
names = generate_bulk_names(1000)
export_to_excel(names, "khmer_1000.xlsx")
```
