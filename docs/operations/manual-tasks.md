# Manual Tasks

Repository files cannot complete every GitHub-side setup step.
Track manual work here so a newly generated repo is not considered production-ready before these items are handled.

## Initial GitHub Setup

- [ ] Confirm default branch is `main`.
- [ ] Enable Dependabot alerts.
- [ ] Enable Dependabot security updates.
- [ ] Enable secret scanning where available.
- [ ] Set GitHub Actions default workflow permissions to read-only.
- [ ] Confirm Actions can create and approve pull requests only if the repo intentionally allows it.
- [ ] Configure private vulnerability reporting or document the private security contact in `SECURITY.md`.

## Required Checks

After the first PR has run, confirm the exact check names and use them in rulesets or branch protection.

Recommended minimum:

- [ ] `Baseline static checks`
- [ ] `Dependency Review`

## Rulesets

The examples in `rulesets/` are intentionally disabled.

- [ ] Review `rulesets/default-branch.example.json`.
- [ ] Replace placeholder repository / target values if required by the import method.
- [ ] Add bypass actors for emergency maintainers.
- [ ] Add bypass actors for release automation or GitHub Apps when needed.
- [ ] Confirm required check names match actual workflow check names.
- [ ] Change `enforcement` from `disabled` to `active` only after the above is complete.
- [ ] Document any bypass actor and reason in `docs/operations/repo-baseline.md`.

## Secrets And Variables

Do not add placeholder secrets to repository files.
Create only the secrets that are actually required by generated repo workflows.

- [ ] List required secrets in the generated repo README.
- [ ] Create GitHub Actions secrets.
- [ ] Create environment-specific secrets if deployment environments are used.
- [ ] Record secret owners and rotation expectations in the generated repo's private operations notes.

## GitHub Apps

- [ ] Install required GitHub Apps, such as label sync or release automation.
- [ ] Restrict app permissions to the minimum needed.
- [ ] Add app bypass permissions to rulesets only when required.
- [ ] Record app purpose and maintainer in `docs/operations/repo-baseline.md`.

## Labels

`.github/labels/labels.yml` is declarative source data.

- [ ] Run `scripts/sync-labels --repo OWNER/REPO --dry-run`.
- [ ] Review create/update/stale output.
- [ ] Apply with `scripts/sync-labels --repo OWNER/REPO --apply` after confirming stale labels do not need deletion.

## Template Cleanup

For each generated repo:

- [ ] Replace README title and description.
- [ ] Replace issue template contact links.
- [ ] Remove unused Dependabot ecosystems.
- [ ] Add repo-specific validation commands.
- [ ] Add repo-specific deployment or release manual tasks.
