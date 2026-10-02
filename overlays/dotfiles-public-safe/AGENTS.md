# AGENTS

このリポジトリは個人用 dotfiles だが、公開しても破綻しない状態を維持する。

## 基本方針

- 実名、個人メールアドレス、認証情報、セッション情報、端末固有の秘匿パスはコミットしない
- repo 内の設定は public template として読める形を優先する
- 共有できる設定と個人専用の設定を分離する

## ローカル専用に置くもの

- `~/.gitconfig.local`
- `zsh/env.local.zsh`
- `.zsecret`
- `config/gh/hosts.yml`
- `config/*/credentials.json`
- `config/*/session.json`

## 運用ルール

- install 系スクリプトは、まず `--dry-run` で確認してから適用する
- 誤って秘密情報をコミットした場合は履歴まで含めて対処する
- 設定追加やリンク追加をしたら、関連ドキュメントも更新する
