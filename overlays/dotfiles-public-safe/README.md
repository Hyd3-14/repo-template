# Dotfiles Public-Safe Template

公開しても破綻しない dotfiles リポジトリ向けテンプレート。

## 目的

- 共有できる設定と個人専用設定を分離する
- 新しいマシンで復元しやすい構成を先に作る
- token や個人情報を repo に置かない

## 含めるもの

- `AGENTS.md`
- `Makefile`
- `scripts/install.sh`
- `docs/SETUP.md`
- `docs/SECURITY.md`
- `git/`
- `zsh/`
- `config/`

## 方針

- install 系は必ず `--dry-run` を先に通す
- 個人情報、認証情報、端末固有パスは local/private 側へ逃がす
- `*.example` を置いて、必要な private ファイルを利用者に作らせる
