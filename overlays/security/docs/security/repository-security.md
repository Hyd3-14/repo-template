# Repository Security

このテンプレートは、軽量な supply chain / secret scan の導線を追加する。

## Takumi Guard

npm / pnpm / yarn は `.npmrc` の `registry` 設定を読む。Takumi Guard を使う場合は、`.npmrc.example` を参考に `.npmrc` を作る。

```bash
cp .npmrc.example .npmrc
```

private registry を使う repo では、scope ごとに直接 registry を指定して public package だけ Takumi Guard 経由にする。

## gitleaks

CI では `.github/workflows/secret-scan.yml` が gitleaks を実行する。個人アカウントの repo では通常追加 secret は不要だが、Organization-owned repo では `GITLEAKS_LICENSE` が必要になる。

ローカルで確認する場合:

```bash
gitleaks git --config .gitleaks.toml --redact --verbose
```

誤検知時は、まず secret の削除・無効化・ローテーションを検討する。allowlist は理由を残せる場合だけ追加する。

## Local hooks

pre-commit / lefthook / git hooks は repo ごとの運用差が大きいので必須化しない。必要になった repo だけ、gitleaks を pre-commit hook に追加する。

## Workflow pinning

- GitHub Actions は可能な限り commit SHA で pin する。
- Docker image は tag だけでなく digest で pin する。
- gitleaks の PR コメントは初期状態では無効にし、`pull-requests: write` を要求しない。
