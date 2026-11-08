import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from hash_isos import process

class HashTests(unittest.TestCase):
    def test_create_verify_tamper(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            iso = directory / "sinisternux-test.iso"
            iso.write_bytes(b"test iso")
            self.assertEqual(process("create", directory), 0)
            self.assertEqual(process("verify", directory), 0)
            iso.write_bytes(b"tampered")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(process("verify", directory), 1)

if __name__ == "__main__":
    unittest.main()
