from __future__ import annotations

import unittest

from helpers import load_script

check_baseline = load_script("check-baseline")


class SummarizeLabelsTest(unittest.TestCase):
    def test_差分行だけを数える(self) -> None:
        output = "OK area: app\nCREATE area: ci #ffffff - CI\nUPDATE review: human #000000 - x\n"
        ok, detail = check_baseline.summarize_labels(output)
        self.assertFalse(ok)
        self.assertIn("2", detail)

    def test_一致(self) -> None:
        ok, _ = check_baseline.summarize_labels("OK area: app\nOK review: human\n")
        self.assertTrue(ok)


class SummarizeSettingsTest(unittest.TestCase):
    def test_差分(self) -> None:
        ok, detail = check_baseline.summarize_settings(
            "OK allow_squash_merge: true\nDIFF allow_auto_merge: false -> true\nno drift\n"
        )
        self.assertFalse(ok)
        self.assertIn("1", detail)

    def test_一致(self) -> None:
        ok, _ = check_baseline.summarize_settings("OK allow_auto_merge: true\nno drift\n")
        self.assertTrue(ok)


class SummarizeRulesetTest(unittest.TestCase):
    def test_未作成(self) -> None:
        ok, detail = check_baseline.summarize_ruleset(
            "CREATE ruleset default-branch-baseline: まだ存在しない\n"
        )
        self.assertFalse(ok)
        self.assertEqual(detail, "未作成")

    def test_差分(self) -> None:
        ok, _ = check_baseline.summarize_ruleset("DIFF rule deletion: あり -> なし\n")
        self.assertFalse(ok)

    def test_一致(self) -> None:
        ok, _ = check_baseline.summarize_ruleset(
            "OK ruleset default-branch-baseline: 宣言と一致\n"
        )
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
