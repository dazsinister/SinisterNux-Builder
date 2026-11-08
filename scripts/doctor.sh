#!/usr/bin/env bash
set -euo pipefail
printf 'SinisterNux Alpha 0.1 environment check\n'
printf 'Host: %s\nKernel: %s\n' "$(hostname)" "$(uname -r)"
if [[ -r /etc/arch-release ]]; then printf '[OK] Arch base detected\n'; else printf '[WARN] Build in a clean Arch VM.\n'; fi
for cmd in bash python3 git make sudo mkarchiso sha256sum; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '[OK] %-12s %s\n' "$cmd" "$(command -v "$cmd")"
  else
    printf '[MISSING] %s\n' "$cmd"
  fi
done
if [[ -f /usr/share/archiso/configs/releng/profiledef.sh ]]; then
  printf '[OK] Upstream archiso releng profile exists\n'
else
  printf '[MISSING] releng profile; install archiso\n'
fi
printf '\nFree space:\n'
df -h -- "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
printf '\nMemory:\n'
free -h | head -n 2
