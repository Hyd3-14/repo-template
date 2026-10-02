# AGENTS

このテンプレートは app 系リポジトリ向け。

## 追加ルール

- 仕様変更は docs または PR 本文に理由を残す
- 継続的に効く設計判断は `docs/adr/` に残す
- 障害や調査ハマりは `docs/postmortem/` に残す
- release に影響する変更はバージョン方針を明記する

## 運用メモ

- `repo-template` の共通GitHubルールをそのまま適用する
- deploy や smoke test は利用サービスに合わせて別途追加する
