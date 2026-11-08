# SinisterNux progressive milestones

- [ ] Alpha 0.1: Boot a branded terminal with networking.
- [ ] Alpha 0.2: KDE Plasma, Wayland, Sinister Crimson, Sinister Command, Kicker.
- [ ] Alpha 0.3: Calamares, Btrfs, Linux Zen + LTS, dracut, Limine.
- [ ] Alpha 0.4: Snapper, signed repo, guided updates and rollback.
- [ ] Alpha 0.5: Fully loaded apps, gaming, hardware, virtualization.
- [ ] Alpha 0.6+: Custom Qt/QML apps and graphical rescue center.

## Alpha 0.1 acceptance
- [x] `make iso` succeeds in a clean Arch VM (ISO created; user confirmed).
- [x] ISO boots via UEFI in a disposable Unraid test VM (photo-verified).
- [x] `sinister-info` displays SinisterNux branding (known missing `hostname` command causes exit 127 in initial image; source fix committed, rebuild pending).
- [x] `/etc/os-release` reports SinisterNux (photo-verified).
- [x] Guest network and DNS work (`ping -c 3 archlinux.org`, 3/3 received, 0% loss; photo-verified).
- [ ] ISO SHA-256 verifies (not yet confirmed).
- [ ] Build revision and `pacman -Q archiso` recorded (not yet recorded).

No milestone is marked complete without actual VM verification.

## First boot evidence

On November 7, 2026 local time (ISO image identifies itself as `0.1.0_alpha_20261108`), the user tested the first Alpha 0.1 ISO in a separate Unraid VM. Screenshots verified console boot, `sinister-info` branding, `/etc/os-release`, `uname -n` = `sinisternux`, an active network interface with dynamic addressing, successful DNS resolution, and 3/3 ping replies. The initial `sinister-info` script had a missing `hostname` executable; the source was corrected to `uname -n` in commit `fed56b0` but the corrected ISO still requires rebuild and retest. Kernel observed: `7.2.14-arch1-1`. Do not claim the release is finalized until checksum, fix/rebuild, and provenance checks are complete.
