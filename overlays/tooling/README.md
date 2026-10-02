# Tooling Repository Template

CLI、スクリプト集、ライブラリ、小さめの OSS 向けテンプレート。

`repo-template` の共通GitHub運用を前提に、app系より軽い構成だけを足す。

## 想定する用途

- CLI ツール
- 自分用ユーティリティ集
- npm package
- 小さめのライブラリ repo

## 追加で含めるもの

- `docs/usage.md`
- `scripts/`
- `examples/`
- `.github/PULL_REQUEST_TEMPLATE/default.md`
- `.github/workflows/release.yml`

## 方針

- deploy / smoke test は含めない
- README と usage doc で利用方法が分かる状態を優先する
- `repo-template`をbaseとして適用した上で、このdirectoryの追加ファイルを重ねる
