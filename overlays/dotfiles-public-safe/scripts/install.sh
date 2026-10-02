#!/usr/bin/env bash

set -euo pipefail

dry_run=false

while (($# > 0)); do
  case "$1" in
    --dry-run)
      dry_run=true
      shift
      ;;
    --yes)
      shift
      ;;
    *)
      echo "unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [ "$dry_run" = true ]; then
  echo "[dry-run] install plan"
  echo "- link git/, zsh/, config/ into \$HOME"
  exit 0
fi

echo "implement symlink logic for your environment"
