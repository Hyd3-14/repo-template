# 手動作業

repository fileだけでは完了しないGitHub側の設定を記録します。

## 初期設定

- [ ] default branchが`main`であることを確認する。
- [ ] Dependabot alertsとsecurity updatesを有効にする。
- [ ] 利用可能ならsecret scanningとprivate vulnerability reportingを有効にする。
- [ ] GitHub Actionsのdefault token permissionをread-onlyにする。
- [ ] `Baseline CI`と`Dependency Review`の実際のcheck名を確認する。
- [ ] default branchのrulesetまたはbranch protectionへ必要なcheckを設定する。

## Labels

`.github/labels.yml`が宣言上の正本です。既存のGitHub labelsをrenameまたは削除する場合は、先にdry-runで差分を確認し、既存Issue/PRから外れる影響を人間が確認してください。

```sh
scripts/sync-labels --repo OWNER/REPO --dry-run --prune
```

削除候補に問題がないと確認できた場合だけ、明示的な移行判断として次を実行します。

```sh
scripts/sync-labels --repo OWNER/REPO --apply --prune
```

通常の初期導入では`--prune`を使わず、create/updateだけを行います。旧labelのrename、既存Issue/PRへの付け替え、削除はこのPRの自動処理対象外です。

## 生成先repoでの確認

- [ ] READMEとAGENTSを生成先repoの目的に合わせて更新する。
- [ ] 不要なDependabot ecosystemを削除する。
- [ ] repo固有のlint、test、build、release手順を追加する。
- [ ] secrets、variables、environments、GitHub Appを必要な範囲だけ設定する。
- [ ] `./scripts/validate-template`相当の検証、またはdotfilesの`repo-preflight --agent`を実行する。
