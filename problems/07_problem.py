import re
from pathlib import Path
from typing import Dict, Tuple, Union

# ----------------------------------------------------------------------
# Parsing helpers
# ----------------------------------------------------------------------
Instruction = Tuple[str, Tuple[Union[int, str], ...]]  # (op, args)

def parse_line(line: str) -> Tuple[str, Instruction]:
    """
    Turn a raw instruction line into (target_wire, (op, args)).
    """
    target = line.split(" -> ")[1].strip()
    expr = line.split(" -> ")[0].strip()

    # Patterns for the various forms
    if m := re.fullmatch(r"(\w+) AND (\w+)", expr):
        op, a, b = "AND", m.group(1), m.group(2)
    elif m := re.fullmatch(r"(\w+) OR (\w+)", expr):
        op, a, b = "OR", m.group(1), m.group(2)
    elif m := re.fullmatch(r"(\w+) LSHIFT (\d+)", expr):
        op, a, b = "LSHIFT", m.group(1), int(m.group(2))
    elif m := re.fullmatch(r"(\w+) RSHIFT (\d+)", expr):
        op, a, b = "RSHIFT", m.group(1), int(m.group(2))
    elif m := re.fullmatch(r"NOT (\w+)", expr):
        op, a = "NOT", m.group(1)
        b = None
    elif m := re.fullmatch(r"(\d+)", expr):
        # literal assignment
        op, a = "SET", int(m.group(1))
        b = None
    else:
        # simple wire copy
        op, a = "SET", expr
        b = None

    args = (a,) if b is None else (a, b)
    return target, (op, args)


# ----------------------------------------------------------------------
# Core evaluator
# ----------------------------------------------------------------------
MASK = 0xFFFF  # keep only lower 16 bits

class Circuit:
    def __init__(self, lines):
        self.rules: Dict[str, Instruction] = {}
        for line in lines:
            if line.strip():
                target, instr = parse_line(line.strip())
                self.rules[target] = instr
        self.cache: Dict[str, int] = {}

    def _value(self, token: Union[int, str]) -> int:
        """Resolve a token – either a literal int or a wire name."""
        if isinstance(token, int):
            return token
        # token is a wire name
        return self.evaluate(token)

    def evaluate(self, wire: str) -> int:
        """Recursively compute the signal on *wire*."""
        if wire.isdigit():                     # direct numeric literal
            return int(wire) & MASK

        if wire in self.cache:
            return self.cache[wire]

        op, args = self.rules[wire]

        if op == "SET":
            result = self._value(args[0])
        elif op == "AND":
            result = self._value(args[0]) & self._value(args[1])
        elif op == "OR":
            result = self._value(args[0]) | self._value(args[1])
        elif op == "LSHIFT":
            result = (self._value(args[0]) << args[1]) & MASK
        elif op == "RSHIFT":
            result = (self._value(args[0]) >> args[1]) & MASK
        elif op == "NOT":
            result = (~self._value(args[0])) & MASK
        else:
            raise ValueError(f"Unknown op {op}")

        self.cache[wire] = result & MASK
        return self.cache[wire]
    
    # ------------------------------------------------------------------
    # Helper to reset the circuit (clear memoisation & optionally replace a rule)
    # ------------------------------------------------------------------
    def reset(self, overrides: Dict[str, Instruction] | None = None):
        """Clear cached values and optionally replace some rules."""
        self.cache.clear()
        if overrides:
            for w, instr in overrides.items():
                self.rules[w] = instr

# ----------------------------------------------------------------------
# Run it
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Read file
    INPUT_PATH = Path("07_input.txt")
    lines = INPUT_PATH.read_text().splitlines()

    # ---------- Part 1 ----------
    circuit = Circuit(lines)
    part1_a = circuit.evaluate("a")
    print("Part 1 – signal on wire a =", part1_a)

    # ---------- Part 2 ----------
    # Reset the circuit, override wire 'b' with the value from part 1.
    circuit.reset(overrides={"b": ("SET", (part1_a,))})
    part2_a = circuit.evaluate("a")
    print("Part 2 – new signal on wire a =", part2_a)

