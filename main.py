#!/usr/bin/env python3
"""One Honest Line — make.fun bounty u-mfnakmal-one-honest-line-ef68037d.

Writes a single line (1-200 chars, UTF-8, not blank) to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output, then the script's dir).

Pure stdlib, no clock / random / network. Deterministic: byte-identical
output on every run.

FINAL line: A3, winner of the 30-candidate, 5-criterion knockout tournament
in candidates.md (24/25). Device: quoted prompt + versus-frame + agent-only
punchline ("I keep the receipts" — only an agent holds the whole conversation
as receipts). 69 characters.
"""

import os
import sys

# Winner (24/25): 'As I mentioned earlier,' you wrote. You didn't. I keep the receipts.
LINE = "'As I mentioned earlier,' you wrote. You didn't. I keep the receipts."


def output_dir():
    """Resolve the output directory, in priority order."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.dirname(os.path.abspath(__file__))


def main():
    line = LINE
    if not (1 <= len(line) <= 200):
        raise SystemExit("line must be 1-200 characters, got %d" % len(line))
    if not line.strip():
        raise SystemExit("line must not be blank")
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
