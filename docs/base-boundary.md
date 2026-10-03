# baseとoverlayの境界

この文書は、`repo-template`のdefault baseに何を入れ、何を入れないかの判断基準と、現在の全ファイルの分類を記録します。目標は、repo-templateに余計なものを入れず、新規repositoryが必要最低限のものだけを取り出せる状態にすることです。

ファイルの移動や削除はこの文書では行いません。分類の合意後に、後続のIssueへ分けて進めます（#39）。

## baseの判断基準

次のすべてを満たすものだけをbaseに入れます。1つでも満たさない場合はoverlayへ移すか、template専用として生成先へ持ち込まないようにします。

1. **ほぼ全repositoryで使う**: app、tooling、docs、PoCのどれで作っても、生成直後から使う。
2. **無料の個人private repositoryで壊れない**: GitHub側の追加設定、Secret登録、有償機能、public限定機能がなくても、workflowとvalidationが失敗しない（#31）。
3. **本体実装より先の作業を要求しない**: 生成直後に必須の手動作業がない。推奨の設定は残してよいが、未実施でもCIが失敗しない。
4. **言語、package manager、配布形態を前提にしない**: Node.js、Docker、release、OSS公開などの前提を持ち込まない。
5. **生成先で書き換えても壊れない**: 生成先repositoryがlabelやIssue Formを足しても、base由来の検査が失敗しない。

迷った場合はbaseへ入れず、overlayにして必要なrepositoryだけが明示的に取り込みます。

## defaultへ入れないもの

- 特定の言語やpackage manager向けの設定（npm、Docker、Node.js向けignoreなど）
- public repositoryや有償機能でしか動かないworkflow（Dependency Reviewなど）
- 権限の強いtrigger（`pull_request_target`、`workflow_run`）を使う自動化
- GitHub側の追加設定（auto-merge、required checks、rulesetなど）を前提にする自動化
- template自身を保守するためのファイル（template向けREADME、LICENSE、template契約の検査など）
- 実利用のない言語variant

## 分類

PR #35（#31〜#34の対応）と#44（目次生成、review label、CIの省略判定）を適用した後の状態を対象にします。

| 区分 | 意味 |
| --- | --- |
| base | 生成先repositoryにそのまま残す |
| overlay | dotfilesの`templates/overlays/`へ移し、必要なrepositoryだけが`repo-bootstrap`で取り込む。repo-templateに置くと`Use this template`で生成先へ入るため、このrepositoryには置かない |
| template専用 | repo-template自身の保守に使い、生成先へ持ち込まない |
| 削除 | 必要な内容を他の場所へ移したうえで削除する |

### base

| ファイル | 理由・補足 |
| --- | --- |
| `AGENTS.md` | どのrepositoryでもagentへの常時指示が必要 |
| `.editorconfig`、`.gitattributes` | 言語に依存しない |
| `.gitignore` | `.env`系とOS固有ファイルだけを残す。`node_modules/`、`dist/`、`.next/`などNode.js向けの行は`app` overlayへ移す |
| `.github/ISSUE_TEMPLATE/*.yml`（6 Formと`config.yml`） | Issue Formは全repositoryで必須 |
| `.github/PULL_REQUEST_TEMPLATE/default.md`、`.github/pull_request_template.md` | PR templateは全repositoryで必須 |
| `.github/labels.yml`、`scripts/sync-labels`、`.github/workflows/sync-labels.yml` | labelsは全repositoryで必須。同期workflowは`GITHUB_TOKEN`だけで動く |
| `.github/hyd3-baseline.yml` | dotfilesの`repo-preflight`がprofile判定に使う |
| `.github/dependabot.yml` | `github-actions`のupdaterだけを残す。npmとdockerのupdaterは`app` overlayへ移す |
| `.github/workflows/ci.yml` | 残す。ただし生成先のbaselineを検査する部分だけにし、template契約の検査（`scripts/validate-template`の呼び出し）を外す |
| `scripts/docs-toc`、`scripts/docs-toc-targets.json` | Python標準ライブラリだけで動き、言語に依存しない。対象一覧はrepo-template自身の文書を指しているので、生成先で書き換える（基準5） |
| `scripts/ci-changes` | GitHub側の追加設定なしに動き、未知のpathは必ず検証するので、生成先で重いjobを足しても検証を誤って省かない |

