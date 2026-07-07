# Guia Completo de Exercícios / Complete Exercise Guide — produto low ticket

E-book em PDF com **152 exercícios ilustrados**, organizados em 12 grupos musculares, com fotos de
execução (posição inicial e final), instruções passo a passo, ficha técnica (músculo alvo,
equipamento, nível, mecânica), QR codes com vídeos demonstrativos e 6 rotinas de treino prontas.
Disponível em **dois idiomas** (mesmo layout "Atlas de Treino"):

- 🇧🇷 **Português:** [`dist/guia-completo-de-exercicios.pdf`](dist/guia-completo-de-exercicios.pdf) (~176 páginas, A4)
- 🇺🇸 **English:** [`dist/complete-exercise-guide.pdf`](dist/complete-exercise-guide.pdf) (~176 pages, A4)

## Estrutura do repositório

```
content/
  exercicios.json        # 152 exercícios (fonte da verdade): campos PT + instrucoes_en/qrcode_en
  capitulos/*.md         # capítulos introdutórios e rotinas em PT (Markdown)
  capitulos-en/*.md      # mesmos capítulos em inglês
assets/
  images/                # 304 fotos (2 por exercício) — domínio público
  qrcodes/               # 152 QR codes PT (busca do exercício no YouTube em PT)
  qrcodes-en/            # 152 QR codes EN (busca em inglês)
scripts/
  curadoria.py           # pipeline: cruza os datasets, cura, copia fotos, monta o JSON
build/
  gerar_html.py          # monta o HTML a partir de content/ (aceita idioma: pt|en)
  build_pdf.sh           # HTML -> PDF via Chromium headless (pt, en ou ambos)
design/
  PROMPT-DESIGN.md       # prompt pronto para redesenhar o produto com IA (Claude Designer)
dist/
  guia-completo-de-exercicios.pdf   # PT
  complete-exercise-guide.pdf       # EN
```

## Como regenerar os PDFs

```bash
bash build/build_pdf.sh        # gera os dois idiomas
bash build/build_pdf.sh pt     # só português
bash build/build_pdf.sh en     # só inglês
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
- **Texto em inglês:** instruções dos exercícios do free-exercise-db (domínio público) + capítulos
  traduzidos do conteúdo original.
- O material tem caráter educacional e não substitui orientação profissional individualizada.
