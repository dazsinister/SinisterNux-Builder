"""Offline profile transformation tests; do not require Archiso installed."""
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from prepare_profile import ProfileError, add_executable_permission, prepare, replace_shell_assignment

class ProfileTests(unittest.TestCase):
    def test_replace_assignment(self):
        result = replace_shell_assignment('iso_name="archlinux"\ninstall_dir="arch"\n', "iso_name", "sinisternux")
        self.assertIn('iso_name="sinisternux"', result)
        self.assertIn('install_dir="arch"', result)

    def test_missing_assignment_fails(self):
        with self.assertRaises(ProfileError):
            replace_shell_assignment("other=1\n", "iso_name", "sinisternux")

    def test_file_permissions(self):
        result = add_executable_permission('file_permissions=(\n["/etc/shadow"]="0:0:400"\n)\n', "/usr/local/bin/sinister-info")
        self.assertIn('["/usr/local/bin/sinister-info"]="0:0:755"', result)

    def test_mock_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp) / "releng"
            (base / "airootfs").mkdir(parents=True)
            (base / "efiboot" / "loader" / "entries").mkdir(parents=True)
            (base / "profiledef.sh").write_text(
                'iso_name="archlinux"\niso_label="ARCH_2026"\niso_publisher="Arch"\n'
                'iso_application="Arch Live"\niso_version="2026.11"\ninstall_dir="arch"\n'
                'file_permissions=(\n["/etc/shadow"]="0:0:400"\n)\n')
            (base / "packages.x86_64").write_text("linux\ngit\n")
            menu = base / "efiboot/loader/entries/01.conf"
            menu.write_text("title Arch Linux install medium\n")
            target = Path(temp) / "build" / "profile"
            result = prepare(base, target)
            self.assertIn('iso_name="sinisternux"', (result / "profiledef.sh").read_text())
            self.assertIn("zsh", (result / "packages.x86_64").read_text())
            self.assertIn("SinisterNux", (result / "efiboot/loader/entries/01.conf").read_text())
            self.assertIn("archlinux", (base / "profiledef.sh").read_text())

if __name__ == "__main__":
    unittest.main()