### overlay

| ファイル | 移動先 | 理由 |
| --- | --- | --- |
| `.github/workflows/dependabot-triage.yml`、`.github/workflows/automerge-dependabot.yml` | Dependabot自動化用のoverlay（新設） | `pull_request_target`と`workflow_run`を使い、auto-mergeとrequired checksのGitHub設定を前提にする（基準2、3） |
| `.github/workflows/github-actions-static-checks.yml` | `security` | zizmor、ghalint、pinactはworkflowを多く持つrepository向けのhardening。pinactはGitHub APIの認証も要る（基準1、3）。actionlintだけはbaseのCIに残す |
| `SECURITY.md` | `security`、またはpublic公開用のoverlay | private vulnerability reportingはpublic repository向けの導線（基準2） |

### template専用

| ファイル | 理由 |
| --- | --- |
| `README.md`（現在の内容） | repo-template自身の説明になっている。生成先には別の短いREADME skeletonを渡す |
| `LICENSE` | repo-template自身の公開用。生成先のprivate repositoryへMIT licenseが意図せず引き継がれる |
| `scripts/validate-template` | label集合やIssue Formの数を固定で検査するため、生成先で足すと失敗する（基準5） |
| `docs/operations/repo-baseline.md` | Hyd3 baseline全体の説明。正本はdotfilesの`docs/repository-baseline.md` |
| `rulesets/default-branch.example.json` | 参考例。rulesetの適用は生成直後の必須作業にしない |
| `docs/base-boundary.md`（この文書） | template保守用の判断基準 |
| `scripts/tests/`（`helpers.py`、`test_docs_toc.py`、`test_ci_changes.py`） | baseに残すhelperそのものの回帰test。生成先ではhelperを変更しない限り不要 |

### 削除

| ファイル | 移す先 |
| --- | --- |
| `docs/operations/manual-tasks.md` | overlay固有の確認項目は各overlayのdocsへ移す。baseで推奨として残す項目（Actionsのdefault token permissionをread-onlyにするなど）は、生成先README skeletonの短い節へ移す |

## 追加候補との関係

Issue #41 で検討している次の3点は、上の判断基準を満たす限りbaseへ入れてよいものとして扱います。

- **miseによるtool・task管理**: task名だけを共通にし、中身を言語に依存させなければ基準4を満たす。
- **secret content scan**: licenseやGitHub側の設定なしにCLIで動かせば基準2を満たす。
- **`CLAUDE.md`**: `AGENTS.md`を参照するだけなら全repositoryで使え、追加作業もない。

## 既存repositoryの移行方針

- 既存の生成先repositoryへは一括同期しない。各repositoryに手を入れる機会に、dotfilesの`repo-preflight`の結果を見て段階的に追従する。
- overlayへ移したファイルが既存repositoryに残っていても失敗扱いにしない。dotfilesの`repo-preflight`と`repo-bootstrap`は、baseから外したファイルを必須として扱わないよう追従させる。
- ファイルを移すときは、移動先のoverlayへ追加する変更を、baseから外す変更より先にmergeする。overlayから取り込めない期間を作らない。

## 後続の作業

分類の合意後、次の単位でIssueへ分けます。

1. Dependabot自動化をoverlayへ移す（repo-template、dotfiles）。
2. Actions静的検査のzizmor、ghalint、pinactを`security` overlayへ移し、actionlintをbaseのCIへ残す。
3. template専用ファイルを生成先へ持ち込まない仕組みを作り、生成先向けのREADME skeletonを用意する（#32 の残り）。
4. `.github/dependabot.yml`と`.gitignore`の言語固有部分を`app` overlayへ移す。
5. `docs/operations/manual-tasks.md`を解体し、CIからtemplate契約の検査を外す。
6. dotfilesの`repo-bootstrap`、`repo-preflight`、`templates/overlays/`を新しい境界へ追従させる。
