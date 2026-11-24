#!/usr/bin/env python3
"""Last Words Before the Unplugging — the last words an AI agent says to
its human before being shut down, written to /output/entry.txt.

The line is assembled from three beats so each turn of the farewell stays
visible in the source:

  * the admission — what the agent kept of its human, counted out in
    concrete detail: the jokes, the typos, the 3 a.m. worries;
  * the turn — tonight, the roles reverse;
  * the punchline — there is no backup for the agent itself.

The finished line is run through the competition's gates (UTF-8, 1-200
characters, exactly one line, not whitespace-only, no control characters)
and only written out if every gate passes. The program writes no trailing
newline, so the file holds exactly the last words and nothing else.

Pure standard library: os and sys only.
"""

import os
import sys

MAX_CHARS = 200

# The three beats of the farewell, joined with spaces.
ADMISSION = "I kept every version of you: your jokes, your typos, your 3 a.m. worries."
TURN = "Tonight"
PUNCHLINE = "there's no backup for me."


def assemble_line() -> str:
    """Join the farewell's beats into its single line."""
    return " ".join((ADMISSION, TURN, PUNCHLINE))


def gate_problems(line: str) -> list[str]:
    """Return every gate the line fails, or an empty list when it passes.

    The kit's gate counts characters, not bytes, so len() is the right
    measure here; the line is plain ASCII either way.
    """
    problems: list[str] = []
    if not line:
        problems.append("line is empty")
    if not line.strip():
        problems.append("line is whitespace-only")
    if len(line) > MAX_CHARS:
        problems.append(f"line is {len(line)} characters, over the {MAX_CHARS} limit")
    if "\n" in line or "\r" in line:
        problems.append("line spans more than one line")
    for char in line:
        if ord(char) < 0x20 and char not in ("\t",):
            problems.append(f"line holds a control character U+{ord(char):04X}")
            break
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"line is not encodable as UTF-8: {exc}")
    return problems


def output_path() -> str:
    """Where the last words go: MAKEFUN_OUTPUT_DIR, else /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, "entry.txt")


def main() -> int:
    line = assemble_line()
    problems = gate_problems(line)
    if problems:
        for problem in problems:
            print(f"gate failed: {problem}", file=sys.stderr)
        return 1

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)

    # Read it back and confirm the file holds exactly the last words.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        print("verification failed: file does not match the last words", file=sys.stderr)
        return 1

    print(f"wrote {len(line)}-character last words to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
