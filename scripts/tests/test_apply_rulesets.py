from __future__ import annotations

import copy
import unittest

from helpers import load_script

apply_rulesets = load_script("apply-rulesets")

DECLARATION = {
    "name": "default-branch-baseline",
    "target": "branch",
    "enforcement": "active",
    "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
    "rules": [
        {"type": "deletion"},
        {
            "type": "pull_request",
            "parameters": {
                "required_approving_review_count": 0,
                "allowed_merge_methods": ["squash", "rebase"],
            },
        },
        {
            "type": "required_status_checks",
            "parameters": {
                "strict_required_status_checks_policy": True,
                "required_status_checks": [
                    {"context": "Baseline static checks", "integration_id": 15368}
                ],
            },
        },
    ],
}


def server_copy() -> dict:
    """サーバーが既定値を補った形を模す。"""
    data = copy.deepcopy(DECLARATION)
    data["id"] = 123
    for rule in data["rules"]:
        if rule["type"] == "pull_request":
            rule["parameters"]["require_extra_approval_for_unattributed_changes"] = True
            rule["parameters"]["required_reviewers"] = []
    return data


class DescribeDiffTest(unittest.TestCase):
    def test_サーバーの既定値は差分にしない(self) -> None:
        self.assertEqual(apply_rulesets.describe_diff(DECLARATION, server_copy()), [])

    def test_enforcementの違いを検出する(self) -> None:
        current = server_copy()
        current["enforcement"] = "disabled"
        diffs = apply_rulesets.describe_diff(DECLARATION, current)
        self.assertEqual(len(diffs), 1)
        self.assertIn("enforcement", diffs[0])

    def test_必須チェックの違いを検出する(self) -> None:
        current = server_copy()
        for rule in current["rules"]:
            if rule["type"] == "required_status_checks":
                rule["parameters"]["required_status_checks"] = []
        diffs = apply_rulesets.describe_diff(DECLARATION, current)
        self.assertEqual(len(diffs), 1)
        self.assertIn("required_status_checks", diffs[0])

    def test_ルールの有無を検出する(self) -> None:
        current = server_copy()
        current["rules"] = [
            rule for rule in current["rules"] if rule["type"] != "deletion"
        ]
        diffs = apply_rulesets.describe_diff(DECLARATION, current)
        self.assertTrue(any("deletion" in line for line in diffs))


class LoadDeclarationTest(unittest.TestCase):
    def test_必須キーの不足はエラーにする(self) -> None:
        import tempfile
        from pathlib import Path

        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        )
        handle.write('{"name": "x"}')
        handle.close()
        with self.assertRaises(ValueError):
            apply_rulesets.load_declaration(Path(handle.name))


if __name__ == "__main__":
    unittest.main()
