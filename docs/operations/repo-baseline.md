# Repository Baseline

この文書は、`repo-template`から生成するHyd3 repositoryの共通前提を記録します。生成先repo固有の運用はここへ大量に戻さず、そのrepoのdocsへ追加してください。

## 責務

- `repo-template`: README、軽量AGENTS、Issue Forms、PR template、labels、CI、Dependabotなど共通baseの正本。
- `my-toolbox`: `app`、`tooling`、`security`、`dotfiles-public-safe`などproject type固有overlayの正本。
- `dotfiles`: repo-preflight、repo-bootstrap、branch検査、publish workflow、drift検査など運用仕様と実行ロジックの正本。

## 共通仕様

- Issue titleには種別prefixを付けず、`type: bug`、`type: feature`、`type: chore`などのlabelで分類する。
- PR titleは原則Conventional Commits形式とする。
- PR本文は`関連Issue`、`概要`、`変更点`、`動作確認`、`補足`の軽量構成とする。
- branchは`<type>/<issue-number>-<short-summary>`とする。
- label nameは英語、descriptionは日本語とし、`type:`、`area:`、`status:`、`risk:`、`size:`の最小カテゴリを使う。

## Required files

- `README.md`
- `AGENTS.md`
- `SECURITY.md`
- `.editorconfig`
- `.gitattributes`
- `.gitignore`
- `.github/hyd3-baseline.yml`
- `.github/labels.yml`
- `.github/ISSUE_TEMPLATE/bug.yml`
- `.github/ISSUE_TEMPLATE/feature.yml`
- `.github/ISSUE_TEMPLATE/chore.yml`
- `.github/PULL_REQUEST_TEMPLATE/default.md`
- `.github/workflows/ci.yml`
- `.github/workflows/dependency-review.yml`

## 検証

```sh
./scripts/validate-template
git diff --check
```

dotfiles側の`repo-preflight --agent`とcross-repo drift検査は、生成先repoへ必要な場合だけ適用します。

## GitHub側で残る設定

branch protectionまたはruleset、required checks、Dependabot alerts、secret scanning、private vulnerability reporting、secrets、GitHub App権限はファイルから自動適用しません。`manual-tasks.md`に確認項目を残します。
