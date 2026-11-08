# Alpha 0.2 — KDE live desktop plan

Status: planning, NOT boot-tested. Baseline is main (Alpha 0.1 verified live boot).

## Phase A: functional graphical desktop
- Add KDE Plasma (Wayland + XWayland), Konsole, Dolphin, NetworkManager, PipeWire, WirePlumber, fonts and a compatible display manager to the generated Archiso profile.
- Configure a live-only local account and graphical login/autologin after confirming current Arch package and service names.
- Retain text-console fallback, tested networking, and the original Alpha 0.1 ISO.
- Use a distinctive Alpha 0.2 ISO build identifier to avoid clobbering the previous image.
- Do not introduce Calamares, Limine, or an installed system into this live-desktop milestone.

## Acceptance checklist
- [ ] ISO builds in the Arch builder VM.
- [ ] SHA256 verifies.
- [ ] UEFI/OVMF + VNC live boot succeeds in disposable Unraid test VM.
- [ ] KDE Plasma graphical session works.
- [ ] Konsole and Dolphin open.
- [ ] Networking and DNS work.
- [ ] PipeWire/WirePlumber services run.
- [ ] Rescue TTY remains reachable via VM Send Key menu.
- [ ] Clean guest shutdown.
- [ ] Record results and fix errors before declaring success.

## Phase B: Sinister Crimson
Once Phase A passes, add theme, KDE layout, and Kicker launcher in small commits, testing each build.

## Safety
Develop only on the alpha-0.2-kde branch; keep main as the known-good Alpha 0.1 baseline. Keep a separate copy of the successfully booted ISO on Unraid.
