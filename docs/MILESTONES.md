# SinisterNux progressive milestones

- [x] Alpha 0.1 core boot goal: branded terminal, corrected `sinister-info`, and networking verified in a disposable Unraid VM (checksum and build provenance still pending).
- [ ] Alpha 0.2: KDE Plasma, Wayland, Sinister Crimson, Sinister Command, Kicker.
- [ ] Alpha 0.3: Calamares, Btrfs, Linux Zen + LTS, dracut, Limine.
- [ ] Alpha 0.4: Snapper, signed repo, guided updates and rollback.
- [ ] Alpha 0.5: Fully loaded apps, gaming, hardware, virtualization.
- [ ] Alpha 0.6+: Custom Qt/QML apps and graphical rescue center.

## Alpha 0.1 acceptance
- [x] `make iso` succeeds in a clean Arch VM (ISO created; user confirmed).
- [x] ISO boots via UEFI in a disposable Unraid test VM (photo-verified).
- [x] `sinister-info` displays SinisterNux branding and completes without the earlier missing-`hostname` failure after rebuilding with source fix `fed56b0` (user confirmed retest).
- [x] `/etc/os-release` reports SinisterNux (photo-verified).
- [x] Guest network and DNS work (`ping -c 3 archlinux.org`, 3/3 received, 0% loss; photo-verified).
- [x] ISO SHA-256 verifies (user ran `make verify` on the rebuilt ISO and confirmed it passed before launching the test VM).
- [ ] Build revision and `pacman -Q archiso` recorded (not yet recorded).

No milestone is marked complete without actual VM verification.

## First boot evidence

On November 7, 2026 local time (ISO image identifies itself as `0.1.0_alpha_20261108`), the user tested the first Alpha 0.1 ISO in a separate Unraid VM. Screenshots verified console boot, `sinister-info` branding, `/etc/os-release`, `uname -n` = `sinisternux`, an active network interface with dynamic addressing, successful DNS resolution, and 3/3 ping replies. The initial `sinister-info` script had a missing `hostname` executable; the source was corrected to `uname -n` in commit `fed56b0`. The user subsequently rebuilt, booted, and reported that `sinister-info`, OS identification, and networking all checked out. Full output of the corrected test was not supplied. Kernel observed: `7.2.14-arch1-1`. Do not claim the release is finalized until checksum, fix/rebuild, and provenance checks are complete.

## Fixed-image retest

On November 8, 2026 local date, the user confirmed that the **rebuilt Alpha 0.1 image** booted and its `sinister-info`, OS identity, and networking checks passed. The prior `hostname` error is considered fixed in this tested image. SHA-256 verification of the rebuilt image was confirmed by the user. The exact build-source commit and installed archiso package version have not yet been recorded; this remains an administrative follow-up.

## Checksum verification confirmation

The user confirmed running `make verify` on the rebuilt Alpha 0.1 ISO before booting the second test VM; checksum verification passed. The generated checksum file and ISO remain on the user's Unraid/build storage, not committed to GitHub. This closes the checksum acceptance item; source provenance recording is still pending.
