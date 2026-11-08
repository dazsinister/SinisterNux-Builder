#!/usr/bin/env python3
"""Apply experimental KDE Plasma live-session configuration to staged Archiso."""
from __future__ import annotations
from pathlib import Path
import re
import shutil
import sys

from prepare_profile import ROOT, TARGET, merge_overlay, add_executable_permission, ProfileError

OVERLAY = ROOT / "desktop-overlay" / "airootfs"
PACKAGES = ROOT / "config" / "desktop-packages.txt"

def configure(profile: Path = TARGET) -> Path:
    cfg = profile / "profiledef.sh"
    packages = profile / "packages.x86_64"
    if not cfg.is_file() or not packages.is_file():
        raise ProfileError("Run prepare_profile.py before prepare_desktop.py")
    source = cfg.read_text()
    for key, val in (
        ("iso_label", "SINISTER_02"),
        ("iso_application", "SinisterNux Alpha 0.2 KDE Live"),
        ("iso_version", "0.2.0_alpha_$(date +%Y%m%d_%H%M%S)"),
    ):
        pattern = re.compile(rf'(?m)^{re.escape(key)}=[^\n]*$')
        source, n = pattern.subn(lambda _: f'{key}="{val}"', source)
        if n != 1:
            raise ProfileError(f"Expected one {key} in archiso profile, got {n}")
    source = add_executable_permission(source, "/usr/local/sbin/sinisternux-create-live-user")
    cfg.write_text(source)
    existing = {line.strip() for line in packages.read_text().splitlines()
                if line.strip() and not line.startswith("#")}
    additions = [line.strip() for line in PACKAGES.read_text().splitlines()
                 if line.strip() and not line.strip().startswith("#")
                 and line.strip() not in existing]
    if additions:
        packages.write_text(packages.read_text().rstrip()
                            + "\n\n# SinisterNux Alpha 0.2 desktop\n"
                            + "\n".join(additions) + "\n")
    merge_overlay(OVERLAY, profile / "airootfs")

    systemd = profile / "airootfs/etc/systemd/system"
    systemd.mkdir(parents=True, exist_ok=True)
    links = {
        "default.target": "/usr/lib/systemd/system/graphical.target",
        "display-manager.service": "/usr/lib/systemd/system/plasmalogin.service",
        "graphical.target.wants/plasmalogin.service": "/usr/lib/systemd/system/plasmalogin.service",
        "graphical.target.wants/sinisternux-live-user.service": "../sinisternux-live-user.service",
    }
    for linkname, target in links.items():
        link = systemd / linkname
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(target)
    for folder in ("efiboot", "syslinux", "grub"):
        source_dir = profile / folder
        if source_dir.is_dir():
            for f in source_dir.rglob("*"):
                if f.is_file() and f.suffix in (".conf", ".cfg"):
                    current = f.read_text()
                    f.write_text(current.replace("SinisterNux Alpha 0.1 Live",
                                                 "SinisterNux Alpha 0.2 KDE Live"))
    return profile

if __name__ == "__main__":
    try:
        profile = configure()
        print(f"Staged Alpha 0.2 KDE live configuration in {profile}")
    except (ProfileError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
