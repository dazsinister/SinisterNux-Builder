#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
if [[ "$ROOT" == / || ! -f "$ROOT/Makefile" || ! -f "$ROOT/tools/prepare_profile.py" ]]; then
  echo 'Refusing cleanup: project root verification failed' >&2
  exit 1
fi
paths=("$ROOT/build/work" "$ROOT/build/profile" "$ROOT/build/out")
printf 'Delete generated build files ONLY (including ISO output)?\n'
printf '  %s\n' "${paths[@]}"
printf 'Type DELETE to confirm: '
read -r response
[[ "$response" == DELETE ]] || { echo Cancelled; exit 0; }
for path in "${paths[@]}"; do
  if [[ -L "$path" ]]; then
    echo "Refusing symlink at $path" >&2
    exit 1
  fi
done
sudo rm -rf -- "${paths[@]}"
echo 'Generated build files removed.'
