from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
# validate-template自身の走査に引っかからないよう、実行時に組み立てる。
LEGACY_REFERENCE = "size" + ": s\n"


class ValidateTemplateScanTest(unittest.TestCase):
    """validate-templateの旧label走査が依存物と生成物を読まないことを確かめる。"""

    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name) / "repo"
        shutil.copytree(
            REPO_ROOT,
            self.root,
            ignore=shutil.ignore_patterns(".git", "node_modules", "dist", "__pycache__"),
        )

    def tearDown(self) -> None:
        self.directory.cleanup()

    def write(self, relative: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(LEGACY_REFERENCE, encoding="utf-8")

    def validate(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["./scripts/validate-template"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def test_node_modulesとdistの旧label参照では失敗しない(self) -> None:
        self.write("node_modules/mdast-util-to-hast/readme.md")
        self.write("dist/assets/readme.md")

        completed = self.validate()

        self.assertEqual(completed.returncode, 0, completed.stdout)

    def test_repository直下の旧label参照は引き続き検出する(self) -> None:
        self.write("notes.md")

        completed = self.validate()

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("旧label参照が残っています", completed.stdout)


if __name__ == "__main__":
    unittest.main()
