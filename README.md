# Hyd3 Repository Template

Hyd3 repositoryの共通base templateです。GitHubの`Use this template`から新規repoを作成できる公開形を維持します。

## 含まれるもの

- 軽量な`AGENTS.md`
- `.editorconfig`、`.gitattributes`、`.gitignore`
- 日本語defaultのIssue FormsとPR template
- `.github/labels.yml`のlabels baseline
- Dependabot、dependency review、GitHub Actions static check、baseline CI
- ruleset exampleと初期設定docs

## 言語variant

rootの人間向けファイルは日本語をdefaultとします。英語で使う場合は`variants/en/`のREADME、AGENTS、Issue Forms、PR template、SECURITYを生成先repoへコピーしてください。workflow、Dependabot、labelsのvalidationなどmachine-readableな共通設定はrootだけで管理します。

## Use this template

1. GitHubの`Use this template`から新規repoを作成する。
2. READMEと`docs/operations/repo-baseline.md`を生成先repo向けに更新する。
3. repo固有のbuild、test、release手順を追加する。
4. `./scripts/validate-template`と`git diff --check`を実行する。
5. `docs/operations/manual-tasks.md`を確認し、GitHub側の設定を行う。

## GitHub運用

- Issue titleには種別prefixを付けず、種別はlabelsで表す。
- PR titleは原則Conventional Commits形式とし、squash merge時の履歴へそのまま利用できるようにする。
- Issue Formは`.github/ISSUE_TEMPLATE/bug.yml`、`feature.yml`、`chore.yml`を使う。
- PR templateのcanonicalは`.github/PULL_REQUEST_TEMPLATE/default.md`とする。GitHubの通常のPR作成画面でも読み込めるよう、同内容の`.github/pull_request_template.md`をcompatibility aliasとして置く。
- branchは`<type>/<issue-number>-<short-summary>`を標準とする。

## Labels

`.github/labels.yml`がこのtemplateのlabels baselineです。名前は英語のmachine-readable identifier、descriptionは日本語とします。種別、領域、状態、リスク、規模を必要最小限のlabelで表します。

GitHub上の既存labelを変更する場合は、まずdry-runで差分と削除候補を確認し、既存Issue/PRへの影響を人間が確認してください。通常のsyncはcreate/updateに限定し、削除は明示的な移行判断がある場合だけ行います。

```sh
scripts/sync-labels --repo OWNER/REPO --dry-run
scripts/sync-labels --repo OWNER/REPO --apply
```

## Source of truth

`repo-template`は共通baseの正本です。project type固有の追加物は`my-toolbox/github/templates/{app,tooling,security,dotfiles-public-safe}`で管理し、dotfilesの`repo-bootstrap`がbaseとoverlayをcomposeします。

## GitHub側の手動設定

このrepositoryのファイルだけではbranch protection、ruleset、secrets、Dependabot alerts、private vulnerability reportingは完了しません。初期導入時は`docs/operations/manual-tasks.md`を確認してください。
