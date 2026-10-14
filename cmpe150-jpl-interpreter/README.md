# JPL compiler and interpreter

JPL (Japanese Programming Language) is a small language with Japanese keywords, defined in CMPE 150 Homework 5 (Fall 2025). `hw5.py` compiles a `.jpl` source file into an object file (a pickled list of instructions) and then executes that object file.

## The language

| JPL | Meaning |
| --- | --- |
| `Puroguramu o hajimeyo .` / `Puroguramu o oware .` | First and last line of every program |
| `x wa seisu de aru .` | Declare `x` as an integer (`seisu`) |
| `s wa moji-retsu de aru .` | Declare `s` as a string (`moji-retsu`) |
| `x no atai wa <expr> de aru .` | Assign the value of an expression to `x` |
| `<expr> o print suru .` | Print the value of an expression |
| `tasu` | Addition, or string concatenation |
| `kakeru` | Multiplication, or string repetition (`3 kakeru -ab-`) |
| `kaikakko` ... `tojikakko` | Parentheses (one level, no nesting) |

- Integers have at most 10 digits. Commas group digits in fours, following the Japanese 万/億 grouping: `7,9519,8784`.
- Strings are written between hyphens (`-hello world-`) and hold up to 10,000 characters.
- Parentheses come first, then `kakeru`, then `tasu`. Operators of the same level are evaluated right to left.
- Variable names are case-insensitive, use only English letters and are at most 10 letters long. Keywords are case-sensitive.
- Every token is separated by exactly one space, including the final ` .`.

## Usage

```
python3 hw5.py -compile examples/hello.jpl hello.obj
python3 hw5.py -execute hello.obj output.txt
```

For [examples/hello.jpl](examples/hello.jpl), `output.txt` contains:

```
3,7035
-konnichiwa, sekai-
-haha-
```

Errors are raised as `Exception("Compile error line_no=N")` or `Exception("Runtime error line_no=N")`, always for the earliest failing line. If compilation fails, no object file is written. If execution fails, everything printed before the error stays in the output file.

## How it works

1. **Compile.** Each line is split into tokens, with a string constant kept as one token even if it contains spaces. The compiler checks the statement form, declarations, variable names, constant ranges, comma grouping, parentheses and operand types, then pickles the instruction list.
2. **Execute.** Expressions are evaluated in the order above. Every intermediate result is checked against the 10-digit and 10,000-character limits.

## Tests

`tests/test_jpl.py` runs 39 cases: the examples from the assignment plus edge cases for spacing, comma grouping, parentheses, types and runtime limits.

```
python3 tests/test_jpl.py hw5.py /tmp/jpl-tests
```

## Fixes after grading

The first commit in this repository is the version I submitted. After the course I fixed the bugs below, with help from an AI assistant. The commit history shows each change.

- The closing line `Puroguramu o oware .` was parsed as a statement, so every valid program failed to compile.
- Expressions with parentheses crashed with a `KeyError` during type checking.
- String constants containing spaces were split into several tokens.
- Variable names were case-insensitive in declarations but not inside expressions.
- Spaces at the start or end of a line were silently removed instead of being reported.
- Malformed expressions were accepted, crashed or looped forever. Examples: two operands in a row, an operator at either end, empty parentheses.
- Integer constants such as `12345,6789`, whose first group is longer than four digits, were accepted.
- `puroguramu` was accepted as a variable name.
- At runtime, a string value such as `-tasu-` could be mistaken for an operator, and a very large string repetition was built before its length was checked.
