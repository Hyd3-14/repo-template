# セキュリティ方針

## 対応対象

default branchの最新状態を対象に保守します。生成先repoでは公開しているrelease lineに合わせて更新してください。

| Version | Supported |
| --- | --- |
| default branch | Yes |

## 脆弱性の報告

脆弱性や秘密情報の混入を見つけた場合は、公開Issueに詳細を書かないでください。GitHub Security Advisoryが有効なら、Private vulnerability reportingを使ってください。

Private vulnerability reportingが未設定の場合は、maintainerが指定する非公開の連絡先をREADMEまたはrepo settingsに追記してください。

## 対応

- 受領後に影響範囲と再現条件を確認する。
- 秘密情報が含まれる場合は、rotationと履歴対応を優先する。
- 修正PRでは必要な範囲だけを変更し、再発防止の検証を追加する。
- 公開disclosureは修正または緩和策の準備後に行う。

## Baseline

- GitHub Actionsのtoken permissionはjob単位で最小化する。
- third-party actionは固定versionを使い、floating refを避ける。
- Dependabot alerts、dependency review、secret scanningを有効にする。
- secrets、tokens、credentials、session、履歴、logs、cacheをcommitしない。
