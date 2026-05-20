# Pull Request Templates

GitHub は PR template から labels を自動付与しません。
PR の labels は reviewer、maintainer、automation が付けます。

## Templates

- `default.md`: 通常変更
- `docs.md`: docs-only 変更
- `dependency.md`: 依存更新
- `release.md`: release / promotion

通常の PR 作成では `.github/pull_request_template.md` が使われます。
用途別 template を使う場合は、PR 作成 URL に query parameter を付けます。

```text
https://github.com/OWNER/REPO/compare/main...branch?quick_pull=1&template=docs.md
https://github.com/OWNER/REPO/compare/main...branch?quick_pull=1&template=dependency.md
```

PR title は squash merge commit title に流用する場合だけ Conventional Commits prefix を使います。
流用方針が未確認なら、title prefix なしを既定にします。
