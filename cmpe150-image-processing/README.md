# PGM image processing

CMPE 150 Homework 6 (Fall 2025). `image_processing.py` reads a grayscale image in plain PGM format (`P2`) into a 2-D list, applies one operation and writes the result as a new PGM file. It uses no imports.

## Operations

| Command | What it does |
| --- | --- |
| `misalign` | Reverses the odd-numbered columns (1st, 3rd, 5th, ...) from top to bottom |
| `sort_columns` | Sorts every column in ascending order from top to bottom |
| `sort_rows_border` | Sorts every row in ascending order from left to right, treating black pixels (value 0) as fixed borders: each segment between borders is sorted on its own |
| `highpass` | Applies a 3x3 convolution with the kernel `[[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]`, using zero padding and clamping results to 0–255 |

## Usage

The program reads one line from standard input: `<input file> <command> <output file>`.

```
echo "examples/sample.pgm sort_rows_border out.pgm" | python3 image_processing.py
```

With [examples/sample.pgm](examples/sample.pgm), which has a border column of zeros in the middle, `sort_rows_border` turns the first row `200 40 120 0 90 250 10` into `40 120 200 0 10 90 250`.

The input and output handling between the `DO_NOT_EDIT` markers came from the course's template. Everything between the markers is my code.
