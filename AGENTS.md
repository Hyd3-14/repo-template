# AGENTS

このリポジトリは Hyd3 repository の共通base templateです。生成先repoの目的に合わせて、不要な雛形は削除してください。

- 特別な指定がない限り、Issue、PR、commit本文、docsは日本語で書く。
- 秘密情報、個人情報、認証情報、session、履歴、cacheなどのruntime stateをcommitしない。
- 無関係な変更を混ぜず、所有者不明の既存変更を上書き・削除・stageしない。
- GitHub Actionsは最小権限を明示し、checkoutでは`persist-credentials: false`を使う。
- repo固有のbuild、test、release手順は生成先repoのdocsへ追加する。
- 変更時は`./scripts/validate-template`と`git diff --check`を実行する。
