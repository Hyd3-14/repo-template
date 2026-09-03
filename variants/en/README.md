# Hyd3 Repository Template (English)

This directory contains the English human-facing variant of the common Hyd3 repository base. The Japanese files at the repository root are the default.

Copy these files to a generated repository when English is the preferred human-facing language:

- `README.md`
- `AGENTS.md`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/*.yml`
- `.github/PULL_REQUEST_TEMPLATE/default.md`

Keep the root machine-readable configuration unchanged. Workflows, Dependabot, labels validation, and branch policy are shared rather than duplicated by locale.

Issue titles do not use type prefixes. Pull request titles use Conventional Commits by default, and branches use `<type>/<issue-number>-<short-summary>`.
