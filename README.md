# SinisterNux Alpha 0.1 — First Boot

This repository contains the **source-code starter** for SinisterNux Alpha 0.1, an Arch-based Linux distribution project. It is **not yet a bootable ISO** and is not ready for installation on real hardware.

## Alpha 0.1 goal

Create a branded, Archiso-based **UEFI live ISO** that boots to a terminal, has networking, and reports `SinisterNux Alpha 0.1` through `sinister-info`. KDE Plasma, the installer, Linux Zen/LTS, Limine, dracut, snapshots, and custom applications are later milestones. This first alpha deliberately keeps the upstream Archiso live boot infrastructure.

## Prerequisites

Inside a clean Arch Linux x86_64 build VM (recommended: 4 vCPUs, 8 GiB RAM, 80 GiB disk):

```bash
sudo pacman -Syu
sudo pacman -S --needed archiso git make python sudo
```

## Build

```bash
make doctor       # Check build prerequisites
make check        # Run offline source tests
make prepare      # Stage a branded copy of Archiso releng
make iso          # Build ISO; needs sudo and package downloads
make verify       # Check SHA-256 output
```

Expected output: `build/out/sinisternux-*.iso` with a SHA-256 checksum. **The ISO has not yet been built or verified in an Arch VM.**

## Testing

Use a separate disposable QEMU/KVM VM with UEFI/OVMF. After live boot, run:

```bash
sinister-info
cat /etc/os-release
uname -a
ip a
ping -c 3 archlinux.org
```

Never run installer or partitioning tools from this early live image on a valuable physical disk.

## Documentation

- `docs/ARCHITECTURE.md`: 39 long-term architectural decisions, not implemented features.
- `docs/MILESTONES.md`: incremental alpha goals and acceptance checks.
- `docs/BUILD-VM.md`: clean Arch build VM and testing instructions.

Local Git is our development workflow; GitHub is a remote copy and collaboration point, **not** cloud-based ISO compilation. Do not commit build output, signing keys, secrets, or VM disk files.

Archiso references: [ArchWiki](https://wiki.archlinux.org/title/Archiso) · [mkarchiso manual](https://man.archlinux.org/man/mkarchiso.1.en).
