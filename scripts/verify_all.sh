#!/bin/bash
# Lint and execute every notebook in order, in the verification venv. Stops at the first failure.
set -e
VENV=${VENV:-$HOME/venv/onboarding-mace}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
export MPLCONFIGDIR=${MPLCONFIGDIR:-${TMPDIR:-/tmp}/mpl}

# Module 03 falls back to cached files and overwrites its committed outputs when no key is set.
if [ -z "${MP_API_KEY:-}" ]; then
  echo "verify_all.sh: MP_API_KEY is not set. export MP_API_KEY first; module 03 needs it." >&2
  exit 1
fi

# Build the list with find, one path per entry, so a space in a path cannot split it.
NBS=()
while IFS= read -r -d '' nb; do
  NBS+=("$nb")
done < <(find "$ROOT/modules" "$ROOT/projects" -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*' -print0 | sort -z)

if [ "${#NBS[@]}" -eq 0 ]; then
  echo "verify_all.sh: no notebooks found under $ROOT/modules or $ROOT/projects" >&2
  exit 1
fi

echo "Linting ${#NBS[@]} notebooks"
"$VENV/bin/python" "$ROOT/scripts/check_notebook.py" "${NBS[@]}"

for nb in "${NBS[@]}"; do
  d=$(dirname "$nb"); f=$(basename "$nb")
  echo "== $f"
  ( cd "$d" && /usr/bin/time -p "$VENV/bin/jupyter" nbconvert --to notebook --execute --inplace \
      --ExecutePreprocessor.timeout=1800 --ExecutePreprocessor.kernel_name=python3 "$f" )
done
echo "all notebooks executed"
