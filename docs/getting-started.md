# Getting started

This page walks through adopting the baseline, either by hand or by handing the work to an AI agent. It assumes no prior knowledge of this template.

日本語版: [getting-started.ja.md](getting-started.ja.md)

## Prerequisites

- A GitHub repository to apply the baseline to (new or existing), with admin access
- `gh` (GitHub CLI) authenticated: `gh auth status` succeeds
- Python 3 (the helper scripts use only the standard library)
- [Copier](https://copier.readthedocs.io/) — only for creating a new repository from the template

## Let an agent do it

Copy the block below into your agent (Claude Code, Codex, or similar), replacing `OWNER/REPO` with your repository. The agent runs the same steps as the manual paths further down, and reports before it changes anything destructive.

```text
Set up the Hyd3-14/repo-template baseline for OWNER/REPO.

1. Clone https://github.com/Hyd3-14/repo-template and work from that clone.
   The scripts read the declarations locally and act on the repository given
   by --repo, so the target repository does not need the files yet.
2. Run `python3 scripts/check-baseline --repo OWNER/REPO` and show me the
   full result before changing anything.
3. Apply in this order, running each script with --dry-run first and
   showing me the output:
   - python3 scripts/sync-labels --repo OWNER/REPO --apply
   - python3 scripts/apply-repo-settings --repo OWNER/REPO --apply
   - python3 scripts/apply-rulesets --repo OWNER/REPO --apply
4. Stop and ask me before continuing if:
   - check-baseline prints a WARN about missing required checks (applying
     the ruleset then would block every merge), or
   - any dry-run proposes deleting labels (STALE lines in sync-labels).
5. Run check-baseline again and report the result. Every area must say OK.
```

## Path A: a new repository

```bash
copier copy gh:Hyd3-14/repo-template <dest>
cd <dest>
gh repo create <owner>/<repo> --public --source=. --push   # or --private
python3 scripts/sync-labels --repo <owner>/<repo> --apply
python3 scripts/apply-repo-settings --repo <owner>/<repo> --apply
python3 scripts/apply-rulesets --repo <owner>/<repo> --apply
python3 scripts/check-baseline --repo <owner>/<repo>
```

The last command must report every area as OK.

## Path B: an existing repository

The GitHub-side state (labels, repository settings, ruleset) can be applied from a clone of this template, without changing the target repository's files first:

```bash
git clone https://github.com/Hyd3-14/repo-template
cd repo-template
python3 scripts/check-baseline --repo <owner>/<repo>   # see where you stand
```

Read the report, then apply each area with `--apply` in the order labels, settings, ruleset — the same order as Path A. The file-side baseline (workflows, issue forms, PR template) is separate: generate it with Copier into a scratch directory and copy the files you want, or adopt the files gradually. `check-baseline` only reports the GitHub-side state.

## Troubleshooting

- **check-baseline warns about missing required checks.** The ruleset requires the `Baseline static checks` and `GitHub Actions Static Checks` workflows. If the target repository does not have them, do not apply the ruleset yet — every merge would block. Add the baseline workflows first (they ship with the template), or edit the declaration in `rulesets/default-branch.json` to match the checks the repository actually runs.
- **sync-labels shows STALE labels.** Those labels exist on GitHub but not in the baseline. `--apply` alone does not delete them. Deleting requires `--prune` and is a separate, explicit decision — check what the labels are attached to first.
- **Private repositories.** Labels, settings, and rulesets all work on private repositories, including on the GitHub Free plan. Features that need GitHub Advanced Security are not part of this baseline.
- **Dependabot auto-merge does nothing.** It depends on `allow_auto_merge`, which is part of the settings declaration. Run `apply-repo-settings` and confirm with `check-baseline`.
- **A script fails with an authentication error.** The scripts call `gh`. Run `gh auth status` and make sure the account has admin access to the target repository.
