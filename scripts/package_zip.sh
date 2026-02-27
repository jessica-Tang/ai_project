#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${1:-$PROJECT_ROOT/dist}"
ZIP_NAME="${2:-ai_ad_tool_preview.zip}"

mkdir -p "$OUT_DIR"
cd "$PROJECT_ROOT"

# Create a clean bundle for local run (exclude git metadata, caches, generated artifacts).
zip -r "$OUT_DIR/$ZIP_NAME" . \
  -x ".git/*" \
  -x "dist/*" \
  -x "artifacts/*" \
  -x "__pycache__/*" \
  -x "*/__pycache__/*" \
  -x "*.pyc"

echo "Created: $OUT_DIR/$ZIP_NAME"
