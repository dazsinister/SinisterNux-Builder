#!/usr/bin/env bash
# Experimental post-install software bundle — VM ONLY.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
MANIFEST="$ROOT/config/yolo-packages.txt"
if (( EUID != 0 )); then
  echo "Run as root: sudo bash scripts/yolo-postinstall.sh" >&2
  exit 1
fi
if [[ -d /run/archiso ]]; then
  echo "Refusing to run on a live ISO. Reboot into your INSTALLED VM." >&2
  exit 1
fi
if ! command -v systemd-detect-virt >/dev/null || ! systemd-detect-virt -q; then
  echo "Refusing: first use must be on a disposable VM." >&2
  exit 1
fi
[[ -f "$MANIFEST" ]] || { echo "Missing package manifest: $MANIFEST" >&2; exit 1; }
[[ -f /etc/pacman.conf ]] || { echo "Missing /etc/pacman.conf" >&2; exit 1; }
if ! grep -q '^ID=arch$' /etc/os-release && ! grep -q '^ID=sinisternux$' /etc/os-release; then
  echo "This script supports Arch-derived test installations only." >&2
  exit 1
fi

cat <<'EOF'
SinisterNux YOLO POST-INSTALL — EXPERIMENTAL
- Installs a huge official-repository package bundle on THIS disposable VM.
- Enables multilib for Steam/32-bit packages.
- May download multiple gigabytes, upgrade your whole Arch system,
  install multiple kernels, and require significant disk space.
- Does NOT install or activate Limine, alter your EFI bootloader,
  repartition disks, enable AppArmor kernel parameters, or configure
  Snapper rollback / Restic backups.
- It leaves the Arch identity and boot process unchanged for now.
EOF
read -r -p "Type YOLO-VM-ONLY to continue: " answer
[[ "$answer" == "YOLO-VM-ONLY" ]] || { echo "Cancelled."; exit 1; }

if ! grep -q '^\[multilib\]$' /etc/pacman.conf; then
  if grep -q '^#\[multilib\]$' /etc/pacman.conf; then
    cp -a /etc/pacman.conf "/etc/pacman.conf.sinisternux-yolo.$(date +%Y%m%d%H%M%S).bak"
    sed -i '/^#\[multilib\]/,+1 s/^#//' /etc/pacman.conf
  else
    echo "Cannot find standard multilib stanza. Enable it manually, then rerun." >&2
    exit 1
  fi
fi

echo "Updating system completely BEFORE installing additional packages..."
pacman -Syu

packages=()
while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%%#*}"
  line="${line//[[:space:]]/}"
  [[ -z "$line" ]] && continue
  if [[ ! "$line" =~ ^[a-z0-9@._+-]+$ ]]; then
    echo "Invalid package name in manifest: $line" >&2
    exit 1
  fi
  packages+=("$line")
done < "$MANIFEST"

available=()
missing=()
for pkg in "${packages[@]}"; do
  if pacman -Si -- "$pkg" >/dev/null 2>&1; then
    available+=("$pkg")
  else
    missing+=("$pkg")
  fi
done
if (( ${#missing[@]} > 0 )); then
  echo "Not found in current enabled repositories:"
  printf '  %s\n' "${missing[@]}"
  echo "These will be skipped. Investigate availability after the install."
fi
if (( ${#available[@]} == 0 )); then
  echo "No package names resolved." >&2
  exit 1
fi

echo "Installing ${#available[@]} packages through pacman..."
pacman -S --needed -- "${available[@]}"

# Prepare conservative service defaults for next boot.
for service in firewalld.service bluetooth.service cups.service; do
  if systemctl list-unit-files --no-legend "$service" 2>/dev/null | grep -q "^$service"; then
    systemctl enable "$service" || true
  fi
done

echo
echo "Bundle complete. Review pacman warnings and missing packages."
echo "Restart into the existing bootloader; rollback/rescue is not yet configured."
