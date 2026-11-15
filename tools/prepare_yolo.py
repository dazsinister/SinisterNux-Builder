#!/usr/bin/env python3
"""Create an experimental all-in live ISO profile from the Alpha 0.2 KDE profile."""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from prepare_profile import ROOT, ProfileError, merge_overlay, add_executable_permission

SOURCE = ROOT / "build" / "profile"
TARGET = ROOT / "build" / "yolo-profile"
PACKAGES = ROOT / "config" / "yolo-packages.txt"
OVERLAY = ROOT / "yolo-overlay" / "airootfs"

def enable_multilib(config: str) -> str:
    if re.search(r"(?m)^\[multilib\]\s*$", config):
        return config
    pattern = re.compile(
        r"(?m)^#\[multilib\]\s*\n#Include\s*=\s*/etc/pacman\.d/mirrorlist\s*$"
    )
    result, n = pattern.subn(
        "[multilib]\nInclude = /etc/pacman.d/mirrorlist", config
    )
    if n != 1:
        raise ProfileError("Cannot enable [multilib] in Archiso pacman.conf")
    return result

def prepare(source: Path = SOURCE, target: Path = TARGET) -> Path:
    if not (source / "profiledef.sh").is_file():
        raise ProfileError("Run 'make prepare' before YOLO profile staging")
    if target.is_symlink():
        raise ProfileError("Refusing symlink at generated YOLO profile")
    if target.exists():
        if not target.is_dir():
            raise ProfileError("Expected a directory for YOLO profile")
        shutil.rmtree(target)
    shutil.copytree(source, target, symlinks=True)
    cfg = target / "profiledef.sh"
    definition = cfg.read_text()
    for key, value in (
        ("iso_name", "sinisternux-yolo"),
        ("iso_label", "SINISTER_YOLO"),
        ("iso_application", "SinisterNux YOLO All-in Preview"),
        ("iso_version", "0.9.0_yolo_$(date +%Y%m%d_%H%M%S)"),
    ):
        definition, count = re.subn(
            rf"(?m)^{re.escape(key)}=[^\n]*$",
            lambda _: f'{key}="{value}"',
            definition,
        )
        if count != 1:
            raise ProfileError(f"Expected one assignment for {key}, saw {count}")
    definition = add_executable_permission(definition, "/usr/local/bin/sinisternux-install-preview")
    # sudo requires secure root-owned 0440 permissions on sudoers files.
    sudoers_path = "/etc/sudoers.d/99-sinisternux-yolo-installer"
    sudoers_token = f'["{sudoers_path}"]="0:0:440"'
    if sudoers_token not in definition:
        definition, count = re.subn(
            r"(?m)^file_permissions=\(\s*$",
            lambda m: m.group(0) + "\n" + sudoers_token,
            definition,
        )
        if count != 1:
            raise ProfileError("Cannot apply sudoers file permissions")

    cfg.write_text(definition)
    pacman_conf = target / "pacman.conf"
    if not pacman_conf.is_file():
        raise ProfileError("Archiso releng pacman.conf not found")
    pacman_conf.write_text(enable_multilib(pacman_conf.read_text()))
    existing_path = target / "packages.x86_64"
    existing = existing_path.read_text()
    already = {s.strip() for s in existing.splitlines() if s.strip() and not s.startswith("#")}
    packages = []
    for line in PACKAGES.read_text().splitlines():
        name = line.strip()
        if not name or name.startswith("#"):
            continue
        if not re.fullmatch(r"[a-z0-9@._+-]+", name):
            raise ProfileError(f"Invalid package name: {name}")
        if name not in already and name not in packages:
            packages.append(name)
    if packages:
        existing_path.write_text(
            existing.rstrip() + "\n\n# SinisterNux YOLO all-in packages\n"
            + "\n".join(packages) + "\n"
        )
    merge_overlay(OVERLAY, target / "airootfs")
    return target

if __name__ == "__main__":
    try:
        result = prepare()
        print(f"YOLO staging ready: {result}")
        print("WARNING: packages and live GUI are UNTESTED; build only on an Arch VM.")
    except (OSError, ProfileError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
