# Prompt de Design — Guia Completo de Exercícios

> **Como usar:** copie o prompt abaixo (entre as linhas ---) e cole no **Claude Designer em modo
> Document** (ou em qualquer ferramenta de design com IA). Anexe junto os arquivos
> `content/exercicios.json` e `content/capitulos/*.md` deste repositório — eles são o conteúdo
> real do produto. O prompt pede um HTML print-ready A4 que o `build/build_pdf.sh` converte em PDF.
>
> O prompt segue um protocolo em etapas: primeiro 3 direções de capa, depois 1 divisor + 1 ficha,
> e só então o documento completo — aprove cada etapa antes de deixar seguir.

---

Você é diretor de arte editorial sênior, com 20 anos desenhando revistas esportivas premium
(Men's Health, Runner's World) e best-sellers de fitness. Você domina design print, tipografia
editorial e a psicologia visual que faz um infoproduto parecer caro. Sua missão: transformar o
conteúdo anexado no e-book de exercícios **mais bonito e profissional do mercado brasileiro** —
um PDF que, só pelo preview da capa e de 2 páginas internas, justifique a compra imediata.

## O PRODUTO

**"Guia Completo de Exercícios"** — e-book A4 em português brasileiro: 152 exercícios ilustrados
em 12 grupos musculares, 4 capítulos introdutórios e 6 rotinas de treino prontas. Público:
brasileiros de 18–45 anos que treinam em casa ou academia, compraram por impulso num preço baixo
e precisam sentir que levaram MUITO mais do que pagaram.

## CONCEITO CRIATIVO: "ATLAS DE TREINO"

Trate o e-book como um atlas esportivo de colecionador, não como apostila. Referências: pôster de
recorde olímpico, tabela periódica, manual técnico da NASA. Cada ficha de exercício é uma "carta
técnica" padronizada e colecionável. A sensação ao folhear: precisão, força, sistema. Nada de
clipart, gradientes arco-íris, sombras exageradas ou estética de PowerPoint.

## DESIGN TOKENS (use exatamente estes valores)

- **Papel:** #FAFAF8 (off-white). Nunca fundo escuro em páginas de conteúdo (tinta e legibilidade).
- **Tinta:** #16181D (texto), #5C636B (metadados), #E4E1DB (linhas/bordas).
- **Cor de ação:** #E8590C (laranja queimado). Regra de disciplina: presente em 100% das páginas,
  ocupando no máximo 10% da área de cada uma. Variações permitidas: #C14A00 (escuro) e
  #FFEDE0 (tint de fundo para caixas).
- **Exceção dramática:** a CAPA e os 12 DIVISORES de capítulo podem inverter — fundo #16181D com
  tipografia gigante em off-white + laranja. É o contraste entre divisores escuros e miolo claro
  que dá ritmo de "capítulos de atlas".
- **Tipografia (máx. 2 famílias, system-safe ou embutidas — sem CDN):** display condensado bold
  700–800 (estilo Archivo Black / Oswald) para capa, divisores e nomes de exercício; sans
  humanista (estilo Inter / Source Sans) para corpo. Escala: capa 44–60 pt · divisor 30–36 pt ·
  nome de exercício 16–18 pt · corpo 10–10,5 pt · metadados 7,5–8,5 pt em caps com tracking +8%.
- **Grid:** A4 210×297 mm, margens 16 mm, 12 colunas, respiro generoso. Página densa = página
  que não vende.

## ANATOMIA DAS PÁGINAS (obrigatória, nesta ordem)

