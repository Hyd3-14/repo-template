# Hyd3 Repository Template (English)

This directory contains the English human-facing variant of the common Hyd3 repository base. The Japanese files at the repository root are the default.

Copy these files to a generated repository when English is the preferred human-facing language:

- `README.md`
- `AGENTS.md`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/*.yml`
- `.github/PULL_REQUEST_TEMPLATE/default.md`
- `.github/pull_request_template.md`

Keep the root machine-readable configuration unchanged. Workflows, Dependabot, labels validation, and branch policy are shared rather than duplicated by locale.

Issue titles do not use type prefixes. Pull request titles use Conventional Commits by default, and branches use `<type>/<issue-number>-<short-summary>`.

Labels use the shared `type`, `priority`, and `area` axes. When migrating an existing repository, run `scripts/sync-labels` in dry-run mode first and pass explicit `--rename OLD=NEW` mappings so existing issue and pull request assignments are preserved.

Dependabot minor and patch updates may be auto-merged only after the `Dependabot auto-merge eligibility`, `Baseline static checks`, `Dependency Review`, and `GitHub Actions Static Checks` checks pass; major updates remain manual review and marking the pull request as draft keeps it on manual hold.

The shared baseline runs `actionlint` with ShellCheck integration, `zizmor`, `ghalint`, and `pinact` from `.github/workflows/github-actions-static-checks.yml`. Every job declares minimal `permissions` and `timeout-minutes`, external actions use full 40-character commit SHAs, and checkout uses `persist-credentials: false`. The pull-request-target triage workflow records a successful `Dependabot auto-merge eligibility` check only for minor and patch updates; the workflow-run path rechecks its latest result before auto-merge. Major updates remain manual review.
