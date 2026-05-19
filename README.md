# Hyd3 Repository Template

Hyd3 projects のための公開 repository baseline template です。
新規 repo の最初の一手として、security / CI / issue workflow / Dependabot / ruleset の安全な既定値をまとめています。

## Included

- `AGENTS.md`: agent 向けの repo 運用ルール
- `SECURITY.md`: 脆弱性報告と対応方針
- `.github/ISSUE_TEMPLATE/`: bug / feature / chore の issue forms
- `.github/pull_request_template.md`: PR checklist
- `.github/dependabot.yml`: minor / patch grouped update と major の明示レビュー
- `.github/workflows/`: CI, dependency review, Dependabot triage, guarded automerge
- `.github/labels.yml`: baseline label definitions
- `rulesets/*.example.json`: GitHub Rulesets の安全側 example
- `docs/operations/`: repo baseline と manual task の記録

## Use This Template

1. GitHub の "Use this template" から新規 repo を作成する。
2. README と `docs/operations/repo-baseline.md` を新規 repo 向けに更新する。
3. 必要な secrets / GitHub App / environments を作成する。
4. `rulesets/*.example.json` を確認し、bypass actor を追加してから ruleset を有効化する。
5. 初回 PR で CI と dependency review の check 名を確認し、branch protection / ruleset の required checks に反映する。

## Safe Defaults

Dependabot は minor / patch を ecosystem ごとに group 化します。
major update は自動 close せず、`dependencies`, `major-update`, `needs-human-review` を付けて人が判断します。

Automerge workflow は Dependabot PR のみを対象にし、以下を満たす場合だけ merge を試みます。

- PR author が `dependabot[bot]`
- update type が semver minor または patch
- `ci.yml` と `dependency-review.yml` が成功している
- major update ではない

## GitHub Setup Required

この template だけでは GitHub 側の設定は完了しません。
初期導入時に `docs/operations/manual-tasks.md` を確認してください。

Minimum recommended settings:

- Rulesets or branch protection for the default branch
- Required checks: `Baseline static checks` and `Dependency Review`
- GitHub Actions read-only default token permissions
- Dependabot alerts and security updates
- Secrets / variables required by repo-specific workflows
- Bypass actors for emergency maintainers or release automation

## Labels

`.github/labels.yml` は declarative label source として使います。
適用には `github/issue-labeler` など任意の label sync tool を使ってください。
この template は特定の sync tool を固定しません。

## Rulesets

`rulesets/*.example.json` は `enforcement: disabled` を既定にしています。
GitHub UI または管理用 script で内容を確認し、repo 固有の bypass actor と required check 名を調整してから `active` にしてください。

## Validation

ローカルで最低限確認する例:

```sh
git status --short
find . -path ./.git -prune -o -type f -print | sort
```

YAML / workflow の厳密な検証は、生成先 repo の toolchain に合わせて追加してください。
