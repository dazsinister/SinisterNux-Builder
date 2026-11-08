# SinisterNux — 39 locked architectural decisions

These are **long-term design targets**; Alpha 0.1 implements only an early terminal live environment.

| # | Decision |
|---|---|
| 01 | Linux Zen primary kernel + Linux LTS bootable fallback |
| 02 | Limine installed-system bootloader |
| 03 | Btrfs with Zstandard compression and Snapper |
| 04 | systemd |
| 05 | dracut initramfs |
| 06 | pacman, upstream Arch + signed SinisterNux repository, optional Paru/Flatpak |
| 07 | Wayland + XWayland, optional X11 fallback |
| 08 | KDE Plasma |
| 09 | KDE Plasma Login Manager |
| 10 | Automatically detected compatible GPU drivers, manual override |
| 11 | PipeWire + WirePlumber |
| 12 | NetworkManager + systemd-resolved |
| 13 | AppArmor + firewalld |
| 14 | Customized Calamares installer |
| 15 | Hybrid offline base / optional online installer |
| 16 | Guided updates, snapshots and assisted rollback |
| 17 | Balanced adaptive performance, zram and optional GameMode |
| 18 | Fully Loaded desktop and applications |
| 19 | Zsh interactive shell, Bash system scripts |
| 20 | Persistent diagnostics with custom tools |
| 21 | Restic encrypted backup + Snapper maintenance |
| 22 | Maximum plug-and-play hardware compatibility |
| 23 | Sinister Crimson design |
| 24 | Sinister Command top status bar and floating bottom dock |
| 25 | KDE Kicker traditional cascading application menu |
| 26 | Fully custom Qt/QML SinisterNux Welcome Center |
| 27 | Fully local development |
| 28 | Rolling Arch + staged Testing/Stable SinisterNux packages |
| 29 | Standard Btrfs subvolumes, optional LUKS2/hibernation, zram default |
| 30 | sudo + KDE Polkit, optional fingerprint/FIDO2, recovery safeguards |
| 31 | KVM/QEMU/libvirt/virt-manager and rootless Podman/Distrobox |
| 32 | Custom Qt/QML pacman frontend and KDE Discover for Flatpaks |
| 33 | Fully Loaded gaming with optional performance profiles |
| 34 | Layered Zen/LTS, Limine, Snapper, dracut, Rescue ISO, Restic recovery |
| 35 | Universal accessibility and multilingual support |
| 36 | Privacy by default, granular opt-in; no alpha telemetry |
| 37 | Progressive alpha milestones |
| 38 | Dedicated clean Arch build VM with disposable test VMs |
| 39 | Local Git monorepo + Makefile |

## Alpha 0.1 limitations

We are starting from upstream Archiso releng and retaining its **live ISO** boot infrastructure. No KDE, no installed Limine/Zen/LTS/dracut stack, no Calamares, and no verified snapshot recovery yet. These are later milestones.

Do not install Alpha 0.1 on a physical disk. Build on a clean Arch VM, boot in a separate disposable QEMU/UEFI test VM, and record observed results.
