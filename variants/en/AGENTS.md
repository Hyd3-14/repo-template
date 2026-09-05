# AGENTS

This repository is the common Hyd3 repository base template. Remove unused scaffolding after creating a repository.

- Unless specified otherwise, write issues, pull requests, commit bodies, and docs in English for this variant.
- Do not commit secrets, credentials, personal information, sessions, history, caches, or other runtime state.
- Keep unrelated changes out, and do not overwrite, delete, or stage changes of unknown ownership.
- Declare minimal `permissions` and `timeout-minutes` for every GitHub Actions job, pin external actions to full commit SHAs, and use `persist-credentials: false` for checkout.
- Pass GitHub context values to shell scripts through step-level `env:` and quote those environment variables in the shell. Keep static action inputs in `with:`.
- Add repository-specific build, test, and release instructions in the generated repository.
- Run `./scripts/validate-template` and `git diff --check` after changes.
