# Security Policy

## Supported Versions

Only the latest state of the default branch is supported.

| Version | Supported |
| --- | --- |
| default branch | Yes |

## Reporting a Vulnerability

If you find a vulnerability or suspect that secrets have been
committed, please do not open a public issue with the details.
Use GitHub's private vulnerability reporting (Security Advisories)
for this repository instead.

## Response

- After a report is received, we confirm the impact and the
  reproduction conditions.
- If secrets are involved, rotation and history cleanup take
  priority.
- Fixes are kept to the necessary scope and add verification to
  prevent recurrence.
- Disclosure happens after a fix or mitigation is ready.

## Baseline

- GitHub Actions token permissions are minimized per job.
- Third-party actions are pinned to fixed versions; floating
  refs are avoided.
- Dependabot alerts are enabled.
- Secrets, tokens, credentials, sessions, history, logs, and
  caches are never committed.
