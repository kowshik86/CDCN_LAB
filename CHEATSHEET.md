# 🎯 Quick Reference Cheat Sheet

## INPUT → PROCESS → OUTPUT

```
INPUT (CSV)          PROCESS                    OUTPUT (Instructions)
───────────────────  ─────────────────────────  ────────────────────────
left,right           1. Load CSV                MOV a , R1
x,a + b              2. Find variables         MOV b , R2
y,x * c              3. Allocate registers     ADD R1 , R2
                     4. Generate instructions  STOR R1 , R0
                     5. Save to file           
                                               MOV x , R0
                                               MOV c , R3
                                               MUL R0 , R3
                                               STOR R3 , R4
```

---

## 📝 CSV Format

### Correct ✅
```csv
left,right
x,a + b
y,x * c
z,y - d
```

### Wrong ❌
```csv
left,right
x,a+b          ← No spaces around operator
y = x * c      ← Has equals sign
z,y-d          ← No spaces
```

---

## 🔢 Instructions Reference

```
MOV value , register      Load a value
ADD reg1 , reg2          Add two registers
SUB reg1 , reg2          Subtract
MUL reg1 , reg2          Multiply
DIV reg1 , reg2          Divide
STOR register , variable Store result
```

---

## 🚀 How to Run

```bash
# Basic
python intermediatecodegenerator.py input.csv

# Custom file
python intermediatecodegenerator.py your_file.csv

# View output
cat OUTPUT_INTERMEDIATE_CODE_GENERATOR/output_*.txt
```

---

## 📊 Example: x = (a + b) * c

| Step | Operation | Code |
|------|-----------|------|
| 1 | Load a | `MOV a , R1` |
| 2 | Load b | `MOV b , R2` |
| 3 | Add a + b | `ADD R1 , R2` |
| 4 | Load c | `MOV c , R3` |
| 5 | Multiply result * c | `MUL R1 , R3` |
| 6 | Store to x | `STOR R1 , R0` |

---

## 💡 Key Concepts

| Term | Meaning |
|------|---------|
| **Register** | A memory location (R0, R1, R2, etc.) |
| **Variable** | A named value (a, b, x, y, etc.) |
| **Operand** | A value used in operation (a, b, 5, etc.) |
| **Operator** | Mathematical symbol (+, -, *, /) |
| **Three-Address Code** | Instructions with max 3 operands |

---

## 📁 Output Files

```
OUTPUT_INTERMEDIATE_CODE_GENERATOR/
└── output_YYYYMMDD_HHMMSS.txt

Example: output_20251111_174704.txt
```

---

## ✅ Checklist

- [ ] CSV has 2 columns: left, right
- [ ] Operators are space-separated (a + b)
- [ ] File exists in current directory
- [ ] Run: `python intermediatecodegenerator.py filename.csv`
- [ ] Check console output
- [ ] Check file in OUTPUT_ folder

---

## ❌ Common Mistakes

| Mistake | Fix |
|---------|-----|
| `a+b` | Use `a + b` (spaces) |
| `x = a + b` | Remove equals, use just `a + b` |
| `file.csv` not found | Check file is in same directory |
| No spaces in CSV | Use: `left , right` |

---

## 📖 Quick Learn

1. **Read**: SUMMARY.md (2 min)
2. **Understand**: COMPLETE_EXPLANATION.md (5 min)
3. **Visualize**: VISUAL_GUIDE.md (3 min)
4. **Try it**: Create CSV → Run program → Check output

---

## 🎓 What's It For?

**Compiler intermediate code generation** - converts:
```
High-level:   x = a + b
              ↓
Intermediate: MOV a , R1
              MOV b , R2
              ADD R1 , R2
              STOR R1 , R0
              ↓
Low-level:    (CPU instructions)
```

---

**Master this cheat sheet, you understand the whole project!** ⚡
