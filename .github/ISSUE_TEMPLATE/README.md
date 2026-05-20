# Issue Templates

Issue は YAML Issue Forms で管理します。
title prefix は使わず、種別や状態は labels で表します。

## Template

| Template | 用途 | 初期 labels |
| --- | --- | --- |
| `bug.yml` | 不具合、回帰 | `10: type/bug`, `00: needs-triage` |
| `feature.yml` | 新機能、拡張 | `10: type/feature`, `00: needs-triage` |
| `docs.yml` | 文書更新 | `10: type/docs`, `20: area/docs` |
| `task.yml` | 保守、設定、repo 運用 | `10: type/chore`, `00: needs-triage` |
| `question.yml` | 回答で閉じられる確認 | `10: type/question`, `30: status/needs-info` |
| `discussion.yml` | 方針、設計、仕様判断 | `10: type/discussion`, `30: status/needs-decision` |

## 運用

- title は自然文で書き、`bug:` や `feat:` の prefix は付けません。
- 迷った issue は `00: needs-triage` 付き template を選びます。
- `question` は回答で閉じられる確認に使います。
- `discussion` は結論後に実装 issue や docs へ落とす議論に使います。
