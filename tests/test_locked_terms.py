import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bethesda_localization_qa.locked_terms import (
    choose_josa,
    protect_format_tokens,
    restore_format_tokens,
    restore_locked,
)


class LockedTermsTests(unittest.TestCase):
    def test_josa_batchim_and_rieul(self):
        self.assertEqual(choose_josa("비탄", "OBJ"), "을")
        self.assertEqual(choose_josa("브루마", "OBJ"), "를")
        self.assertEqual(choose_josa("펠리날", "DIR"), "로")

    def test_restore_locked_marker(self):
        mapping = [{"token": "__PN001__", "target": "비탄"}]
        self.assertEqual(
            restore_locked("__PN001__{OBJ} 지켜라", mapping),
            "비탄을 지켜라",
        )

    def test_restore_locked_direct_target_is_allowed(self):
        mapping = [{"token": "__PN001__", "target": "탐리엘"}]
        self.assertEqual(
            restore_locked("탐리엘의 역사", mapping),
            "탐리엘의 역사",
        )

    def test_format_roundtrip(self):
        source = "Hello<br>World\nValue: %d"
        protected, mapping = protect_format_tokens(source)
        self.assertIn("__FMT001__", protected)
        self.assertEqual(restore_format_tokens(protected, mapping), source)


if __name__ == "__main__":
    unittest.main()
