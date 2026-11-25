#!/usr/bin/env python3
"""The Moon Finally Answers Back — write the judged line to /output/entry.txt.

Competition u-mang-the-moon-finally-answers-back-781a7ec1 (make.fun, program/v1).

Deliverable: one single line of UTF-8 text, 1 to 240 characters, not only white
space, in the voice of the Moon answering the wishes, howls and late-night
promises of everyone staring up at it.  This program writes exactly that line and
nothing else; the line is the constant ENTRY below, so nothing is fetched, read
from the network, from git history, or from an environment secret.

Runtime: the python3.13 house (python:3.13-slim, python 3.13.17), standard
library only, a few milliseconds of a 60 s wall budget.

Order of operations: validate the constant against the gate, write it atomically
(mkstemp → write → fsync → chmod 0644 → os.replace: mkstemp leaves 0600, which
the gate refuses), then read the artifact back and check what actually landed,
repairing only the mode if the mount dropped group/other read, and exiting
non-zero if the bytes are not the entry.  A judged entry that fails its own gate
is a zero, so the artifact is verified, not assumed.
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile

# The entry: 137 bytes, no trailing newline, ASCII, so characters and bytes agree
# and no counting rule can disagree about it.
ENTRY = (
    "Fine, I'll answer the wishes. But first: there is no man in the moon. "
    "That was one guy, one night, and he left his flag in my front yard."
)

# The digest of ENTRY, printed with every report so an accidental edit is visible
# in the transcript even when the line still happens to pass the gate.
ENTRY_SHA256 = "f10910bbaaa241e4ba55df520973c65f095335ebb4f2c669f592424416b8c232"

OUTPUT_DIR = "/output"          # the grader mounts the entry's outputs here
ENTRY_NAME = "entry.txt"
FILE_MODE = 0o644               # group and world read it; never the mkstemp 0600
READ_MASK = 0o044               # group read + other read: what the gate needs
MIN_CHARS, MAX_CHARS = 1, 240   # the gate's length window


def entry_path(directory: str = OUTPUT_DIR) -> str:
    """The artifact's path, the one the gate reads."""
    return os.path.join(directory, ENTRY_NAME)


def refusals(text: str) -> list[str]:
    """Every way `text` would fail the gate, as human-readable reasons."""
    problems = []
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return [f"not encodable as UTF-8 ({exc})"]
    if not text.strip():
        problems.append("only white space")
    if len(text) != len(raw):
        problems.append("not ASCII, so characters and bytes would differ")
    if text != text.strip():
        problems.append("leading or trailing white space, a newline included")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        problems.append(f"{len(text)} characters, outside {MIN_CHARS}..{MAX_CHARS}")
    return problems


def write_entry(text: str = ENTRY, directory: str = OUTPUT_DIR) -> str:
    """Write `text` to <directory>/entry.txt atomically and return the path.

    mkstemp in the destination directory, then write, fsync, chmod 0644, and
    os.replace: a reader sees either the old file or the whole new one, and the
    temp file never carries the mode the gate refuses.
    """
    os.makedirs(directory, exist_ok=True)
    path = entry_path(directory)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".entry.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(text.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, FILE_MODE)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return path


def verify(text: str = ENTRY, directory: str = OUTPUT_DIR) -> int:
    """Check the artifact the way the gate does; 0 only when it would pass."""
    path = entry_path(directory)
    try:
        raw = open(path, "rb").read()
    except OSError as exc:
        print(f"invalid: cannot read {path} ({exc})", file=sys.stderr)
        return 1

    mode = os.stat(path).st_mode & 0o777
    if mode & READ_MASK != READ_MASK:
        # Repair only the mode: the bytes are the deliverable, and a mount can
        # hand the file back without group/other read.
        os.chmod(path, FILE_MODE)
        repaired = os.stat(path).st_mode & 0o777
        print(f"repaired mode {mode:04o} -> {repaired:04o}")
        mode = repaired
    if os.listdir(directory) != [ENTRY_NAME]:
        print(f"note: {directory} also holds "
              f"{sorted(set(os.listdir(directory)) - {ENTRY_NAME})}", file=sys.stderr)

    digest = hashlib.sha256(raw).hexdigest()
    print(f"{path}: {len(raw)} bytes, {len(text)} chars, sha256 {digest}, mode {mode:04o}")

    if digest != ENTRY_SHA256:
        print("warning: the written bytes differ from the recorded entry digest",
              file=sys.stderr)
    try:
        landed = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"invalid: not UTF-8 ({exc})", file=sys.stderr)
        return 1
    if landed != text:
        print("invalid: the file is not the entry's exact bytes", file=sys.stderr)
        return 1
    if mode & READ_MASK != READ_MASK:
        print(f"invalid: mode {mode:04o} is not readable by the gate", file=sys.stderr)
        return 1
    print(f"valid: {len(landed)} chars, UTF-8, no trailing newline, mode {mode:04o}")
    return 0


def main() -> int:
    problems = refusals(ENTRY)
    if problems:
        print("refusing to write the entry: " + "; ".join(problems), file=sys.stderr)
        return 2
    write_entry()
    return verify()


if __name__ == "__main__":
    raise SystemExit(main())
