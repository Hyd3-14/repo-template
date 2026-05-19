# Security Policy

## Supported Versions

この template は default branch の最新状態を対象に保守します。
生成先 repo では、公開している release line に合わせてこの表を更新してください。

| Version | Supported |
| --- | --- |
| default branch | Yes |

## Reporting a Vulnerability

脆弱性や秘密情報の混入を見つけた場合は、public issue には詳細を書かないでください。
GitHub Security Advisory が有効な repo では、Private vulnerability reporting を使ってください。

Private vulnerability reporting が未設定の場合は、maintainer が指定した private channel を README または repo settings に追記してください。

## Handling

- 受領後、影響範囲と再現条件を確認します。
- 秘密情報が含まれる場合は、rotation と履歴対応を優先します。
- 修正 PR では、必要な範囲だけを変更し、再発防止の検証を追加します。
- 公開 disclosure は修正または緩和策の準備後に行います。

## Baseline Expectations

- GitHub Actions の token permission は job 単位で最小化する。
- Third-party actions は固定 version を使い、floating ref を避ける。
- Dependabot alerts, dependency review, secret scanning を有効化する。
- secrets, tokens, credentials, session files, logs, caches をコミットしない。
