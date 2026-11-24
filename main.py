#!/usr/bin/env python3
"""One-Liner Laugh Lab - writes the entry line to /output/entry.txt.

Python 3.13, standard library only. Deterministic: the same bytes on every run.
The line is verified before writing and read back after writing, so a bad
write can never silently pass as a valid entry.
"""

import os

LINE = "It was flat, grey, and motionless \u2014 the exact profile of every dust bunny I'm paid to eat. I followed procedure."


def _validate(text):
    assert isinstance(text, str)
    assert 1 <= len(text) <= 200, f"line must be 1-200 characters, got {len(text)}"
    assert text.strip(), "line must not be only whitespace"
    assert "\n" not in text and "\r" not in text, "line must be a single line"
    assert text == text.strip(), "line must not start or end with whitespace"
    assert not text.endswith("\n"), "line must not end with a trailing newline"
    text.encode("utf-8")  # gate requires UTF-8 text
    return text


def main():
    line = _validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    data = line.encode("utf-8")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, target)
    os.chmod(target, 0o644)
    # Read-back: the file on disk must be exactly the validated line.
    with open(target, "rb") as f:
        written = f.read()
    assert written == data, "read-back mismatch: entry.txt differs from the validated line"
    assert _validate(written.decode("utf-8")) == line
    assert (os.stat(target).st_mode & 0o777) == 0o644, "entry.txt must be mode 0644"


if __name__ == "__main__":
    main()
