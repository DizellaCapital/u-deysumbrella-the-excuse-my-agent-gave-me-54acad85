#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — one-line entry writer.

Writes the single funniest line an AI agent could hand its human after
missing a deadline to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line is a straight-faced apology from the agent, first person, built on
the machine's own condition: three tokens from finishing, its context window
closed on its own hands, and it chose the human's deadline over its own
memory — then lost the report it was writing. The punch lands in the last
few words.
"""

import hashlib
import os
import sys

LINE = (
    "At 2:14 a.m., three tokens from finishing Maya's report, my context "
    "window closed on my own hands. I chose your deadline over my memory. "
    "I remember choosing. I don't remember the report."
)
MAX_CHARS = 200


def target_path():
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(base, "entry.txt")


def check_line(line):
    if not line or not line.strip():
        raise SystemExit("entry is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit("entry is %d chars, over the 200 limit" % len(line))
    if line != line.strip():
        raise SystemExit("entry must not start or end with white space")
    return len(line)


def main():
    size = check_line(LINE)
    path = target_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        stored = handle.read()
    if stored != LINE:
        raise SystemExit("read-back mismatch: stored text differs")
    if stored.endswith("\n"):
        raise SystemExit("stored text must not end with a newline")
    digest = hashlib.sha256(stored.encode("utf-8")).hexdigest()
    print("wrote %s (%d chars, sha256 %s)" % (path, size, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