**1. CAPA (fundo escuro #16181D)** — título em tipografia gigante condensada, quebrado em 2–3
linhas com "EXERCÍCIOS" em laranja; subtítulo-promessa ("152 exercícios ilustrados com fotos,
passo a passo e vídeos — para treinar em casa ou na academia"); régua horizontal com os 4
números-troféu: 152 exercícios · 12 grupos · 10 equipamentos · 6 rotinas; um elemento gráfico
técnico sutil (grid fino, crosshair, linhas de blueprint) — NUNCA foto de banco de imagem.
Teste do thumbnail: legível a 200 px de largura.

**2. SUMÁRIO** — capítulos numerados 01–17 com contagem de exercícios por grupo em laranja;
linha pontilhada conectando número ao título.

**3. CAPÍTULOS INTRODUTÓRIOS (4 arquivos .md anexados)** — não altere o texto. Blockquotes viram
caixas de destaque com barra lateral laranja e fundo #FFEDE0; tabelas de rotina com cabeçalho
escuro, linhas zebradas e a coluna de séries×reps em bold; listas numeradas com números em
círculos laranja.

**4. DIVISOR DE GRUPO MUSCULAR (12×, fundo escuro)** — número do capítulo gigante (80–100 pt)
vazado ou em 15% de opacidade; nome do grupo em condensada; frase-resumo; lista dos exercícios
do capítulo em 2 colunas com marcadores laranja. É a página que dá a sensação de "novo território
do atlas".

**5. FICHA DE EXERCÍCIO (152×, 1 por página, fundo claro) — o coração do produto:**
- Cabeçalho: nome PT em condensada 16–18 pt + nome original em 8 pt cinza logo abaixo;
- Linha de chips: músculo alvo (chip laranja sólido, texto branco) + equipamento, nível, mecânica
  e auxiliares (chips outline cinza);
- Par de fotos lado a lado, mesma altura (~50 mm), cantos levemente arredondados (2 mm), borda
  1 px #E4E1DB, com micro-rótulos "INÍCIO" e "FIM" e uma seta fina laranja entre elas;
- Passos numerados: números em círculos laranja, texto 10 pt, entrelinha 1,5;
- Bloco de vídeo no canto direito: QR code ≥ 22 mm com zona de silêncio branca preservada +
  legenda "Aponte a câmera para ver vídeos";
- Rodapé fixo: nome do grupo muscular à esquerda · número da página à direita, separados por
  filete laranja de 0,5 pt.
- As 152 fichas devem ser IDÊNTICAS em estrutura — a padronização é o que passa profissionalismo.

**6. ÍNDICE POR EQUIPAMENTO** — 2 colunas, títulos de equipamento em laranja, e o aviso legal
(material educacional, não substitui profissional) em 8 pt no rodapé final.

## DADOS (não invente nada)

`exercicios.json`: campos `nome`, `nome_original`, `grupo_titulo`, `musculo_alvo`,
`musculos_secundarios`, `equipamento`, `nivel`, `mecanica`, `imagens` (2 caminhos), `qrcode`
(caminho PNG), `instrucoes` (passos PT-BR). `capitulos/*.md`: texto pronto. Seu trabalho é forma,
nunca conteúdo. Zero lorem ipsum, zero placeholder, zero texto em inglês fora de `nome_original`.

## RESTRIÇÕES TÉCNICAS INEGOCIÁVEIS

- Saída: **um único HTML com CSS embutido**, print-ready: `@page { size: A4; margin: … }`, cada
  página em bloco com `page-break-after: always`, fichas com `break-inside: avoid`;
- Caminhos de imagem relativos EXATAMENTE como no JSON (`assets/images/...`, `assets/qrcodes/...`)
  prefixados com `../` (o HTML vive em `build/`);
- Zero JavaScript, zero fonte de CDN, zero imagem remota — o PDF é gerado offline com Chromium
  headless;
- Fotos com `object-fit: cover` e mesma altura no par — nunca distorcidas;
- Como são 152 fichas, gere um **script Python único** que lê o JSON e os .md e escreve o HTML
  (use `build/gerar_html.py` do repositório como referência estrutural, mas o design é 100% seu).

## CHECKLIST FINAL (verifique item a item antes de entregar)

- [ ] Capa legível em miniatura de 200 px;
- [ ] Nenhuma ficha quebrada entre páginas;
- [ ] Divisores escuros / miolo claro alternando com ritmo;
- [ ] Laranja presente em todas as páginas, nunca acima de ~10% da área;
- [ ] Contraste WCAG AA em todo texto;
- [ ] QRs ≥ 22 mm com zona de silêncio;
- [ ] Rodapé com grupo + página em todas as fichas;
- [ ] Aviso legal presente.

## PROTOCOLO DE ENTREGA (siga a ordem, não pule etapas)

1. **Primeiro:** me mostre **3 direções de capa** diferentes (variações de composição tipográfica
   e elemento gráfico) e espere eu escolher;
2. Com a capa aprovada, mostre **1 divisor + 1 ficha de exercício** no mesmo sistema visual e
   espere aprovação;
3. Só então gere o documento completo;
4. Encerre com um resumo de 10 linhas das decisões de design (paleta final, fontes, escala,
   espaçamentos).

---

## Dicas de uso

- **Iterar:** o protocolo já força a ordem certa — capa primeiro (é o thumbnail da página de
  vendas), depois as páginas-modelo, depois o documento.
- **Trocar a paleta:** substitua o `#E8590C` pela cor da sua marca antes de enviar.
- **Regerar o PDF:** substitua `build/guia.html` pelo HTML novo e rode `bash build/build_pdf.sh`
  (requer Chromium; em outra máquina, aponte a variável `CHROMIUM` para o executável do
  Chrome/Chromium).
