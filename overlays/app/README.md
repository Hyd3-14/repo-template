# Application Repository Template

Web アプリや API サーバー向けのテンプレート。

`repo-template` の共通GitHub運用を前提に、設計記録、運用手順、軽いreleaseフローを最初から置く。

## 想定する用途

- Next.js アプリ
- API サーバー
- DB / 認証 / デプロイを伴う個人プロダクト

## 追加で含めるもの

- `docs/adr/`
- `docs/development/`
- `docs/operations/`
- `docs/postmortem/`
- `.github/actions/setup-node-pnpm/action.yml`
- `.github/PULL_REQUEST_TEMPLATE/periodic-main-promotion.md`
- `.github/workflows/release.yml`

## 方針

- deploy workflow はサービス依存が強いため含めない
- release と設計・運用ドキュメントの受け皿だけ先に作る
- `repo-template`をbaseとして適用した上で、このdirectoryの追加ファイルを重ねる

## Portless

portless を導入する repo では、pre-1.0 の揺れを避けるため devDependency に exact pin する。Next.js など通常の `.localhost` 開発では追加設定は不要で、LAN mode の `.local` hostnames を使う場合だけ framework 側の allowed origins を確認する。
