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
- label nameは英語、descriptionは日本語とし、`type:`、`priority:`、`area:`の3軸を使う。
- `type:`はIssueの種別、`priority:`は対応優先度、`area:`は主な対象領域を表す。
- 原則として`type:`は1つ、`priority:`は必要なIssueだけ、`area:`は主対象を1つ付与する。横断Issueでは`area:`を複数付与してよい。
- Dependabotのminor/patch更新は自動マージ対象だが、PRのdraft状態を手動保留の手段として使える。

## Labels

`.github/labels.yml`が宣言上の正本です。共通baselineは次の15 labelsです。

- `type: feature`、`type: bug`、`type: chore`、`type: documentation`、`type: test`、`type: security`
- `priority: P0`、`priority: P1`、`priority: P2`
- `area: app`、`area: database`、`area: dependency`、`area: devex`、`area: ci`、`area: deployment`

既存labelを移行する場合は、共通scriptへrepo固有の対応表を埋め込まず、対象repoの実行時に`--rename OLD=NEW`を明示します。GitHub APIの改称を使うため、既存Issue/PRへの付与を保ったまま移行できます。削除を伴う場合は、先にdry-runで差分と利用状況を確認してください。

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
- `.github/PULL_REQUEST_TEMPLATE/default.md`（canonical）
- `.github/pull_request_template.md`（GitHub自動読み込み用。canonicalと同一内容）
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
