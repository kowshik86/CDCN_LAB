# 📋 Complete Project Explanation

## What This Project Does (Simple Version)

**It translates math expressions into computer instructions.**

Think of it like translating:
- **English**: "Calculate x equals a plus b"
- **Computer language**: 
  ```
  MOV a , R1
  MOV b , R2
  ADD R1 , R2
  STOR R1 , R0
  ```

---

## 📥 INPUT - What You Give It

### File Format
A CSV file with exactly 2 columns named `left` and `right`:

```
left,right
x,a + b
y,x * c
z,y - d
```

### Column Meanings
- **`left`** = Where to store the result (variable name)
- **`right`** = The calculation to perform

### Rules
1. Operators must be space-separated: `a + b` (not `a+b`)
2. Supported operators: `+` `-` `*` `/`
3. Each `left` value must be unique
4. You can reference results from previous lines in later lines

### Example CSV
```csv
left,right
a,5
b,a + 10
c,b * 2
d,c - a
```

**What this means:**
- `a` = 5
- `b` = (5) + 10 = 15
- `c` = (15) * 2 = 30
- `d` = (30) - 5 = 25

---

## ⚙️ PROCESS - What The Program Does

### Step 1: Load CSV
- Opens the file
- Checks format is correct
- Displays what it found

### Step 2: Identify Elements
- Finds all **variable names** (a, b, c, x, y, z)
- Finds all **operators** (+, -, *, /)
- Removes duplicates

### Step 3: Allocate Registers
Assigns each variable to a "register" (like memory slots):
```
a → R0
b → R1
c → R2
x → R3
y → R4
z → R5
```

Think of registers like labeled boxes where values are stored.

### Step 4: Generate Instructions
For each expression, creates low-level instructions:
- `MOV` = Load a value
- `ADD` = Add two values
- `SUB` = Subtract
- `MUL` = Multiply
- `DIV` = Divide
- `STOR` = Save the result

### Step 5: Output Results
- Prints to screen
- Saves to file
- Shows statistics

---

## 📤 OUTPUT - What You Get

### On Screen (and in file)

```
THREE-ADDRESS CODE GENERATOR
============================================================
Input CSV file: input.csv
Expressions to process: 3

GENERATED THREE-ADDRESS CODE
============================================================

# Expression 1: x = a + b
  MOV a , R1      ← Load a into register 1
  MOV b , R2      ← Load b into register 2
  ADD R1 , R2     ← Add R1 and R2 (result in R1)
  STOR R1 , R0    ← Store R1 into register 0 (x's location)

# Expression 2: y = x * c
  MOV x , R0      ← Load x (from R0 where we stored it)
  MOV c , R3      ← Load c into register 3
  MUL R0 , R3     ← Multiply them
  STOR R3 , R4    ← Store result in register 4 (y's location)

GENERATION STATISTICS
============================================================
Total expressions processed: 3
Unique variables: 4
Registers allocated: 4
Operators used: +, *

Register Mapping:
  a -> R0
  b -> R1
  c -> R2
  x -> R3
  y -> R4

[SUCCESS] Output saved to: OUTPUT_INTERMEDIATE_CODE_GENERATOR/output_20251111_174704.txt
```

### Output Format Explained

Each instruction has the format: `INSTRUCTION operand1 , operand2`

| Instruction | What It Means | Example |
|-------------|--------------|---------|
| `MOV value , register` | Load a value | `MOV a , R1` means put `a` into register R1 |
| `ADD reg1 , reg2` | Add two registers | `ADD R1 , R2` means R1 = R1 + R2 |
| `SUB reg1 , reg2` | Subtract | `SUB R1 , R2` means R1 = R1 - R2 |
| `MUL reg1 , reg2` | Multiply | `MUL R1 , R2` means R1 = R1 * R2 |
| `DIV reg1 , reg2` | Divide | `DIV R1 , R2` means R1 = R1 / R2 |
| `STOR reg , var` | Store result | `STOR R1 , x` means store R1 to x |

---

## 🔍 Detailed Example Walkthrough

### INPUT
```csv
left,right
result,5 + 3
```

### PROCESSING

**Expression: `result = 5 + 3`**

