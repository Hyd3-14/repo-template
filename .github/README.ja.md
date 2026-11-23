<h1 align="center">Hyd3 Repository Template</h1>

<p align="center">新しい GitHub リポジトリに、Issue と PR の型、ラベル、リポジトリ設定、ブランチの ruleset、CI チェックまでそろった baseline を、ファイルとスクリプトで入れる <a href="https://copier.readthedocs.io/">Copier</a> テンプレートです。セットアップは生成1回と適用コマンド3本で終わり、Settings の画面を順にクリックする作業は要りません。</p>

<p align="center"><a href="README.md">English</a> | 日本語</p>

## 得られるもの

| 対象 | まっさらな状態から始める場合 | このテンプレートを使う場合 |
| --- | --- | --- |
| Issue | タイトルは自由形式、ラベルはその場の判断 | 6種のフォームで起票し、種別は自動で設定される。優先度と期日は Issue Fields で持つ |
| ラベル | 時間とともに増えて散らかる | 18件の baseline を `.github/labels.yml` に宣言し、スクリプトで同期する |
| Pull Request | テンプレートなし、書きぶりにばらつき | ELI5、関連 Issue、設計判断、検証結果、残リスクの型があり、`review:` ラベルを1つ付ける |
| リポジトリ設定 | 画面で1つずつ設定し、付け忘れに気づけない | `.github/repo-baseline.yml` に宣言し、`scripts/apply-repo-settings` で適用する |
| default branch | 誰かが思い出すまで無防備 | `rulesets/default-branch.json` に ruleset を宣言する（PR 必須、チェック必須、force push と削除の禁止）。`scripts/apply-rulesets` で適用する |
| CI | リポジトリごとに組み立てる | baseline のチェックに加えて、GitHub Actions の静的検証（actionlint、zizmor、ghalint、pinact）が入る |
| 依存関係 | 手作業で更新する | Dependabot が週次で更新し、7日間の cooldown を置く。minor と patch はチェックが通れば自動マージする |
| 後からの baseline 変更 | セットアップを手でやり直す | `copier update` で生成先へ取り込める |

## 最短の始め方

Agent 向け：`gh` の認証が済んだシェルで、次のコマンドを順に実行してください。

```bash
# 1. 生成する（質問はリポジトリ名と説明の2つだけ）
copier copy gh:Hyd3-14/repo-template <dest>
cd <dest>

# 2. GitHub リポジトリを作って push する（既にある場合は飛ばす）
gh repo create <owner>/<repo> --public --source=. --push

# 3. baseline を GitHub 側へ適用する
python3 scripts/sync-labels --repo <owner>/<repo> --apply
python3 scripts/apply-repo-settings --repo <owner>/<repo> --apply
python3 scripts/apply-rulesets --repo <owner>/<repo> --apply

# 4. 検証する
./scripts/validate-template
python3 -m unittest discover -s scripts/tests
```

適用スクリプトはいずれも `--dry-run` で変更前に差分を表示できます。`apply-rulesets` は baseline の CI チェックがリポジトリに存在することが前提のため、最後に実行してください。

GitHub の **Use this template** ボタンでも作れますが、その場合は生成した瞬間のコピーで終わり、後からの baseline 変更は流れません。Copier で生成すると版が `.copier-answers.yml` に記録され、`copier update` で更新できます。

## 含まれるもの

- `AGENTS.md`、`.editorconfig`、`.gitattributes`、`.gitignore`
- 6種の Issue Forms と PR テンプレート（既定は日本語）
- ラベルの baseline と `scripts/sync-labels`
- リポジトリ設定の宣言と `scripts/apply-repo-settings`
- default branch の ruleset の宣言と `scripts/apply-rulesets`
- baseline CI、GitHub Actions の静的検証、Dependabot の設定
- `scripts/ci-changes`（文書だけの PR では重い job を省略する。判定できない場合は省略しない）と `scripts/docs-toc`（目次の生成と検査）
- 運用文書：仕様は `docs/operations/repo-baseline.md`、手作業が残る項目（Dependabot alerts、secrets など）は `docs/operations/manual-tasks.md`

## 管理場所

共通 base はこのリポジトリで管理します。特定のプロジェクトにだけ関係するものは、このリポジトリには入れず、そのプロジェクト側で管理します。

## 着想を得たもの

この baseline の型は、次から着想を得ています。

- Pull Request の書き方（短い要約でレビュワーが判断でき、量ではなく証拠で示す）は、[mattpocock/skills](https://github.com/mattpocock/skills) の `pr` Skill の考え方に沿っています。その Skill は HumanLayer の [show-me](https://github.com/humanlayer/skills) が元になっています
- レビュワー個人の頑張りではなく、テストや検査のような決まった仕組みで担保する方針は、pstack（poteto-mode）を使った経験から来ています
- 生成と更新には [Copier](https://copier.readthedocs.io/) を使い、baseline の変更は各リポジトリの手作業ではなくテンプレート側の変更として扱います
