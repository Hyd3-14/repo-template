<h1 align="center">Hyd3 Repository Template</h1>

<p align="center">A <a href="https://copier.readthedocs.io/">Copier</a> template that gives a new GitHub repository a working baseline — issue and PR conventions, labels, repository settings, a branch ruleset, and CI checks — as files and scripts. Setup is one generation plus three apply commands, instead of an afternoon of clicking through Settings pages.</p>

<p align="center">English | <a href="README.ja.md">日本語</a></p>

## What you get

| Area | Starting from scratch | With this template |
| --- | --- | --- |
| Issues | Free-form titles, ad-hoc labels | Forms for 6 types; the type is set automatically on creation, and priority and dates live in Issue Fields |
| Labels | Whatever accumulates over time | An 18-label baseline declared in `.github/labels.yml` and synced by script |
| Pull requests | No template, uneven detail | A template with ELI5, linked issue, design notes, verification, and risk sections; one `review:` label per PR |
| Repository settings | Clicked through by hand, easy to miss one | Declared in `.github/repo-baseline.yml`, applied with `scripts/apply-repo-settings` |
| Default branch | Unprotected until someone remembers | A ruleset declared in `rulesets/default-branch.json` (PR required, status checks required, no force push, no deletion), applied with `scripts/apply-rulesets` |
| CI | Set up per repository | Baseline checks plus GitHub Actions static analysis (actionlint, zizmor, ghalint, pinact) |
| Dependencies | Manual updates | Dependabot weekly with a 7-day cooldown; minor and patch updates auto-merge when checks pass |
| Later baseline changes | Re-do the setup by hand | `copier update` pulls baseline changes into generated repositories |

## Quick start

For agents: run these commands in order, in a shell where `gh` is authenticated.

```bash
# 1. Generate (two questions: repository name and description)
copier copy gh:Hyd3-14/repo-template <dest>
cd <dest>

# 2. Create the GitHub repository and push (skip if it already exists)
gh repo create <owner>/<repo> --public --source=. --push

# 3. Apply the baseline to GitHub
python3 scripts/sync-labels --repo <owner>/<repo> --apply
python3 scripts/apply-repo-settings --repo <owner>/<repo> --apply
python3 scripts/apply-rulesets --repo <owner>/<repo> --apply

# 4. Verify
./scripts/validate-template
python3 -m unittest discover -s scripts/tests
```

Every apply script accepts `--dry-run` to show the diff before changing anything. Run `apply-rulesets` last: it requires the baseline CI checks to exist in the repository.

Full walkthrough — prerequisites, the existing-repository path, troubleshooting, and an instruction block you can hand to an AI agent: [docs/getting-started.md](../docs/getting-started.md).

GitHub's **Use this template** button also works, but it is a one-time copy and later baseline changes do not flow in. Copier records the template version in `.copier-answers.yml` and supports `copier update`.

## What is included

- `AGENTS.md`, `.editorconfig`, `.gitattributes`, `.gitignore`
- Issue Forms for 6 types and a PR template, Japanese by default
- The labels baseline and `scripts/sync-labels`
- The repository settings declaration and `scripts/apply-repo-settings`
- The default-branch ruleset declaration and `scripts/apply-rulesets`
- Baseline CI, GitHub Actions static checks, and Dependabot configuration
- `scripts/ci-changes` (skips heavy jobs for docs-only PRs, fail-closed) and `scripts/docs-toc` (generates and checks tables of contents)
- Operations docs: `docs/operations/repo-baseline.md` is the spec, and `docs/operations/manual-tasks.md` lists what stays manual (Dependabot alerts, secrets, and similar)

## Where things live

This repository is where the common base is maintained. Anything specific to a single project is kept with that project, not here. What belongs in the base and what does not is recorded in [docs/base-boundary.md](../docs/base-boundary.md).

## Influences

The conventions in this baseline did not appear from nowhere:

- The pull request style — a short brief a reviewer can judge quickly, backed by evidence rather than volume — follows the spirit of the `pr` skill in [mattpocock/skills](https://github.com/mattpocock/skills), which builds on HumanLayer's [show-me](https://github.com/humanlayer/skills) skill.
- The preference for deterministic checks (tests, linters, contract validation) over reviewer heroics comes from working with pstack (poteto-mode).
- Generation and later updates are handled by [Copier](https://copier.readthedocs.io/), so a baseline change is a template change, not a manual edit in every repository.
