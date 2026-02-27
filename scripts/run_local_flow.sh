#!/usr/bin/env bash
set -euo pipefail

PRODUCT_URL="${1:-https://shop.example.com/shoe-ultra-1}"
OUT_DIR="${2:-./artifacts}"

mkdir -p "$OUT_DIR"

echo "[1/4] running tests..."
python -m unittest discover -s tests -p "test_*.py"

echo "[2/4] module A plan..."
python -m ad_tool.cli plan "$PRODUCT_URL" --channel meta --budget 600 > "$OUT_DIR/plan.json"

echo "[3/4] module C creatives..."
python -m ad_tool.cli creative "轻薄跑鞋" --channel meta --sizes 1080x1080,1080x1920 --count 3 > "$OUT_DIR/creative.json"

echo "[4/4] full flow A->C->B..."
python -m ad_tool.cli flow "$PRODUCT_URL" --channel meta --budget 600 --use-ai-creatives --ai-creative-count 3 > "$OUT_DIR/flow.json"

echo "done. generated:"
ls -1 "$OUT_DIR"
