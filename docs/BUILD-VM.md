# Clean Arch build VM

Use virt-manager and create a **new** Arch Linux VM: 4 vCPUs, 8 GiB RAM, an 80 GiB **virtual** disk, UEFI/OVMF firmware, and NAT network. Install a minimal Arch system with a sudo-capable user. Do not pass through a physical disk.

Inside the builder:

```bash
sudo pacman -Syu
sudo pacman -S --needed archiso git make python sudo
git clone https://github.com/dazsinister/SinisterNux-Builder.git
cd SinisterNux-Builder
make doctor
make check
make iso
make verify
```

If build fails, preserve the full error output. Build output is under `build/out/`. This is an experimental **live ISO only**, not a disk installer.

On CachyOS, use a **separate disposable test VM** with UEFI/OVMF to boot the generated ISO. Verify:

```bash
sinister-info
cat /etc/os-release
uname -a
ip a
ping -c 3 archlinux.org
```

Do not overwrite the build VM or modify real partitions.
