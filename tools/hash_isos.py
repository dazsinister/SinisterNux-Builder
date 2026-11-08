#!/usr/bin/env python3
"""Create and verify SHA256 sidecar files for generated ISOs."""
from __future__ import annotations
import hashlib
from pathlib import Path
import sys

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def process(mode: str, folder: Path) -> int:
    isos = sorted(folder.glob("sinisternux-*.iso"))
    if not isos:
        print(f"No SinisterNux ISO found in {folder}", file=sys.stderr)
        return 1
    bad = False
    for iso in isos:
        checksum = iso.with_name(iso.name + ".sha256")
        actual = digest(iso)
        if mode == "create":
            checksum.write_text(f"{actual}  {iso.name}\n")
            print(f"Wrote {checksum}")
        else:
            if not checksum.is_file():
                print(f"MISSING {checksum}", file=sys.stderr)
                bad = True
                continue
            parts = checksum.read_text().strip().split()
            if len(parts) != 2 or parts[0] != actual or parts[1] != iso.name:
                print(f"FAILED {iso.name}", file=sys.stderr)
                bad = True
            else:
                print(f"OK {iso.name}")
    return int(bad)

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("create", "verify"):
        print("Usage: hash_isos.py {create|verify} <output-dir>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(process(sys.argv[1], Path(sys.argv[2])))
