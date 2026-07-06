#!/usr/bin/env bash
# Gera dist/guia-completo-de-exercicios.pdf a partir de build/guia.html
set -euo pipefail
cd "$(dirname "$0")/.."
python3 build/gerar_html.py
mkdir -p dist
CHROMIUM="${CHROMIUM:-/opt/pw-browsers/chromium}"
"$CHROMIUM" --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="dist/guia-completo-de-exercicios.pdf" \
  "file://$PWD/build/guia.html" 2>/dev/null
ls -lh dist/guia-completo-de-exercicios.pdf
