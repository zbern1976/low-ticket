#!/usr/bin/env bash
# Gera os PDFs do e-book (PT e EN) a partir do HTML gerado.
# Uso:  bash build/build_pdf.sh        # gera ambos (pt e en)
#       bash build/build_pdf.sh pt      # só português
#       bash build/build_pdf.sh en      # só inglês
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
CHROMIUM="${CHROMIUM:-/opt/pw-browsers/chromium}"

render() {  # $1=lang  $2=html  $3=pdf
  python3 build/gerar_html.py "$1"
  "$CHROMIUM" --headless --disable-gpu --no-sandbox \
    --no-pdf-header-footer \
    --print-to-pdf="dist/$3" \
    "file://$PWD/build/$2" 2>/dev/null
  ls -lh "dist/$3"
}

LANG_ARG="${1:-both}"
case "$LANG_ARG" in
  pt)   render pt guia.html      guia-completo-de-exercicios.pdf ;;
  en)   render en guide-en.html  complete-exercise-guide.pdf ;;
  both) render pt guia.html      guia-completo-de-exercicios.pdf
        render en guide-en.html  complete-exercise-guide.pdf ;;
  *)    echo "uso: build_pdf.sh [pt|en|both]"; exit 1 ;;
esac
