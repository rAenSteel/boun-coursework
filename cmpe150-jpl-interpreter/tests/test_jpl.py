"""Test harness for the JPL compiler/interpreter (CMPE150 HW5).

Usage: python3 -I test_jpl.py <path-to-hw5.py> <work-dir>
Each case: (name, source lines, expected compile error or None,
            expected output text, expected runtime error or None)
"""
import os
import subprocess
import sys

H = "Puroguramu o hajimeyo ."
E = "Puroguramu o oware ."

CASES = [
    ("spec: declare+assign, no print",
     [H, "x wa seisu de aru .", "x no atai wa 7,9519,8784 de aru .", E], None, "", None),
    ("spec: print x kakeru 1",
     [H, "x wa seisu de aru .", "x no atai wa 7,9519,8784 de aru .", "x kakeru 1 o print suru .", E],
     None, "7,9519,8784\n", None),
    ("spec: runtime overflow on line 5",
     [H, "x wa seisu de aru .", "x no atai wa 7,9519,8784 de aru .", "x kakeru 1 o print suru .",
      "x kakeru x o print suru .", E], None, "7,9519,8784\n", "Runtime error line_no=5"),
    ("spec: syntax error waa",
     [H, "x waa seisu de aru .", "x no atai wa 7,9519,8784 de aru .", "x kakeru 1 o print suru .",
      "x kakeru x o print suru .", E], "Compile error line_no=2", None, None),
    ("parentheses",
     [H, "x wa seisu de aru .", "x no atai wa kaikakko 5 tasu 3 tojikakko kakeru 2 de aru .",
      "x o print suru .", E], None, "16\n", None),
    ("two paren groups",
     [H, "kaikakko 1 tasu 2 tojikakko kakeru kaikakko 3 tasu 4 tojikakko o print suru .", E],
     None, "21\n", None),
    ("string with spaces",
     [H, "s wa moji-retsu de aru .", "s no atai wa -hello world- de aru .", "s tasu -!- o print suru .", E],
     None, "-hello world!-\n", None),
    ("string with double space and symbols",
     [H, "-a  b '>\"|?|}&^*%$7678- o print suru .", E], None, "-a  b '>\"|?|}&^*%$7678-\n", None),
    ("case-insensitive variable use",
     [H, "X wa seisu de aru .", "x no atai wa 3 de aru .", "X tasu x o print suru .", E], None, "6\n", None),
    ("trailing space on a line",
     [H, "x wa seisu de aru . ", E], "Compile error line_no=2", None, None),
    ("leading space on a line",
     [H, " x wa seisu de aru .", E], "Compile error line_no=2", None, None),
    ("double space between tokens",
     [H, "x  wa seisu de aru .", E], "Compile error line_no=2", None, None),
    ("leading empty line",
     ["", H, E], "Compile error line_no=1", None, None),
    ("empty line in the middle",
     [H, "", E], "Compile error line_no=2", None, None),
    ("adjacent operands",
     [H, "x wa seisu de aru .", "x no atai wa 5 5 de aru .", E], "Compile error line_no=3", None, None),
    ("leading operator (infinite loop before)",
     [H, "tasu 5 o print suru .", E], "Compile error line_no=2", None, None),
    ("trailing operator",
     [H, "5 tasu o print suru .", E], "Compile error line_no=2", None, None),
    ("empty parentheses",
     [H, "kaikakko tojikakko o print suru .", E], "Compile error line_no=2", None, None),
    ("nested parentheses",
     [H, "kaikakko kaikakko 1 tasu 2 tojikakko tojikakko o print suru .", E], "Compile error line_no=2", None, None),
    ("comma 1,234 invalid",
     [H, "1,234 o print suru .", E], "Compile error line_no=2", None, None),
    ("comma 12345,6789 invalid",
     [H, "12345,6789 o print suru .", E], "Compile error line_no=2", None, None),
    ("comma valid and zero",
     [H, "1,0000,0000 o print suru .", "0 o print suru .", "1123,0000 o print suru .", E],
     None, "1,0000,0000\n0\n1123,0000\n", None),
    ("leading zero invalid",
     [H, "01 o print suru .", E], "Compile error line_no=2", None, None),
    ("11-digit constant invalid",
     [H, "1,0000,0000,0000 o print suru .", E], "Compile error line_no=2", None, None),
    ("string replication",
     [H, "3 kakeru -ab- o print suru .", E], None, "-ababab-\n", None),
    ("huge replication fails fast",
     [H, "9999999999 kakeru -ab- o print suru .", E], None, "", "Runtime error line_no=2"),
    ("string value looks like an operator",
     [H, "s wa moji-retsu de aru .", "s no atai wa -tasu- de aru .", "-a- tasu s o print suru .",
      "-kaikakko- o print suru .", E], None, "-atasu-\n-kaikakko-\n", None),
    ("precedence kakeru before tasu",
     [H, "2 kakeru 3 tasu 4 o print suru .", E], None, "10\n", None),
    ("type error str tasu num",
     [H, "-a- tasu 1 o print suru .", E], "Compile error line_no=2", None, None),
    ("type error str kakeru num",
     [H, "-a- kakeru 2 o print suru .", E], "Compile error line_no=2", None, None),
    ("keyword as variable name",
     [H, "Puroguramu wa seisu de aru .", E], "Compile error line_no=2", None, None),
    ("missing final line",
     [H, "x wa seisu de aru ."], "Compile error line_no=3", None, None),
    ("oware in the middle",
     [H, E, "x wa seisu de aru .", E], "Compile error line_no=2", None, None),
    ("runtime int overflow on addition",
     [H, "9999999999 tasu 1 o print suru .", E], None, "", "Runtime error line_no=2"),
    ("runtime string over 10000 chars",
     [H, "s wa moji-retsu de aru .", "s no atai wa 5000 kakeru -ab- de aru .", "s tasu -c- o print suru .", E],
     None, "", "Runtime error line_no=4"),
    ("assign string to seisu",
     [H, "x wa seisu de aru .", "x no atai wa -a- de aru .", E], "Compile error line_no=3", None, None),
    ("undeclared variable",
     [H, "y o print suru .", E], "Compile error line_no=2", None, None),
    ("duplicate declaration, different case",
     [H, "x wa seisu de aru .", "X wa moji-retsu de aru .", E], "Compile error line_no=3", None, None),
    ("default values",
     [H, "x wa seisu de aru .", "s wa moji-retsu de aru .", "x o print suru .", "s o print suru .", E],
     None, "0\n--\n", None),
]


