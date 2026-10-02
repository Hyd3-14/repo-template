from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

from helpers import load_script

docs_toc = load_script("docs-toc")
MARKER = "<!-- START docs-toc -->\n\n<!-- END docs-toc -->"
TARGET = docs_toc.Target("manual.md")


def generate(source: str, target=TARGET) -> str:
    return unquote(docs_toc.generate_toc(source, target))


class GenerateTocTest(unittest.TestCase):
    def test_日本語の章と節をリンクにし本文と見出しを維持する(self) -> None:
        body = "## 開発を始める\n\n本文。\n\n### 初回セットアップ\n\n#### 詳細\n"
        result = generate(f"# マニュアル\n\n説明。\n\n{MARKER}\n\n{body}")
        self.assertIn("- [開発を始める](#開発を始める)", result)
        self.assertIn("  - [初回セットアップ](#初回セットアップ)", result)
        self.assertNotIn("[詳細]", result)
        self.assertTrue(result.startswith("# マニュアル\n\n説明。"))
        self.assertTrue(result.endswith(body))

    def test_anchorをpercent_encodingする(self) -> None:
        result = docs_toc.generate_toc(f"# 文書\n\n{MARKER}\n\n## 章 A\n", TARGET)
        self.assertIn("- [章 A](#%E7%AB%A0-a)", result)

    def test_同名見出しの番号に文書タイトルと表示対象外の見出しも含める(self) -> None:
        result = generate(f"# 重複\n\n{MARKER}\n\n## 重複\n\n#### 重複\n\n## 重複\n")
        self.assertIn("[重複](#重複-1)", result)
        self.assertIn("[重複](#重複-3)", result)
        self.assertNotIn("(#重複-2)", result)

    def test_コードブロック内の見出しを目次に含めない(self) -> None:
        result = generate(f"# 手順\n\n{MARKER}\n\n## 実際の章\n\n```md\n## サンプル\n```\n\n~~~\n## 別のサンプル\n~~~\n")
        self.assertIn("[実際の章](#実際の章)", result)
        self.assertNotIn("サンプル]", result)

    def test_日本語の記号と装飾を除いたanchorの重複を数える(self) -> None:
        source = f"# 文書\n\n{MARKER}\n\n## 採用・_変更_・不採用\n\n#### 採用変更不採用\n\n## 採用変更不採用\n"
        result = generate(source)
        self.assertIn("[採用・_変更_・不採用](#採用変更不採用)", result)
        self.assertIn("[採用変更不採用](#採用変更不採用-2)", result)
        self.assertNotIn("(#採用変更不採用-1)", result)

    def test_inline_codeとlinkを表示文字列にする(self) -> None:
        result = generate(f"# 文書\n\n{MARKER}\n\n## `mise run` と[link](https://example.com)の使い方\n\n## snake_case\n")
        self.assertIn("- [`mise run` とlinkの使い方](#mise-run-とlinkの使い方)", result)
        self.assertIn("- [snake_case](#snake_case)", result)

    def test_既存の第1階層の章を含められる(self) -> None:
        source = f"# 方針\n\n{MARKER}\n\n# 原則\n\n## 詳細\n"
        result = generate(source, docs_toc.Target("manual.md", True))
        self.assertIn("- [原則](#原則)\n  - [詳細](#詳細)", result)
        self.assertTrue(result.endswith("# 原則\n\n## 詳細\n"))

    def test_生成を繰り返しても差分が増えない(self) -> None:
        first = docs_toc.generate_toc(f"# 文書\n\n{MARKER}\n\n## 章\n", TARGET)
        self.assertEqual(docs_toc.generate_toc(first, TARGET), first)

    def test_markerが欠損重複逆順なら失敗する(self) -> None:
        for source in [
            "# 文書\n\n## 章\n",
            f"# 文書\n\n{MARKER}\n\n{MARKER}\n\n## 章\n",
            "# 文書\n\n<!-- END docs-toc -->\n\n<!-- START docs-toc -->\n\n## 章\n",
        ]:
            with self.subTest(source=source), self.assertRaisesRegex(docs_toc.TocError, "marker"):
                docs_toc.generate_toc(source, TARGET)

    def test_コードブロック内のmarkerは置換対象にしない(self) -> None:
        example = "```markdown\n<!-- START docs-toc -->\n<!-- END docs-toc -->\n```\n"
        result = docs_toc.generate_toc(f"# 文書\n\n{MARKER}\n\n## 章\n\n{example}", TARGET)
        self.assertTrue(result.endswith(example))
        self.assertIn("- [章](#%E7%AB%A0)", result)

    def test_タイトルや章見出しがなければ失敗する(self) -> None:
        with self.assertRaisesRegex(docs_toc.TocError, "タイトル"):
            docs_toc.generate_toc(f"本文\n\n{MARKER}\n", TARGET)
        with self.assertRaisesRegex(docs_toc.TocError, "章見出し"):
            docs_toc.generate_toc(f"# 文書\n\n{MARKER}\n\n#### 深い見出し\n", TARGET)


class SyncTocsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def write(self, content: str) -> Path:
        path = self.root / TARGET.path
        path.write_text(content, encoding="utf-8")
        return path

    def test_checkは古い目次を検出してファイルを書き換えない(self) -> None:
        source = f"# 文書\n\n{MARKER}\n\n## 章\n"
        path = self.write(source)
        self.assertEqual(docs_toc.sync_tocs(self.root, [TARGET], check=True), [TARGET.path])
        self.assertEqual(path.read_text(encoding="utf-8"), source)
        self.assertEqual(docs_toc.sync_tocs(self.root, [TARGET]), [TARGET.path])
        self.assertEqual(docs_toc.sync_tocs(self.root, [TARGET], check=True), [])

    def test_見出しを変更するとcheckが不一致を検出する(self) -> None:
        path = self.write(docs_toc.generate_toc(f"# 文書\n\n{MARKER}\n\n## 元の章\n", TARGET))
        edited = path.read_text(encoding="utf-8").replace("## 元の章", "## 新しい章")
        path.write_text(edited, encoding="utf-8")
        self.assertEqual(docs_toc.sync_tocs(self.root, [TARGET], check=True), [TARGET.path])
        self.assertEqual(path.read_text(encoding="utf-8"), edited)

    def test_後続の対象が失敗しても先行文書を書き換えない(self) -> None:
        source = f"# 文書\n\n{MARKER}\n\n## 章\n"
        path = self.write(source)
        with self.assertRaises(docs_toc.TocError):
            docs_toc.sync_tocs(self.root, [TARGET, docs_toc.Target("missing.md")])
        self.assertEqual(path.read_text(encoding="utf-8"), source)


if __name__ == "__main__":
    unittest.main()
