# AGENTS

このリポジトリは Hyd3 repository の共通base templateです。生成先repoの目的に合わせて、不要な雛形は削除してください。

- 特別な指定がない限り、Issue、PR、commit本文、docsは日本語で書く。
- 秘密情報、個人情報、認証情報、session、履歴、cacheなどのruntime stateをcommitしない。
- 無関係な変更を混ぜず、所有者不明の既存変更を上書き・削除・stageしない。
- GitHub Actionsは各jobに必要最小限の`permissions`と`timeout-minutes`を明示し、外部Actionはfull SHA、checkoutでは`persist-credentials: false`を使う。
- GitHub contextの値をshellへ渡すときはstep-level `env:`を介し、shell内では環境変数をquoteする。静的なAction inputは`with:`に置く。
- repo固有のbuild、test、release手順は生成先repoのdocsへ追加する。
- 変更時は`./scripts/validate-template`と`git diff --check`を実行する。
