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

`.github/labels.yml`が宣言上の正本です。labelの軸は`type`、`priority`、`area`です。

通常の初期同期はcreate/updateだけにします。

```sh
scripts/sync-labels --repo OWNER/REPO --dry-run
scripts/sync-labels --repo OWNER/REPO --apply
```

既存labelを新しい名前へ移行する場合は、対象のrename mappingを明示し、先にdry-runで`RENAME`、`CREATE`、`UPDATE`、`DELETE`の差分を確認します。`RENAME`はGitHub APIの改称を使うため、既存Issue/PRへの付与を保てます。

```sh
scripts/sync-labels --repo OWNER/REPO --dry-run --rename 'OLD LABEL=NEW LABEL' --prune
```

dry-runの出力と既存Issue/PRの付与状況を確認し、削除候補を残さないと判断できた場合だけ明示的に適用します。

```sh
scripts/sync-labels --repo OWNER/REPO --apply --rename 'OLD LABEL=NEW LABEL' --prune
```

`--rename`は対象repoごとに指定し、共通scriptへrepo固有のmappingを埋め込まないでください。通常のsyncでは`--prune`を使わず、不要labelの削除は移行判断と同時に行います。

## 生成先repoでの確認

- [ ] READMEとAGENTSを生成先repoの目的に合わせて更新する。
- [ ] 不要なDependabot ecosystemを削除する。
- [ ] repo固有のlint、test、build、release手順を追加する。
- [ ] secrets、variables、environments、GitHub Appを必要な範囲だけ設定する。
- [ ] `./scripts/validate-template`相当の検証、またはdotfilesの`repo-preflight --agent`を実行する。
