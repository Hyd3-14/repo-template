from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from helpers import load_script

ci_changes = load_script("ci-changes")


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()


class CanSkipTest(unittest.TestCase):
    def test_許可した文書とGitHub運用設定だけを省略対象にする(self) -> None:
        for path in [
            "README.md",
            "docs/operations/repo-baseline.md",
            ".github/ISSUE_TEMPLATE/bug.yml",
            ".github/PULL_REQUEST_TEMPLATE/default.md",
            ".github/labels.yml",
        ]:
            with self.subTest(path=path):
                self.assertTrue(ci_changes.can_skip(path))

    def test_未知のpathとcode隣接の文書は省略しない(self) -> None:
        for path in [
            "src/main.ts",
            "docs/diagram.png",
            "scripts/README.md",
            ".github/workflows/ci.yml",
            ".github/ISSUE_TEMPLATE/nested/form.yml",
            "readme.md",
        ]:
            with self.subTest(path=path):
                self.assertFalse(ci_changes.can_skip(path))


class AssessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.repo = Path(self.directory.name)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.name", "test")
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "commit.gpgsign", "false")
        (self.repo / "README.md").write_text("# test\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "base")
        self.base = git(self.repo, "rev-parse", "HEAD")
        self.previous = os.getcwd()
        os.chdir(self.repo)

    def tearDown(self) -> None:
        os.chdir(self.previous)
        self.directory.cleanup()

    def commit(self, files: dict[str, str]) -> str:
        for name, content in files.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "change")
        return git(self.repo, "rev-parse", "HEAD")

    def env(self, head: str, event: str = "pull_request") -> dict[str, str]:
        return {"CI_EVENT_NAME": event, "CI_BASE_SHA": self.base, "CI_HEAD_SHA": head}

    def test_文書だけの変更では重いjobを省略する(self) -> None:
        head = self.commit({"docs/guide.md": "# guide\n", "README.md": "# changed\n"})
        self.assertEqual(ci_changes.assess(self.env(head))[0], False)

    def test_省略対象以外を1つでも含めば実行する(self) -> None:
        head = self.commit({"docs/guide.md": "# guide\n", "src/app.py": "print()\n"})
        self.assertEqual(ci_changes.assess(self.env(head))[0], True)

    def test_文書へのrenameでも元pathを検査する(self) -> None:
        self.commit({"src/notes.txt": "note\n"})
        self.base = git(self.repo, "rev-parse", "HEAD")
        (self.repo / "docs").mkdir()
        git(self.repo, "mv", "src/notes.txt", "docs/notes.md")
        git(self.repo, "commit", "-q", "-m", "rename")
        head = git(self.repo, "rev-parse", "HEAD")
        self.assertEqual(ci_changes.assess(self.env(head))[0], True)

    def test_PR以外不正なSHA差分なしでは実行する(self) -> None:
        head = self.commit({"docs/guide.md": "# guide\n"})
        self.assertEqual(ci_changes.assess(self.env(head, event="push"))[0], True)
        self.assertEqual(ci_changes.assess({**self.env(head), "CI_BASE_SHA": "main"})[0], True)
        self.assertEqual(ci_changes.assess({**self.env(head), "CI_BASE_SHA": "0" * 40})[0], True)
        self.assertEqual(ci_changes.assess({**self.env(head), "CI_BASE_SHA": head})[0], True)


if __name__ == "__main__":
    unittest.main()