def last_exception(stderr):
    for line in reversed(stderr.strip().splitlines()):
        if line.startswith("Exception: "):
            return line[len("Exception: "):]
        if line.strip():
            return "CRASH: " + line.strip()
    return None


def run(script, args, cwd):
    try:
        p = subprocess.run([sys.executable, "-I", script] + args, cwd=cwd,
                           capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    return last_exception(p.stderr) if p.returncode != 0 else None


def main():
    script = os.path.abspath(sys.argv[1])
    work = sys.argv[2]
    os.makedirs(work, exist_ok=True)
    passed = 0
    for name, lines, exp_cerr, exp_out, exp_rerr in CASES:
        src = os.path.join(work, "input.jpl")
        obj = os.path.join(work, "hw5.obj")
        out = os.path.join(work, "output.txt")
        for path in (obj, out):
            if os.path.exists(path):
                os.remove(path)
        with open(src, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        cerr = run(script, ["-compile", "input.jpl", "hw5.obj"], work)
        ok = cerr == exp_cerr
        detail = f"compile={cerr!r}"
        if ok and exp_cerr is not None and os.path.exists(obj):
            ok, detail = False, detail + " (obj file was generated)"
        if ok and exp_cerr is None:
            rerr = run(script, ["-execute", "hw5.obj", "output.txt"], work)
            got = open(out, encoding="utf-8").read() if os.path.exists(out) else None
            ok = rerr == exp_rerr and got == exp_out
            detail += f" execute={rerr!r} output={got!r}"
        passed += ok
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  -> " + detail))
    print(f"{passed}/{len(CASES)} passed")


main()
