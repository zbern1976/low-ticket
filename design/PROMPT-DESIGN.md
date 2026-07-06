# Prompt de Design — Guia Completo de Exercícios

> Copie o prompt abaixo (entre as linhas ---) e cole no Claude (ou em qualquer ferramenta de design
> com IA). Anexe junto os arquivos `content/exercicios.json` e `content/capitulos/*.md` deste
> repositório — eles são o conteúdo real do produto. O prompt foi escrito para gerar um HTML
> print-ready A4 que pode ser convertido em PDF com `build/build_pdf.sh`.

---

Você é um designer editorial sênior especializado em e-books e infoprodutos fitness. Sua tarefa é
criar o design completo de um e-book em PDF chamado **"Guia Completo de Exercícios"** — um produto
digital low ticket em português brasileiro com 152 exercícios ilustrados, 5 capítulos introdutórios
e 6 rotinas de treino prontas.

## 1. Conteúdo (não invente — use os arquivos anexados)

- `exercicios.json`: lista de 152 exercícios. Campos por exercício: `nome`, `nome_original`,
  `grupo_titulo` (capítulo), `musculo_alvo`, `musculos_secundarios`, `equipamento`, `nivel`,
  `mecanica`, `imagens` (2 fotos: posição inicial e final), `qrcode` (PNG do QR),
  `video_url` e `instrucoes` (passos numerados em PT-BR).
- `capitulos/*.md`: boas-vindas e modo de uso, princípios de treino, aquecimento e segurança,
  e rotinas prontas (com tabelas).
- Não altere o texto do conteúdo; seu trabalho é apresentação, hierarquia e identidade visual.

## 2. Identidade visual

- **Personalidade:** energética, confiável, direta — "personal trainer profissional", nunca
  infantil nem genérica de clipart.
- **Paleta:** fundo claro (branco/off-white #FAFAF8) para economizar tinta e manter legibilidade;
  1 cor de ação quente (laranja #E8590C ou vermelho-coral) usada com disciplina em títulos de
  capítulo, chips de músculo alvo e detalhes; 1 tom escuro para texto (#1A1D21); cinzas neutros
  para metadados. Contraste mínimo WCAG AA em todo texto.
- **Tipografia:** título display bold condensado (peso 700–800) para capa e aberturas de capítulo;
  sans humanista legível para corpo (10–11 pt); use no máximo 2 famílias. Hierarquia clara:
  capa > divisor de capítulo > nome do exercício > passos > metadados.
- **Grid:** A4 (210×297 mm), margens ≥ 14 mm, grid de 12 colunas; respiro generoso — páginas
  densas vendem mal em preview.

## 3. Anatomia das páginas (obrigatória)

1. **Capa:** título, subtítulo com promessa ("152 exercícios ilustrados…"), 4 números de destaque
   (152 exercícios / 12 grupos / 10 equipamentos / 6 rotinas). Sem imagens de banco genéricas.
2. **Sumário:** capítulos numerados com contagem de exercícios por grupo.
3. **Capítulos introdutórios:** texto dos .md com blocos de destaque para avisos e dicas
   (blockquotes viram caixas coloridas), tabelas de rotina estilizadas com linhas zebradas.
4. **Divisor de capítulo (1 página por grupo muscular):** número grande decorativo, nome do
   grupo, resumo e lista dos exercícios do capítulo em 2 colunas.
5. **Ficha de exercício (1 por página, 152×):**
   - Nome PT grande + nome original discreto abaixo;
   - Chips/etiquetas: músculo alvo (destacado), equipamento, nível, mecânica, auxiliares;
   - As 2 fotos lado a lado com mesma altura (início → fim; se quiser, seta entre elas);
   - Passos numerados com números destacados na cor de ação;
   - QR code (~24 mm) no canto com legenda "Aponte a câmera para ver vídeos" + URL curta;
   - Rodapé com nome do capítulo e numeração de página.
6. **Índice por equipamento** ao final, em 2 colunas.

## 4. Regras técnicas de saída

- Gere **um único arquivo HTML** com CSS embutido, pronto para impressão:
  `@page { size: A4; margin: … }`, `page-break-after` nos blocos de página,
  `break-inside: avoid` nas fichas; caminhos de imagem relativos exatamente como estão no JSON
  (`assets/images/...`, `assets/qrcodes/...`).
- Nada de JavaScript, fontes externas de CDN ou imagens remotas — o PDF é gerado offline com
  Chromium headless (`build/build_pdf.sh`).
- Se gerar o HTML por script (recomendado, são 152 fichas), escreva um script Python único que
  leia o JSON e os .md — use `build/gerar_html.py` deste repositório como referência de estrutura.

## 5. Critérios de qualidade (cheque antes de entregar)

- [ ] Nenhuma ficha quebrada no meio entre páginas;
- [ ] Fotos sempre no par início/fim, nunca distorcidas (use object-fit);
- [ ] Texto 100% em PT-BR, sem placeholder ou lorem ipsum;
- [ ] A cor de ação aparece em TODAS as páginas (consistência de marca), mas nunca em mais de
      ~10% da área da página;
- [ ] Capa legível em miniatura de 200 px (teste: é o thumbnail da página de vendas);
- [ ] QR codes com zona de silêncio (borda branca) preservada e tamanho ≥ 20 mm;
- [ ] Aviso legal presente (educacional, não substitui profissional) no início ou fim.

## 6. Entregáveis

1. O HTML final (ou script gerador + HTML);
2. Uma prévia da capa e de 1 ficha de exercício;
3. Lista das decisões de design tomadas (paleta final, fontes, espaçamentos) em 10 linhas.

---

## Dicas de uso

- **Iterar:** peça variações só da capa primeiro ("gere 3 direções de capa e me mostre"), escolha
  uma, depois aplique ao resto — capa é o que vende.
- **Trocar a paleta:** substitua o laranja pela cor da sua marca no prompt antes de enviar.
- **Regerar o PDF:** depois de substituir `build/guia.html` pelo HTML novo, rode
  `bash build/build_pdf.sh` (requer Chromium; em outra máquina, aponte a variável `CHROMIUM`
  para o executável do Chrome/Chromium).
