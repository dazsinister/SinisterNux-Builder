"""Exercise Alpha 0.2 profile staging without downloading packages."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from prepare_desktop import configure

class DesktopTests(unittest.TestCase):
    def test_desktop_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / "profile"
            profile.mkdir()
            (profile / "profiledef.sh").write_text(
                'iso_label="SINISTER_01"\n'
                'iso_application="SinisterNux Alpha 0.1 Live Environment"\n'
                'iso_version="0.1.0_alpha_$(date +%Y%m%d)"\n'
                'file_permissions=(\n["/etc/shadow"]="0:0:400"\n)\n'
            )
            (profile / "packages.x86_64").write_text("linux\n")
            configure(profile)
            cfg = (profile / "profiledef.sh").read_text()
            pkgs = (profile / "packages.x86_64").read_text()
            self.assertIn("SINISTER_02", cfg)
            self.assertIn("0.2.0_alpha_", cfg)
            self.assertIn("konsole", pkgs)
            self.assertIn("dolphin", pkgs)
            self.assertIn("plasma-login-manager", pkgs)
            symlink = profile / "airootfs/etc/systemd/system/display-manager.service"
            self.assertTrue(symlink.is_symlink())
            self.assertEqual(symlink.readlink().as_posix(),
                             "/usr/lib/systemd/system/plasmalogin.service")
            self.assertTrue((profile / "airootfs/etc/systemd/system/sinisternux-live-user.service").is_file())
            self.assertTrue((profile / "airootfs/usr/local/sbin/sinisternux-create-live-user").is_file())
            # Applying twice should not duplicate packages or permission entries.
            configure(profile)
            self.assertEqual((profile / "packages.x86_64").read_text().count("\nkonsole\n"), 1)
            self.assertEqual((profile / "profiledef.sh").read_text().count(
                '["/usr/local/sbin/sinisternux-create-live-user"]="0:0:755"'), 1)

if __name__ == "__main__":
    unittest.main()
