# Repository Baseline

This document records the baseline assumptions for a Hyd3 repository generated from this template.
Keep it short and operational.

## Metadata

- Repository: `Hyd3-14/repo-template`
- Visibility: public
- Default branch: `main`
- Template status: baseline template
- Last baseline review: 2026-05-19

## Baseline Scope

Included:

- Public repo safety guidelines in `AGENTS.md`
- Security policy in `SECURITY.md`
- Issue and pull request templates
- Dependabot configuration for GitHub Actions, npm, and Docker ecosystems
- Baseline CI with repository structure and obvious secret filename checks
- Dependency review workflow
- Dependabot triage and guarded automerge workflows
- Declarative labels file
- Disabled ruleset example
- Manual task tracking

Not included:

- Repo-specific build, test, release, or deployment commands
- GitHub-side secrets, variables, environments, and app installs
- Active branch protection or active rulesets
- Language-specific linting beyond baseline repository checks

## Required Checks

Use the exact check names reported by GitHub after the first PR run.

Initial expected checks:

- `Baseline static checks`
- `Dependency Review`

These names are provisional until the first PR reports the exact GitHub check names.
Do not activate required check rules before confirming the names in GitHub.

## Dependabot Policy

- Minor and patch updates may be grouped and eligible for guarded automerge.
- Major updates are labeled `60: deps/major` and `30: status/needs-human-review`.
- Major updates must not be auto-closed by default.
- Ecosystems that do not apply to a generated repo should be removed from `.github/dependabot.yml`.

## Automerge Policy

Automerge is allowed only for Dependabot minor / patch PRs after required checks succeed.
Human-authored PRs and major updates require maintainer review.

## Label Policy

- Label names use `NN: group/name`.
- Descriptions are written in Japanese so maintainers and agents can choose labels consistently.
- Number prefixes define list order; colors are assigned by meaning, not by prefix.
- Issues and PRs should have at least one `10: type/*` label.
- Use `00: needs-triage` when the correct type, area, priority, or next action is unclear.

## Ruleset Policy

Ruleset examples are disabled by default.
The default branch ruleset is tuned for personal, AI-assisted repositories:

- Linear history is required.
- Required approval count is `0`.
- Required status checks remain strict.
- Last-push approval is disabled.

Before activation:

- Confirm required check names.
- Configure bypass actors.
- Confirm release automation requirements.
- Test with a non-critical PR.

## Manual Work

Manual setup lives in `docs/operations/manual-tasks.md`.
Do not mark a generated repo as ready until required GitHub-side tasks are complete.

## Baseline Review Log

| Date | Reviewer | Notes |
| --- | --- | --- |
| 2026-05-19 | Codex | Initial public template baseline. |
