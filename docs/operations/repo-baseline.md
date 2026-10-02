# Repository Baseline

この文書は、`repo-template`から生成するHyd3 repositoryの共通前提を記録します。生成先repo固有の運用はここへ大量に戻さず、そのrepoのdocsへ追加してください。

<!-- START docs-toc -->

**目次**

- [責務](#%E8%B2%AC%E5%8B%99)
- [共通仕様](#%E5%85%B1%E9%80%9A%E4%BB%95%E6%A7%98)
- [GitHub Actions baseline](#github-actions-baseline)
- [Labels](#labels)
  - [レビュー要求label](#%E3%83%AC%E3%83%93%E3%83%A5%E3%83%BC%E8%A6%81%E6%B1%82label)
- [文書の目次](#%E6%96%87%E6%9B%B8%E3%81%AE%E7%9B%AE%E6%AC%A1)
- [CIの省略判定](#ci%E3%81%AE%E7%9C%81%E7%95%A5%E5%88%A4%E5%AE%9A)
- [Required files](#required-files)
- [検証](#%E6%A4%9C%E8%A8%BC)
- [GitHub側で残る設定](#github%E5%81%B4%E3%81%A7%E6%AE%8B%E3%82%8B%E8%A8%AD%E5%AE%9A)

<!-- END docs-toc -->

## 責務

- `repo-template`: README、軽量AGENTS、Issue Forms、PR template、labels、CI、Dependabotなど共通baseの正本。
- `repo-template/overlays/`: `app`、`tooling`、`security`、`dotfiles-public-safe`などproject type固有overlayの管理元。生成先へはbaseとしてコピーせず、profileで選んだものだけを重ねる（[`overlays/README.md`](../../overlays/README.md)）。
- `dotfiles`: repo-preflight、repo-bootstrap、branch検査、publish workflow、drift検査など運用仕様と実行ロジックの正本。

## 共通仕様

- Issue titleには種別prefixを付けず、`type: bug`、`type: feature`、`type: chore`などのlabelで分類する。
- PR titleは原則Conventional Commits形式とする。
- PR本文は`関連Issue`、`概要`、`変更点`、`動作確認`、`補足`の軽量構成とする。
- branchは`<type>/<issue-number>-<short-summary>`とする。
- label nameは英語、descriptionは日本語とし、`type:`、`priority:`、`area:`、`status:`、`review:`の5軸を使う。
- `type:`はIssueの種別、`priority:`は対応優先度、`area:`は主な対象領域、`status:`は現在のライフサイクル状態、`review:`はPRに必要な人間のレビュー行動を表す。
- 原則として`type:`は1つ、`priority:`は必要なIssueだけ、`area:`は主対象を1つ付与する。横断Issueでは`area:`を複数付与してよい。`status:`は必要なIssueに最大1つ付与し、状態遷移時は付け替える。`review:`はPRに1つ付与する。
- Dependabotは`github-actions`、`npm`、`docker`をweeklyで更新し、minor/patchをgroupingする。更新には7日間のcooldownを設け、majorは人間レビューとする。
- Dependabotのminor/patch更新は、`Dependabot auto-merge eligibility`と、`Baseline static checks`、`GitHub Actions Static Checks`が成功し、非draftの同一repository PRである場合だけ自動マージ対象とする。PRのdraft状態は手動保留の手段として維持する。

## GitHub Actions baseline

`.github/workflows/github-actions-static-checks.yml`は、`actionlint`（ShellCheck連携）、`zizmor`、`ghalint`、`pinact`を検証します。`actionlint`成功後、後3者を並列に実行し、集約jobで結果を1つのrequired checkへまとめます。

全workflowでは、次の規約を共通baselineとします。

- 各jobに必要最小限の`permissions`と合理的な`timeout-minutes`を明示する。
- 外部Actionとreusable workflowはfull 40-character commit SHAへ固定し、SHA横のversion annotationを維持する。
- `actions/checkout`では`persist-credentials: false`を指定する。
- secretをworkflow/job-level `env`へ広げず、必要なstepの`with`またはstep-level `env`へ限定する。
- GitHub contextの値をshellへ渡す場合はstep-level `env`を介し、shell内では環境変数をquoteする。静的なAction inputは`with`に置く。

Dependabotのmetadata取得・label付与とrequired check後のauto-mergeには、repository tokenでのAPI操作が必要なため`pull_request_target`と`workflow_run`を使います。metadata取得は`pull_request_target`側で行い、minor/patchだけ`Dependabot auto-merge eligibility` checkを成功させます。`workflow_run`側は`branches` filterを使わず、解決したPRのbase branch、repository、author、draft状態、同checkの最新結果、required checksをAPIで再確認します。これらのworkflowはPR codeをcheckoutせず、`pull_request_target`の対象branchを`main`へ限定し、zizmorの`dangerous-triggers`に対する局所ignoreへ理由を記録しています。新しい特権処理をこの経路へ追加する場合は、別途セキュリティレビューが必要です。

## Labels

`.github/labels.yml`が宣言上の正本です。共通baselineは次の22 labelsです。

- `type: feature`、`type: bug`、`type: chore`、`type: documentation`、`type: test`、`type: security`
- `priority: P0`、`priority: P1`、`priority: P2`
- `area: app`、`area: database`、`area: dependency`、`area: devex`、`area: ci`、`area: deployment`
- `status: needs-discussion`、`status: ready`、`status: in-progress`、`status: blocked`
- `review: routine`、`review: human`、`review: decision`

既存labelを移行する場合は、共通scriptへrepo固有の対応表を埋め込まず、対象repoの実行時に`--rename OLD=NEW`を明示します。GitHub APIの改称を使うため、既存Issue/PRへの付与を保ったまま移行できます。削除を伴う場合は、先にdry-runで差分と利用状況を確認してください。

`status:`はOpen Issueの必須項目にはせず、相談待ち・着手可能・作業中・ブロック中を検索したい場合に使います。完了はGitHub IssueのOpen/Closedを正本とし、`status: done`や`status: closed`は追加しません。GitHub ProjectsのStatusを本格運用する場合は、二重管理コストを評価し、Project側を正本にする選択肢を残します。

### レビュー要求label

`review:*` labelは、そのPRに対してレビュワーが次に取る行動を表します。`type:*`や`area:*`が変更の種類・領域を表すのに対し、`review:*`は「人間が見る必要があるか」「人間の意思決定を待つ必要があるか」をPR一覧から判別するために使います。

PR作成者またはAI Agentは、PR作成時に変更内容と関連Issueを確認し、次のいずれか1つを付けます。

| label | 意味 | 代表例 |
| --- | --- | --- |
| `review: routine` | 通常のCI・レビュー手順で進められ、個別の人間判断を必須としない | 誤字修正、既存方針に沿ったpatch / minorの依存更新、挙動を変えないtestや文書の追加 |
| `review: human` | merge前に人間による内容確認が必要 | 画面や外部から見える挙動の変更、開発フロー・hook・CI・Agent向け指示の変更、DB migration、既存仕様に沿った認証・認可の変更 |
| `review: decision` | 仕様・権限・運用・Production等の意思決定が確定するまでmergeしない | 未確定の仕様、権限や役割の新設・変更、データの保持・削除の決定、Production・deploy・secret運用の変更 |

分類では次を守ります。

- 1つのPRに`review:*`を複数付けない。複数に当てはまる場合は、より上位（`routine` < `human` < `decision`）の1つだけを付ける。
- `review:*`が付いていないPRを`review: routine`とみなさない。未設定は分類漏れとして扱い、気づいた人が分類する。
- 次の領域を含むPRは`review: routine`にしない。既存仕様の範囲内なら`review: human`以上、新しい判断を含むなら`review: decision`にする。
  - 認証・認可、権限・役割
  - DB schema、migration、seed
  - Production、deploy、secret、credentialの扱い
  - 主要な開発フロー（Git hook、CI、PR・レビュー手順、`AGENTS.md`、Agent向けSkill）、大きな依存・frameworkの変更
- 変更ファイルの種類だけで`review: routine`へ格下げしない。上位への引き上げは、作成者・レビュワー・AI Agentの誰でもいつでも行える。引き下げる場合は、理由をPRに記載する。

人間による確認や判断が必要なPRは、GitHubのPR一覧で次のように検索できます。

```text
is:pr is:open label:"review: human"
is:pr is:open label:"review: decision"
is:pr is:open -label:"review: routine" -label:"review: human" -label:"review: decision"
```

最後の検索は、分類漏れのPRを見つけるために使います。`review:*`はレビュー要求だけを表し、merge可能かどうかの判定、AIレビューの実行、GitHub ProjectsのStatusによる工程管理は担いません。

## 文書の目次

長いMarkdownには、見出しから生成した目次を置きます。`scripts/docs-toc-targets.json`へ対象文書を追加し、文書のタイトル見出しの後に次のmarkerを1組置いてから`./scripts/docs-toc`を実行します。

```markdown
<!-- START docs-toc -->
<!-- END docs-toc -->
```

- 目次には第2・第3階層の見出しを含めます。既存文書が第1階層で章を分けている場合は、対象に`"includeTopLevelSections": true`を指定します。
- anchorはGitHubの見出しIDと同じ規則で計算し、同名見出しの番号には目次に出さない見出しも数えます。コードブロック内の見出しは無視します。
- `./scripts/docs-toc --check`は書き換えずに更新漏れを検出し、Baseline CIで実行します。見出しを変えたら`./scripts/docs-toc`で再生成してください。
- 生成はPython標準libraryだけで行い、Node.jsなどの追加依存を要求しません。

## CIの省略判定

`scripts/ci-changes`は、PRの変更pathから重い検証jobを省略できるかを判定し、`run_heavy`を出力します。Baseline CIの`changes` jobが実行し、判定結果と理由をjob summaryに記録します。共通baseの`Baseline static checks`は軽いため、常に実行します。

- 省略を許可するのは、検証結果に影響しないと確認したpathだけです（README等の文書、`docs/**/*.md`、Issue Form、PR template、`.github/labels.yml`）。
- 許可一覧にないpath、renameの元path、PR以外のevent、SHAの不足、差分取得の失敗では、必ず`run_heavy=true`にします。
- 生成先repoでbuild、test、E2Eなどの重いjobを追加する場合は、`needs: changes`と`if: needs.changes.outputs.run_heavy == 'true'`を付けます。`if`で省略したjobはskippedとなり、required checkを満たします。
- 生成先repoで文書から検証対象を生成する場合など、文書変更が検証結果に影響するなら、許可一覧から外してください。

## Required files

- `README.md`
- `AGENTS.md`
- `SECURITY.md`
- `.editorconfig`
- `.gitattributes`
- `.gitignore`
- `.github/hyd3-baseline.yml`
- `.github/labels.yml`
- `.github/ISSUE_TEMPLATE/bug.yml`
- `.github/ISSUE_TEMPLATE/feature.yml`
- `.github/ISSUE_TEMPLATE/chore.yml`
- `.github/PULL_REQUEST_TEMPLATE/default.md`（canonical）
- `.github/pull_request_template.md`（GitHub自動読み込み用。canonicalと同一内容）
- `.github/workflows/ci.yml`
- `.github/workflows/dependabot-triage.yml`
- `.github/workflows/automerge-dependabot.yml`
- `.github/workflows/github-actions-static-checks.yml`
- `scripts/ci-changes`
- `scripts/docs-toc`
- `scripts/docs-toc-targets.json`

## 検証

```sh
./scripts/validate-template
python3 -m unittest discover -s scripts/tests
./scripts/docs-toc --check
git diff --check
actionlint
shellcheck scripts/validate-template
ghalint run
zizmor --collect=all .
pinact run --check --verify-comment
```

`pinact`はversion annotationの検証時にGitHub APIを使うため、必要に応じてstep-levelの`GITHUB_TOKEN`またはローカルの認証済み環境を用意します。生成先repoでは、上記CLIを利用可能なversion固定済みの開発環境へ組み込んでください。

dotfiles側の`repo-preflight --agent`とcross-repo drift検査は、生成先repoへ必要な場合だけ適用します。

## GitHub側で残る設定

branch protectionまたはruleset、required checks、Dependabot alerts、secret scanning、private vulnerability reporting、secrets、GitHub App権限はファイルから自動適用しません。共通baseは追加のGitHub Code Security / Advanced Security機能を要求せず、Dependency Reviewなど利用条件のあるcheckは生成先repoでoptionalに追加します。`manual-tasks.md`に確認項目を残します。
