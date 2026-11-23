from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from helpers import load_script

apply_repo_settings = load_script("apply-repo-settings")

BASELINE = """\
version: 2
actions_policy:
  external_action_ref: full-40-character-sha
repository_settings:
  allow_merge_commit: true
  allow_squash_merge: true
  allow_rebase_merge: true
  allow_auto_merge: true
  allow_update_branch: false
  delete_branch_on_merge: true
  merge_commit_title: PR_TITLE
  merge_commit_message: BLANK
  squash_merge_commit_title: PR_TITLE
  squash_merge_commit_message: BLANK
other_section:
  key: value
"""


def write_baseline(text: str) -> Path:
    handle = tempfile.NamedTemporaryFile(
        "w", suffix=".yml", delete=False, encoding="utf-8"
    )
    handle.write(text)
    handle.close()
    return Path(handle.name)


class ParseSettingsTest(unittest.TestCase):
    def test_repository_settingsだけを型付きで読む(self) -> None:
        settings = apply_repo_settings.parse_settings(write_baseline(BASELINE))
        self.assertEqual(len(settings), 10)
        self.assertIs(settings["allow_auto_merge"], True)
        self.assertIs(settings["allow_update_branch"], False)
        self.assertEqual(settings["squash_merge_commit_title"], "PR_TITLE")
        self.assertEqual(settings["merge_commit_message"], "BLANK")

    def test_未知のkeyはエラーにする(self) -> None:
        text = BASELINE.replace("allow_auto_merge: true", "allow_auto_merge: true\n  unknown_key: true")
        with self.assertRaises(ValueError):
            apply_repo_settings.parse_settings(write_baseline(text))

    def test_不足はエラーにする(self) -> None:
        text = BASELINE.replace("  allow_auto_merge: true\n", "")
        with self.assertRaises(ValueError):
            apply_repo_settings.parse_settings(write_baseline(text))

    def test_不正な列挙値はエラーにする(self) -> None:
        text = BASELINE.replace("merge_commit_message: BLANK", "merge_commit_message: TITLE")
        with self.assertRaises(ValueError):
            apply_repo_settings.parse_settings(write_baseline(text))


class DiffSettingsTest(unittest.TestCase):
    def test_違う値だけを差分として返す(self) -> None:
        declared = {"allow_auto_merge": True, "allow_squash_merge": True}
        current = {"allow_auto_merge": False, "allow_squash_merge": True}
        self.assertEqual(
            apply_repo_settings.diff_settings(declared, current),
            [("allow_auto_merge", False, True)],
        )

    def test_現在値が無いkeyも差分にする(self) -> None:
        declared = {"allow_auto_merge": True}
        self.assertEqual(
            apply_repo_settings.diff_settings(declared, {}),
            [("allow_auto_merge", None, True)],
        )


if __name__ == "__main__":
    unittest.main()
