# AGENTS

このリポジトリは Hyd3 projects の公開 template baseline です。
生成先 repo の目的に合わせて最小限を残し、不要な雛形は削って構いません。

## 基本方針

- 特に指定がない限り、issue / PR / commit 本文 / docs は日本語で書く。
- public repository として安全な既定値を優先する。
- 秘密情報、個人情報、環境固有 state、生成物 cache はコミットしない。
- GitHub Actions は最小権限を明示し、checkout では `persist-credentials: false` を使う。
- Dependabot は minor / patch をまとめて扱い、major update は人が判断する。
- automerge は CI と dependency review の成功後だけ許可する。
- repo 固有の判断は `docs/operations/repo-baseline.md` に追記する。

## Consultation Gate

- ユーザーが懸念、疑問、設計判断、方針相談を述べている場合は、ただちに実装しない。
- まず質問への回答、現状整理、実装するなら何を変えるかの計画を提示し、ユーザー承認後に編集、commit、push へ進む。

## GitHub Hygiene

- issue / PR 作成時は、title prefix ではなく labels で種別、領域、状態、リスクを表す。
- PR title は squash merge commit に使う場合だけ Conventional Commits prefix を許容する。
- squash merge commit title への流用方針が未確認なら、PR title も prefix なしを既定にする。
- 少なくとも種別 label を付ける。迷う場合は `needs-triage` を付ける。
- 正確な label 名は `.github/labels.yml` を source of truth とする。docs-only 変更は `documentation` を既定候補にする。
- `.github/labels.yml` を変更したら、`scripts/sync-labels --repo OWNER/REPO --dry-run` で差分を確認し、必要なら `--apply` で GitHub 側に反映する。
- issue / PR template がある場合は、その見出しとレイアウトを維持して記述する。template を使わなかった場合は作成後に本文を更新して合わせる。

## 変更時の判断基準

- template として再利用できる設定は残す。
- repo 固有の product / domain / deployment 設定は生成先 repo で追加する。
- security / CI / issue workflow の baseline を壊す変更では、代替策を同じ PR に含める。
- manual setup が残る場合は `docs/operations/manual-tasks.md` に記録する。

## 推奨検証

- YAML 変更後は構文検証を行う。
- GitHub Actions 変更後は push 後の workflow 結果を確認する。
- ruleset / secrets / GitHub App 設定は GitHub UI または `gh` で別途確認する。

## コミット方針

- 件名は変更の主題が一読で分かるように簡潔に書く。
- 本文は原則 `What:` と `Why:` を箇条書きで書き、内容は日本語にする。
- `How:` は、実装手段や制約対応が判断材料になるときだけ追加する。
- 小さな変更でも、件名だけでは意図が読めないなら本文を省略しない。

## 初期導入 checklist

1. README の repo 名、目的、利用方法を実 repo 向けに更新する。
2. `docs/operations/repo-baseline.md` の metadata を埋める。
3. 必要な secret / GitHub App / environments を作成する。
4. ruleset example を確認し、必要な bypass actor を設定してから有効化する。
5. 初回 CI と dependency review が成功することを確認する。
