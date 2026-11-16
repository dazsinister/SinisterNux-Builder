"""Offline tests of YOLO ISO package/profile staging."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from prepare_yolo import enable_multilib, prepare

class YoloTests(unittest.TestCase):
    def test_manifest_uses_wayland_not_removed_x11_session(self):
        root = Path(__file__).resolve().parents[1]
        manifest = (root / "config" / "yolo-packages.txt").read_text().splitlines()
        names = [line.strip() for line in manifest if line.strip() and not line.startswith("#")]
        self.assertNotIn("plasma-x11-session", names)
        desktop = (root / "config" / "desktop-packages.txt").read_text().splitlines()
        self.assertIn("xorg-xwayland", desktop)

    def test_enable_multilib(self):
        source = "[core]\nInclude = /etc/pacman.d/mirrorlist\n#[multilib]\n#Include = /etc/pacman.d/mirrorlist\n"
        result = enable_multilib(source)
        self.assertIn("\n[multilib]\nInclude = /etc/pacman.d/mirrorlist", result)
        self.assertEqual(enable_multilib(result), result)

    def test_generated_profile(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "stage"
            source.mkdir()
            (source / "profiledef.sh").write_text(
                'iso_name="sinisternux"\n'
                'iso_label="SINISTER_02"\n'
                'iso_application="SinisterNux Alpha 0.2 KDE Live"\n'
                'iso_version="0.2.0_alpha_$(date +%Y%m%d_%H%M%S)"\n'
                'file_permissions=(\n["/etc/shadow"]="0:0:400"\n)\n'
            )
            (source / "pacman.conf").write_text(
                "[core]\nInclude = /etc/pacman.d/mirrorlist\n"
                "#[multilib]\n#Include = /etc/pacman.d/mirrorlist\n"
            )
            (source / "packages.x86_64").write_text("linux\nkonsole\n")
            target = Path(td) / "yolo"
            prepare(source, target)
            definition = (target / "profiledef.sh").read_text()
            self.assertIn('iso_name="sinisternux-yolo"', definition)
            self.assertIn('SINISTER_YOLO', definition)
            self.assertIn('["/usr/local/bin/sinisternux-install-preview"]="0:0:755"', definition)
            self.assertIn("0.9.0_yolo", definition)
            self.assertIn("[multilib]\nInclude", (target / "pacman.conf").read_text())
            packages = (target / "packages.x86_64").read_text()
            self.assertIn("\nsteam\n", packages)
            self.assertEqual(packages.count("\nkonsole\n"), 1)
            self.assertTrue((target / "airootfs/usr/local/bin/sinisternux-install-preview").is_file())

if __name__ == "__main__":
    unittest.main()
