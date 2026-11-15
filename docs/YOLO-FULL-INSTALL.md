# SinisterNux "Throw Everything At It" — experimental build

**This is a deliberately unstable, VM-ONLY preview.** It is **not** a fully implemented custom installer and not intended for a real physical disk.

## What it really does

1. Starts with the existing Archiso releng + our Alpha 0.2 KDE live image setup.
2. Adds a large, opinionated official-repository package list: Plasma, software, gaming, kernels, dracut, Limine, Btrfs, Snapper, AppArmor, firewalld, Restic, zram, hardware tools, development/virtualization apps.
3. Enables the official **multilib** repository in the ISO build profile so Steam and lib32 libraries can be included.
4. Includes a clearly labeled **Archinstall-based** guided installation launcher on the live image, rather than pretending Calamares integration works.
5. Includes `scripts/yolo-postinstall.sh` for first-boot use inside the **newly installed, disposable Arch VM** to install/configure software and non-boot-critical services.
6. Preserves main (Alpha 0.1) and alpha-0.2-kde untouched by doing all development on `experiment/yolo-full-install`.

## NOT yet completed
- Calamares graphical installer (upstream project uses separately packaged builds; it is not automatically provided by this ISO)
- Fully verified Limine + dracut + Zen/LTS installed boot setup, including ESP/snapshot consistency
- Automated Btrfs partitioning and subvolume layout
- Real KDE Sinister Command top-panel/dock + finished graphics
- A signed SinisterNux pacman repository and Testing/Stable channels
- Native Qt/QML Update, Welcome, Backup and package-management applications
- Hardware-specific NVIDIA configuration, fingerprint setup, FIDO2, actual backup destinations, full accessibility auditing, or validated rescue workflows

The **packages** for many of those features are available in the preview, but packaging software is not the same as engineering and validating integration.

## Build (inside Unraid Arch builder VM)

```bash
cd ~/SinisterNux-Builder
git fetch origin
git switch --track origin/experiment/yolo-full-install
make check
make yolo-prepare
make yolo-iso
make yolo-verify
ls -lh build/yolo-out/
```

If you've already switched to the branch, use `git pull --ff-only` instead of `git switch --track`.

Expect a **multi-gigabyte** ISO, a lengthy build, significant network downloads, and potential package conflicts or missing package names. This branch has NOT been built on an Arch/Unraid VM yet. Report the **first exact pacman error** if it fails.

## Attempt installation — ONLY on an expendable test VM

1. Keep the Alpha 0.1 ISO safely saved; make a **new** Unraid test VM for YOLO, with OVMF, VNC graphics, 8+ GiB RAM, and **a new EMPTY 100+ GiB virtual disk**.
2. Boot the YOLO ISO. From its live console, run `sudo sinisternux-install-preview` if your live session permits sudo; otherwise use the root TTY.
3. The launcher checks virtualization and starts upstream `archinstall` **only after explicit confirmation**.
4. In archinstall choose the **new VM virtual disk** (this WILL erase it), UEFI boot, Btrfs, a user with sudo, Plasma desktop, NetworkManager, and additional packages as needed. Use **the bootloader that archinstall can install successfully**; do not forcibly switch a working EFI bootloader yet.
5. Reboot into the new installation, verify system and networking, clone this repository, then inspect `scripts/yolo-postinstall.sh`. Execute it as root **only inside that expendable VM** to install the broad package list and enable selected services. A repo clone into the installed machine is needed; this installer does not claim to automatically install a custom system image.
6. Verify KDE, Konsole, Dolphin, browsers, gaming tools, and diagnostics individually. Take an Unraid VM snapshot/backup before changing boot components.

## Limine, dracut, Btrfs, Calamares

We intentionally **do not overwrite an existing working EFI bootloader** in this experiment. Having the Limine/dracut packages installed does not mean the installed VM boots through them. A subsequent dedicated installation integration is required. Likewise, `snapper` package presence is not proof that rollback is configured or tested.

## Security warnings

Do not run the experimental postinstall script on the CachyOS gaming host, the Unraid host, or a non-disposable system. This is *not* an unattended destructive installer. Read its package list and inspect its effects first; there is no blanket `pacman --noconfirm` or automatic disk partitioning. Your Unraid data volumes must **never** be passed through to this test VM.
