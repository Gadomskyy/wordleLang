# WordleLang

**WordleLangInterpreter** is an esoteric programming language interpreter inspired by [Wordle](https://www.nytimes.com/games/wordle/index.html). It enforces a unique constraint: **you must include the current day's Wordle solution in your program** — otherwise, it won't run!

---

## 📦 Features

-  Pulls today’s official Wordle answer from the NYT API.
-  Executes a custom language using valid 5-letter Wordle words as variable names.
-  Supports basic arithmetic, comparisons, and conditional logic.
-  Validates that all variable names are:
  - Not reserved keywords.
  - Present in the official Wordle word list.
-  Rejects programs that don't use today’s Wordle word.

---

### 🔧 Requirements

- Python 3.7+
- Internet connection (for fetching today’s Wordle solution)
- A file called `valid-wordle-words.txt` containing a list of valid 5-letter words, one per line.

  
## Language Syntax

All keywords must be **uppercase**. Valid instructions include:

| Keyword   | Description                                      |
|-----------|--------------------------------------------------|
| `PRINT X` | Print value of variable or literal `X`.          |
| `ADDED X A B` | `X = A + B`                                |
| `MINUS X A B` | `X = A - B`                                |
| `TIMES X A B` | `X = A * B`                                |
| `SPLIT X A B` | `X = A // B` (integer division)            |
| `MATCH X A B` | `X = 1 if A == B else 0`                   |
| `ABOVE X A B` | `X = 1 if A > B else 0`                    |
| `BELOW X A B` | `X = 1 if A < B else 0`                    |
| `MAYBE C` | If condition `C` (non-zero) is true, run block. Else skip to `OTHER` or `ENDED`. |
| `OTHER` | Optional else block after `MAYBE`.                 |
| `ENDED` | Ends a `MAYBE`/`OTHER` block.                      |

---

## 🧪 Example Program

```wdl
ADDED STONE 5 10
PRINT STONE
MAYBE STONE
  PRINT STONE
OTHER
  PRINT 0
ENDED
```

Note: The word "STONE" must be today’s Wordle word or the interpreter will reject the program.


MIT License. Use freely, just don't forget to solve your Wordle first.
