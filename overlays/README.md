# Overlays

`overlays/`は、project typeごとに共通baseへ重ねる追加物を管理します。repositoryのrootが共通baseで、ここに置いたdirectoryは、必要なrepositoryだけが明示的に取り込みます。

`overlays/`自体は生成先へコピーしません。dotfilesの`repo-bootstrap`は、baseをコピーするときにこのdirectoryを除外し、profileで選んだoverlayだけをbaseの後に重ねます。profileとoverlayの対応は、機械可読な[`manifest.yml`](manifest.yml)で管理します。

## Overlay一覧

| overlay | 対象 | 追加するもの |
| --- | --- | --- |
| `app` | Web app、API、DB・認証・releaseを伴うrepository | 設計記録（ADR）、development・operations・postmortemの置き場所、release workflow、Node.jsとpnpmのcomposite action |
| `tooling` | CLI、library、script集 | usage、examples、scripts、軽量なrelease workflow |
| `security` | secret scanを追加したいrepository | secret scan workflow、gitleaks設定、security docs。単独でも適用できる |
| `dotfiles-public-safe` | 公開できるdotfiles | 共有する設定とlocal-onlyの状態の境界、dry-runを前提にしたinstall例。baseを重ねず単独で使う |

## 適用

dotfilesの`repo-bootstrap`を使います。既定はdry-runで、既存ファイルは上書きしません。

```sh
repo-bootstrap --target . --profile app --dry-run
repo-bootstrap --target . --profile app --apply
```

手動で適用する場合は、`overlays/`を除いたrootをコピーしてから、必要なoverlay directoryの中身を重ねます。

## 変更するとき

- 共通baseに入れるべきものをoverlayに置かない。逆に、ほぼ全repositoryで使うとは言えないものはbaseに置かず、overlayへ置く。
- overlayのworkflowも、rootの`AGENTS.md`にあるGitHub Actionsの規則（job単位の`permissions`と`timeout-minutes`、外部Actionのfull SHA固定、`persist-credentials: false`）に従う。
- profileやoverlayを追加・削除したら、[`manifest.yml`](manifest.yml)とdotfilesの`repo-bootstrap`を合わせて更新する。
