#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from typing import List

HEX_ESCAPE_RE = re.compile(r'\\x[0-9a-fA-F]{2}')

def memory_length(literal: str) -> int:
    """
    Return the length of the string as it would be stored in memory,
    given the raw literal (including the surrounding quotes).
    """
    # Remove the surrounding quotes
    inner = literal[1:-1]

    i = 0
    mem_len = 0
    while i < len(inner):
        ch = inner[i]
        if ch != '\\':
            # ordinary character
            mem_len += 1
            i += 1
        else:
            # start of an escape sequence
            nxt = inner[i + 1] if i + 1 < len(inner) else ''
            if nxt in ('\\', '"'):
                # \\ or \"
                mem_len += 1
                i += 2
            elif nxt == 'x' and i + 3 < len(inner) and re.match(r'[0-9a-fA-F]{2}', inner[i+2:i+4]):
                # \xhh
                mem_len += 1
                i += 4
            else:
                # Should not happen with valid input, but treat as a literal backslash
                mem_len += 1
                i += 1
    return mem_len


def part1(lines: List[str]) -> int:
    """Sum of (literal length - memory length) for all lines."""
    total = 0
    for line in lines:
        lit_len = len(line)
        mem_len = memory_length(line)
        total += lit_len - mem_len
    return total


def part2(lines: List[str]) -> int:
    """Sum of (encoded length - original literal length) for all lines."""
    total = 0
    for line in lines:
        # Count how many extra characters we need when encoding
        extra = line.count('\\') + line.count('"') + 2
        total += extra
    return total


if __name__ == "__main__":
    INPUT_PATH = Path(sys.argv[1])
    raw_lines = INPUT_PATH.read_text().splitlines()

    print("Part 1 answer :", part1(raw_lines))
    print("Part 2 answer :", part2(raw_lines))