1. **Allocate Registers**
   - result → R0 (where result will be stored)
   - 5 → constant
   - 3 → constant

2. **Generate Instructions**
   ```
   MOV 5 , R1      ← Step 1: Load 5 into register R1
   MOV 3 , R2      ← Step 2: Load 3 into register R2
   ADD R1 , R2     ← Step 3: Add them (R1 = R1 + R2 = 8)
   STOR R1 , R0    ← Step 4: Store result in R0 (variable 'result')
   ```

3. **What happened in memory**
   ```
   After MOV 5 , R1:
   ┌─────────┐
   │ R0 = ?  │
   │ R1 = 5  │
   │ R2 = ?  │
   └─────────┘
   
   After MOV 3 , R2:
   ┌─────────┐
   │ R0 = ?  │
   │ R1 = 5  │
   │ R2 = 3  │
   └─────────┘
   
   After ADD R1 , R2:
   ┌─────────┐
   │ R0 = ?  │
   │ R1 = 8  │ (was 5, now 5+3)
   │ R2 = 3  │
   └─────────┘
   
   After STOR R1 , R0:
   ┌─────────┐
   │ R0 = 8  │ ← result is now 8
   │ R1 = 8  │
   │ R2 = 3  │
   └─────────┘
   ```

### OUTPUT
```
MOV 5 , R1
MOV 3 , R2
ADD R1 , R2
STOR R1 , R0
```

---

## 🎯 Why Is This Important?

This is how **real compilers** work! When you write Python or Java code:

```
result = 5 + 3
```

Your computer doesn't directly understand that. The compiler converts it to intermediate code (like what this program does), which then gets converted to machine code the CPU can execute.

### Full Process
```
High-Level Code (Python)
    ↓
    x = a + b
    ↓
Intermediate Code (This Program)
    ↓
    MOV a , R1
    MOV b , R2
    ADD R1 , R2
    ↓
Assembly Code (x86)
    ↓
    mov eax, [a]
    add eax, [b]
    ↓
Machine Code (Binary)
    ↓
    10110000 01100001
```

---

## 🚀 Quick Start

### 1. Create CSV
```csv
left,right
x,2 + 3
y,x * 4
```

### 2. Run Program
```bash
python intermediatecodegenerator.py your_file.csv
```

### 3. See Output
- On screen immediately
- Saved to `OUTPUT_INTERMEDIATE_CODE_GENERATOR/output_*.txt`

---

## 📊 Real-World Example

### Mathematical Expression
```
Calculate: (a + b) * (c - d)
```

### Input CSV
```csv
left,right
sum,a + b
diff,c - d
result,sum * diff
```

### Generated Three-Address Code
```
# Expression 1: sum = a + b
  MOV a , R1
  MOV b , R2
  ADD R1 , R2
  STOR R2 , R0

# Expression 2: diff = c - d
  MOV c , R3
  MOV d , R4
  SUB R3 , R4
  STOR R4 , R1

# Expression 3: result = sum * diff
  MOV sum , R0
  MOV diff , R1
  MUL R0 , R1
  STOR R1 , R2
```

---

## ✅ Summary

| Aspect | Details |
|--------|---------|
| **INPUT** | CSV file with 2 columns: left (variable), right (expression) |
| **PROCESS** | Parse CSV → Find variables → Allocate registers → Generate instructions |
| **OUTPUT** | Assembly-like three-address code (MOV, ADD, SUB, MUL, DIV, STOR) |
| **FILE** | Automatically saved to OUTPUT_INTERMEDIATE_CODE_GENERATOR/ with timestamp |
| **PURPOSE** | Demonstrate how compilers generate intermediate code |
| **OPERATORS** | `+` (add), `-` (subtract), `*` (multiply), `/` (divide) |
| **REGISTERS** | R0, R1, R2, R3, ... (one per unique variable) |

---

## 🎓 Learn More

- **SUMMARY.md** - Quick one-page overview
- **EXPLANATION.md** - Detailed technical explanation
- **VISUAL_GUIDE.md** - Diagrams and visual walkthroughs
- **USAGE_GUIDE.md** - Complete technical reference
- **README.md** - Quick start guide

---

**This is a simplified version of what real compilers do!**
