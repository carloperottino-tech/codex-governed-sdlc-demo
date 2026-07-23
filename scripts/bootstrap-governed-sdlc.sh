#!/usr/bin/env bash
set -euo pipefail

MARKETPLACE_SOURCE="https://github.com/carloperottino-tech/codex-enterprise-plugin-marketplace"
MARKETPLACE_NAME="codex-enterprise-plugin-marketplace"
MARKETPLACE_REF="v0.1.0"
PLUGIN_NAME="governed-sdlc"
PLUGIN_VERSION="0.1.0"
PLUGIN_ID="${PLUGIN_NAME}@${MARKETPLACE_NAME}"
SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI is required." >&2
  exit 1
fi

echo "Adding ${MARKETPLACE_SOURCE} at immutable demo ref ${MARKETPLACE_REF}..."
codex plugin marketplace add "${MARKETPLACE_SOURCE}" --ref "${MARKETPLACE_REF}"

echo "Confirming ${PLUGIN_ID} advertises version ${PLUGIN_VERSION}..."
codex plugin list --marketplace "${MARKETPLACE_NAME}" --available --json |
  python3 "${SCRIPT_DIRECTORY}/verify_plugin_resolution.py" \
    --plugin-id "${PLUGIN_ID}" \
    --expected-version "${PLUGIN_VERSION}" \
    --allow-available

echo "Installing ${PLUGIN_ID}..."
codex plugin add "${PLUGIN_ID}"

echo "Verifying installed resolution..."
codex plugin list --marketplace "${MARKETPLACE_NAME}" --json |
  python3 "${SCRIPT_DIRECTORY}/verify_plugin_resolution.py" \
    --plugin-id "${PLUGIN_ID}" \
    --expected-version "${PLUGIN_VERSION}"

