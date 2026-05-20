# GitHub Labels

このディレクトリは Hyd3 系 repo の標準 label 定義を管理します。

## Source of Truth

`labels.yml` を label 定義の source of truth とします。
repo に反映する前に必ず dry-run で差分を確認してください。

```sh
scripts/sync-labels --repo Hyd3-14/repo-template --dry-run
scripts/sync-labels --repo Hyd3-14/repo-template --apply
scripts/sync-labels --repo Hyd3-14/another-repo --file .github/labels/labels.yml --dry-run
```

## 命名規則

- label name は `NN: group/name` 形式にします。
- description は日本語で、付与条件が分かる説明にします。
- 数字 prefix は一覧順を安定させるために使います。
- 色は prefix ではなく意味で割り当てます。
- 迷う場合は `00: needs-triage` を付けます。

## 配色

- 赤: 障害、security、breaking、blocked、major
- 黄: triage、needs-info、needs-decision、人間待ち
- 青: docs、CI、GitHub、dependencies など領域
- 緑: automerge、patch/minor、ready、低リスク
- 紫: discussion、question、test など判断・探索系
- 灰: chore、resolution、duplicate、invalid、wontfix

## 反映方針

`scripts/sync-labels` は create/update のみを行います。
既存 label の削除は issue / PR / automation への影響が大きいため、初期版では実行しません。
不要 label は dry-run の `stale` 表示を見て、人間が必要に応じて整理します。
