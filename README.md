# Guia Completo de Exercícios — produto low ticket

E-book em PDF com **152 exercícios ilustrados** em português brasileiro, organizados em 12 grupos
musculares, com fotos de execução (posição inicial e final), instruções passo a passo, ficha
técnica (músculo alvo, equipamento, nível, mecânica), QR codes com vídeos demonstrativos e
6 rotinas de treino prontas.

**PDF final:** [`dist/guia-completo-de-exercicios.pdf`](dist/guia-completo-de-exercicios.pdf) (~156 páginas, A4)

## Estrutura do repositório

```
content/
  exercicios.json        # 152 exercícios curados, 100% em PT-BR (fonte da verdade)
  capitulos/*.md         # capítulos introdutórios e rotinas (Markdown)
assets/
  images/                # 304 fotos (2 por exercício) — domínio público
  qrcodes/               # 152 QR codes (busca do exercício no YouTube)
scripts/
  curadoria.py           # pipeline: cruza os datasets, cura, copia fotos, monta o JSON
build/
  gerar_html.py          # monta build/guia.html a partir de content/
  build_pdf.sh           # HTML -> PDF via Chromium headless
design/
  PROMPT-DESIGN.md       # prompt pronto para redesenhar o produto com IA (Claude Designer)
dist/
  guia-completo-de-exercicios.pdf
```

## Como regenerar o PDF

```bash
bash build/build_pdf.sh
```

Requer Python 3 e Chromium (defina `CHROMIUM=/caminho/do/chrome` se necessário).
Para refazer a curadoria do zero: clone os datasets de origem e rode
`python3 scripts/curadoria.py <caminho-do-free-exercise-db>`, depois gere os QR codes
(`pip install qrcode pillow`).

## Para mudar o visual

Siga `design/PROMPT-DESIGN.md` — é um prompt completo de design editorial para usar com o Claude:
ele lê `content/exercicios.json` e os capítulos e devolve um novo HTML print-ready, que o
`build_pdf.sh` converte em PDF.

## Fontes e licenças

- **Fotos e dados-base dos exercícios:** [free-exercise-db](https://github.com/yuhonas/free-exercise-db)
  (Unlicense — domínio público, uso comercial livre).
- **Curadoria e taxonomia:** inspiradas em [exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset).
- **Texto em português (instruções, capítulos, rotinas):** conteúdo original deste repositório.
- O material tem caráter educacional e não substitui orientação profissional individualizada.
