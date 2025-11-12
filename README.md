# Three-Address Code Generator

Generates intermediate code from CSV files containing arithmetic expressions.

## Quick Start

```bash
# Install dependency
python -m pip install pandas

# Run program
python intermediatecodegenerator.py input.csv

# Or with custom CSV
python intermediatecodegenerator.py your_file.csv
```

## CSV Format

```csv
left,right
x,a + b
y,x * c
z,y - d
```

**Rules:** Space-separate operators and operands (e.g., `a + b` not `a+b`)

## Features

✅ Generate three-address code with automatic register allocation  
✅ File output (timestamped)  
✅ Custom CSV input via command-line  
✅ Full error handling  
✅ Statistics reporting  

## Output Example

```
MOV x , R6
MOV a , R2
MOV b , R1
ADD R2 , R1
STOR R1 , R6
```

## Documentation

- **README.md** - This file (quick start)
- **EXPLANATION.md** - Complete guide with examples
- **CHEATSHEET.md** - Quick reference
