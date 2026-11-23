# 始め方

このページは、baseline を導入する手順を、手作業の場合と AI Agent に任せる場合の両方について説明します。このテンプレートの事前知識は前提にしていません。

English: [getting-started.md](getting-started.md)

## 前提

- baseline を適用する GitHub リポジトリ（新規でも既存でも可）があり、管理者権限を持っている
- `gh`（GitHub CLI）の認証が済んでいる（`gh auth status` が成功する）
- Python 3 がある（helper スクリプトは標準ライブラリだけを使う）
- [Copier](https://copier.readthedocs.io/)（テンプレートから新規リポジトリを作る場合だけ必要）

## Agent に任せる

次のブロックを Agent（Claude Code、Codex など）へ貼り、`OWNER/REPO` を対象リポジトリに置き換えてください。Agent はこのページの手作業の手順と同じことを実行し、取り返しのつかない変更の前には報告します。

```text
Hyd3-14/repo-template の baseline を OWNER/REPO にセットアップしてください。

1. https://github.com/Hyd3-14/repo-template を clone し、その clone の中で作業してください。
   スクリプトは宣言を手元で読み、--repo で指定したリポジトリへ作用します。
   対象リポジトリ側にファイルが無くても実行できます。
2. `python3 scripts/check-baseline --repo OWNER/REPO` を実行し、何も変更する前に
   結果の全文を私に見せてください。
3. 次の順で適用してください。各スクリプトは先に --dry-run を実行し、出力を私に見せてから --apply してください。
   - python3 scripts/sync-labels --repo OWNER/REPO --apply
   - python3 scripts/apply-repo-settings --repo OWNER/REPO --apply
   - python3 scripts/apply-rulesets --repo OWNER/REPO --apply
4. 次の場合は続ける前に止まって私に確認してください。
   - check-baseline が必須チェック不足の WARN を出した場合（そのまま ruleset を適用すると全てのマージが止まります）
   - dry-run がラベルの削除候補（sync-labels の STALE 行）を示した場合
5. 最後に check-baseline を再実行し、結果を報告してください。全ての領域が OK になることが完了の条件です。
```

## 進め方A：新規リポジトリ

```bash
copier copy gh:Hyd3-14/repo-template <dest>
cd <dest>
gh repo create <owner>/<repo> --public --source=. --push   # private の場合は --private
python3 scripts/sync-labels --repo <owner>/<repo> --apply
python3 scripts/apply-repo-settings --repo <owner>/<repo> --apply
python3 scripts/apply-rulesets --repo <owner>/<repo> --apply
python3 scripts/check-baseline --repo <owner>/<repo>
```

最後のコマンドで全ての領域が OK と表示されれば完了です。

## 進め方B：既存リポジトリ

GitHub 側の状態（ラベル、リポジトリ設定、ruleset）は、このテンプレートの clone から適用できます。対象リポジトリのファイルを先に変える必要はありません。

```bash
git clone https://github.com/Hyd3-14/repo-template
cd repo-template
python3 scripts/check-baseline --repo <owner>/<repo>   # 現在の状態を確認する
```

レポートを読んでから、ラベル、設定、ruleset の順に `--apply` で適用します（進め方Aと同じ順番）。ファイル側の baseline（workflow、Issue フォーム、PR テンプレート）は別で、Copier で作業用ディレクトリへ生成して必要なファイルを写すか、少しずつ取り入れてください。`check-baseline` が報告するのは GitHub 側の状態だけです。

## 詰まったとき

- **check-baseline が必須チェック不足の WARN を出す。** ruleset は `Baseline static checks` と `GitHub Actions Static Checks` の workflow を必須にしています。対象リポジトリに無いまま ruleset を適用すると、全てのマージが止まります。先に baseline の workflow（テンプレートに含まれます）を入れるか、`rulesets/default-branch.json` の宣言を、そのリポジトリで実際に走るチェックに合わせて直してください。
- **sync-labels に STALE と出る。** GitHub 側にあって baseline に無いラベルです。`--apply` だけでは削除されません。削除には `--prune` が必要で、別の明示的な判断として扱ってください。先に、そのラベルが何に付いているかを確認してください。
- **private リポジトリ。** ラベル、設定、ruleset は private リポジトリでも使えます。GitHub Free でも同じです。GitHub Advanced Security が必要な機能は、この baseline には含まれていません。
- **Dependabot の自動マージが動かない。** 前提は `allow_auto_merge` で、リポジトリ設定の宣言に含まれています。`apply-repo-settings` を実行し、`check-baseline` で確認してください。
- **認証エラーでスクリプトが止まる。** スクリプトは `gh` を呼びます。`gh auth status` と、対象リポジトリへの管理者権限があるかを確認してください。
