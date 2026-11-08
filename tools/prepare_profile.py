#!/usr/bin/env python3
"""Copy installed Archiso releng into a generated profile and apply Alpha 0.1 changes."""
from __future__ import annotations
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
BASE = Path(os.getenv("SINISTER_ARCHISO_RELENG", "/usr/share/archiso/configs/releng"))
TARGET = ROOT / "build" / "profile"
OVERLAY = ROOT / "profile-overlay" / "airootfs"

class ProfileError(RuntimeError):
    pass

def replace_shell_assignment(source: str, name: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(name)}=[^\n]*$")
    result, n = pattern.subn(lambda _: f'{name}="{value}"', source)
    if n != 1:
        raise ProfileError(f"Expected one {name} assignment in installed profile (found {n})")
    return result

def add_executable_permission(source: str, executable: str) -> str:
    token = f'["{executable}"]="0:0:755"'
    if token in source:
        return source
    pattern = re.compile(r"(?m)^file_permissions=\(\s*$")
    result, n = pattern.subn(lambda m: m.group(0) + "\n" + token, source)
    if n != 1:
        raise ProfileError("Expected file_permissions array in releng profiledef.sh")
    return result

def merge_overlay(src_root: Path, dst_root: Path) -> None:
    for src in src_root.rglob("*"):
        rel = src.relative_to(src_root)
        dst = dst_root / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.is_symlink():
                dst.unlink()
            shutil.copy2(src, dst)
        else:
            raise ProfileError(f"Unexpected overlay type: {src}")

def prepare(base: Path = BASE, target: Path = TARGET) -> Path:
    if not (base / "profiledef.sh").is_file() or not (base / "packages.x86_64").is_file():
        raise ProfileError(f"Archiso releng profile is missing at {base}; install archiso on Arch")
    build = target.parent
    if target.name != "profile" or build.name != "build":
        raise ProfileError("Unexpected generated profile target")
    build.mkdir(exist_ok=True)
    if target.is_symlink():
        raise ProfileError(f"Refusing symlink at {target}")
    if target.exists():
        if not target.is_dir() or target.resolve() != (build / "profile").resolve():
            raise ProfileError("Unexpected generated profile location")
        shutil.rmtree(target)
    shutil.copytree(base, target, symlinks=True)
    cfg = target / "profiledef.sh"
    source = cfg.read_text()
    for key, value in (
        ("iso_name", "sinisternux"),
        ("iso_label", "SINISTER_01"),
        ("iso_publisher", "SinisterNux Project"),
        ("iso_application", "SinisterNux Alpha 0.1 Live Environment"),
        ("iso_version", "0.1.0_alpha_$(date +%Y%m%d)"),
    ):
        source = replace_shell_assignment(source, key, value)
    source = add_executable_permission(source, "/usr/local/bin/sinister-info")
    cfg.write_text(source)
    merge_overlay(OVERLAY, target / "airootfs")
    extra_path = ROOT / "config" / "extra-packages.txt"
    extra = [line.strip() for line in extra_path.read_text().splitlines()
             if line.strip() and not line.strip().startswith("#")]
    packages = target / "packages.x86_64"
    original = packages.read_text()
    installed = {line.strip() for line in original.splitlines() if line.strip() and not line.strip().startswith("#")}
    additions = [name for name in extra if name not in installed]
    if additions:
        packages.write_text(original.rstrip() + "\n\n# SinisterNux additions\n" + "\n".join(additions) + "\n")
    for dirname, glob in (("efiboot", "*.conf"), ("syslinux", "*.cfg"), ("grub", "*.cfg")):
        folder = target / dirname
        if folder.exists():
            for f in folder.rglob(glob):
                if f.is_file():
                    old = f.read_text()
                    new = old.replace("Arch Linux install medium", "SinisterNux Alpha 0.1 Live")
                    if new != old:
                        f.write_text(new)
    return target

if __name__ == "__main__":
    try:
        result = prepare()
        print(f"Staged SinisterNux Alpha 0.1 profile: {result}")
    except (ProfileError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
