#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atlas de Treino — gerador do Guia Completo de Exercícios (print-ready A4).

Lê  content/exercicios.json  +  content/capitulos/*.md
Escreve  build/guia.html  (HTML único, CSS embutido, zero JS, zero CDN).
Converta em PDF com build/build_pdf.sh (Chromium headless, --no-pdf-header-footer).

Design: "Atlas de Treino" — papel off-white, tinta grafite, laranja queimado de ação,
tipografia condensada para display + humanista para corpo. Capa e divisores invertem
para fundo escuro; miolo sempre claro.
"""
import html, json, re
from pathlib import Path

REPO   = Path(__file__).resolve().parent.parent
EXPATH = REPO / "content/exercicios.json"
CAPDIR = REPO / "content/capitulos"
OUT    = REPO / "build/guia.html"

# Nº de páginas de IMPRESSÃO que cada capítulo introdutório ocupa (na ordem 01..04).
# Medido no layout atual. Se você editar muito o texto dos capítulos, reconte e ajuste
# — só afeta o número de página impresso no rodapé das fichas.
CHAPTER_PAGES = [1, 2, 2, 3]

# ----------------------------------------------------------------------------- CSS
CSS = r"""
:root{
  --paper:#FAFAF8; --ink:#16181D; --meta:#5C636B; --line:#E4E1DB;
  --action:#E8590C; --action-dark:#C14A00; --tint:#FFEDE0;
  --disp:'Oswald','Archivo Narrow','Roboto Condensed','Noto Sans Condensed','DejaVu Sans Condensed','Liberation Sans Narrow','Arial Narrow','Helvetica Neue',sans-serif;
  --body:'Inter','Source Sans 3','Source Sans Pro','Noto Sans','Segoe UI','Helvetica Neue',Arial,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:#6f6f6b;}
body{font-family:var(--body); color:var(--ink); -webkit-print-color-adjust:exact; print-color-adjust:exact;}

@page{ size:A4; margin:16mm 16mm 15mm;
  @bottom-left{ content:"ATLAS DE TREINO — GUIA COMPLETO DE EXERCÍCIOS"; font-family:Arial,sans-serif; font-size:7pt; letter-spacing:1.1px; color:#E8590C; }
  @bottom-right{ content:counter(page); font-family:Arial,sans-serif; font-size:8pt; color:#5C636B; }
}
@page bleed{ size:A4; margin:0; }

a{color:var(--action-dark);text-decoration:none;} a:hover{color:var(--action);}
.disp{ font-family:var(--disp); font-weight:800; font-stretch:condensed; }
.caps{ text-transform:uppercase; letter-spacing:.08em; }

.sheet{ position:relative; width:210mm; height:297mm; overflow:hidden; background:var(--paper); color:var(--ink); }
.sheet--bleed{ page:bleed; }

@media screen{
  body{ padding:26px 0; display:flex; flex-direction:column; align-items:center; gap:22px; }
  .sheet,.flow{ box-shadow:0 16px 50px rgba(0,0,0,.30); }
  .flow{ width:210mm; min-height:297mm; padding:16mm; background:var(--paper); }
}
@media print{
  .sheet{ break-after:page; }
  .sheet:last-child{ break-after:auto; }
  .flow{ break-after:page; background:var(--paper); }
}

/* ============ CAPA (1B Manual Técnico) ============ */
.capa{ background:var(--ink); color:var(--paper); padding:20mm; display:flex; flex-direction:column; }
.capa .grid{ position:absolute; inset:0; background-image:linear-gradient(90deg,#FAFAF8 1px,transparent 1px); background-size:16.6mm 100%; opacity:.03; }
.capa .ghost{ position:absolute; right:-8mm; top:40mm; font-family:var(--disp); font-weight:800; font-size:180mm; line-height:.8; color:var(--paper); opacity:.05; letter-spacing:-.02em; }
.capa .top{ position:relative; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #2c2f36; padding-bottom:5mm; font-size:8pt; letter-spacing:1.6px; text-transform:uppercase; color:#8a9098; }
.capa .top .o{ color:var(--action); }
.capa .mid{ position:relative; margin-top:auto; }
.capa .t{ font-family:var(--disp); font-weight:800; font-stretch:condensed; line-height:.9; }
.capa .t1{ font-size:52pt; color:var(--paper); }
.capa .t2{ font-size:30pt; color:var(--paper); margin-top:2mm; }
.capa .t3{ font-size:58pt; color:var(--action); margin-top:1mm; }
.capa .subwrap{ display:flex; gap:5mm; margin-top:9mm; }
.capa .bar{ width:3px; background:var(--action); flex-shrink:0; }
.capa .sub{ font-size:12pt; line-height:1.6; color:#B9BDC4; max-width:120mm; }
.capa .specs{ position:relative; margin-top:auto; padding-top:6mm; border-top:1px solid var(--action); display:flex; }
.capa .spec{ flex:1; }
.capa .spec .l{ font-size:8pt; letter-spacing:1.4px; text-transform:uppercase; color:#8a9098; font-weight:600; }
.capa .spec .n{ font-family:var(--disp); font-weight:800; font-size:34pt; line-height:1; margin-top:2mm; color:var(--paper); }
.capa .spec:first-child .n{ color:var(--action); }

/* ============ SUMÁRIO ============ */
.sumario{ padding:22mm 20mm; display:flex; flex-direction:column; }
.sum-eyebrow{ display:flex; align-items:center; gap:3mm; color:var(--action); font-size:8.5pt; font-weight:600; letter-spacing:1.8px; text-transform:uppercase; }
.sum-eyebrow .r{ width:20mm; height:1px; background:var(--action); }
.sum-title{ font-family:var(--disp); font-weight:800; font-stretch:condensed; font-size:44pt; line-height:1; margin:3mm 0 10mm; }
.sum-list{ display:flex; flex-direction:column; }
.sum-row{ display:flex; align-items:baseline; gap:4mm; padding:2.7mm 0; border-bottom:1px solid var(--line); }
.sum-row .n{ font-family:var(--disp); font-weight:800; font-size:13pt; color:var(--action); min-width:11mm; }
.sum-row .t{ font-size:12pt; color:var(--ink); font-weight:500; }
.sum-row .dots{ flex:1; border-bottom:1px dotted #c9c6bf; transform:translateY(-1.5mm); }
.sum-row .c{ font-size:9pt; color:var(--action); font-weight:600; letter-spacing:.06em; text-transform:uppercase; white-space:nowrap; }
.sum-row .c.muted{ color:var(--meta); }
.sum-foot{ margin-top:auto; padding-top:8mm; font-size:8pt; color:var(--meta); letter-spacing:1.2px; text-transform:uppercase; }

/* ============ CAPÍTULOS (flow) ============ */
.capitulo{ color:var(--ink); }
.capitulo .cap-titulo{ font-family:var(--disp); font-weight:800; font-stretch:condensed; font-size:28pt; line-height:1.0; margin:0 0 7mm; padding-bottom:3.5mm; border-bottom:2px solid var(--action); }
.capitulo h3{ font-family:var(--disp); font-weight:700; font-stretch:condensed; font-size:15pt; margin:8mm 0 2.5mm; color:var(--ink); }
.capitulo h4{ font-weight:700; font-size:11pt; margin:5mm 0 1.5mm; color:var(--ink); }
.capitulo p{ margin:2.6mm 0; font-size:10.5pt; line-height:1.62; color:#22252b; }
.capitulo hr{ border:none; border-top:1px solid var(--line); margin:6mm 0; }
.capitulo code{ font-family:'DejaVu Sans Mono',monospace; background:#efeee9; padding:.2mm 1mm; border-radius:.6mm; font-size:9.5pt; }
.capitulo ul{ list-style:none; margin:3mm 0; }
.capitulo ul li{ position:relative; padding-left:6mm; margin:1.6mm 0; font-size:10.5pt; line-height:1.55; }
.capitulo ul li::before{ content:""; position:absolute; left:0; top:2.3mm; width:2.1mm; height:2.1mm; background:var(--action); border-radius:.4mm; }
.capitulo ol{ list-style:none; counter-reset:li; margin:3mm 0; }
.capitulo ol li{ counter-increment:li; position:relative; padding-left:9mm; margin:2.6mm 0; font-size:10.5pt; line-height:1.55; }
.capitulo ol li::before{ content:counter(li); position:absolute; left:0; top:-.4mm; width:6mm; height:6mm; background:var(--action); color:#fff; border-radius:50%; font-family:var(--disp); font-weight:800; font-size:9pt; display:flex; align-items:center; justify-content:center; }
.capitulo blockquote{ background:var(--tint); border-left:3px solid var(--action); padding:4mm 5mm; margin:4.5mm 0; font-size:10pt; line-height:1.55; border-radius:0 1mm 1mm 0; color:#3a2a20; break-inside:avoid; }
.capitulo table{ border-collapse:collapse; width:100%; margin:4mm 0; break-inside:avoid; }
.capitulo thead th{ background:var(--ink); color:#fff; text-align:left; padding:2.6mm 3.4mm; font-size:8pt; letter-spacing:.6px; text-transform:uppercase; font-weight:600; }
.capitulo tbody td{ border-bottom:1px solid var(--line); padding:2.3mm 3.4mm; font-size:9.5pt; line-height:1.4; vertical-align:top; }
.capitulo tbody tr:nth-child(even){ background:#F2F1ED; }
.capitulo tbody td:last-child{ font-weight:700; font-variant-numeric:tabular-nums; white-space:nowrap; color:var(--ink); }

/* ============ DIVISOR ============ */
.divisor{ background:var(--ink); color:var(--paper); padding:22mm 20mm; display:flex; flex-direction:column; }
.divisor .grid{ position:absolute; inset:0; background-image:linear-gradient(#FAFAF8 1px,transparent 1px),linear-gradient(90deg,#FAFAF8 1px,transparent 1px); background-size:12mm 12mm; opacity:.03; }
.divisor .ghostnum{ position:absolute; right:6mm; top:0; font-family:var(--disp); font-weight:800; font-size:150mm; line-height:.8; color:var(--paper); opacity:.06; letter-spacing:-.02em; }
.div-top{ position:relative; display:flex; align-items:center; gap:3mm; color:var(--action); font-size:8pt; font-weight:600; letter-spacing:1.4px; text-transform:uppercase; }
.div-top .rule{ width:20mm; height:1px; background:var(--action); }
.div-mid{ position:relative; margin-top:auto; }
.div-chapno{ font-family:var(--disp); font-weight:800; font-size:18pt; color:var(--action); letter-spacing:.06em; }
.div-name{ font-family:var(--disp); font-weight:800; font-stretch:condensed; font-size:46pt; line-height:.96; margin-top:2mm; }
.div-sub{ font-size:11pt; line-height:1.5; color:#B9BDC4; max-width:130mm; margin-top:5mm; }
.div-list{ position:relative; margin-top:12mm; padding-top:7mm; border-top:1px solid #2c2f36; columns:2; column-gap:12mm; }
.div-list .item{ break-inside:avoid; display:flex; gap:3mm; align-items:baseline; padding:2mm 0; font-size:9pt; color:#E6E7EA; border-bottom:1px solid #23262d; }
.div-list .item .n{ font-family:var(--disp); font-weight:800; color:var(--action); font-size:8.5pt; min-width:6.5mm; }
.div-foot{ position:relative; margin-top:12mm; display:flex; justify-content:space-between; align-items:center; font-size:8pt; color:#7c828b; letter-spacing:1.2px; text-transform:uppercase; }

/* ============ FICHA ============ */
.ficha{ padding:14mm 14mm 12mm; display:flex; flex-direction:column; }
.fx-head{ display:flex; justify-content:space-between; align-items:flex-start; gap:8mm; }
.fx-title{ font-family:var(--disp); font-weight:800; font-stretch:condensed; font-size:18pt; line-height:1.02; }
.fx-orig{ font-size:8pt; color:var(--meta); font-style:italic; margin-top:1.5mm; letter-spacing:.02em; }
.fx-idx{ text-align:right; flex-shrink:0; }
.fx-idx .num{ font-family:var(--disp); font-weight:800; font-size:15pt; color:var(--line); line-height:1; }
.fx-idx .lbl{ font-size:7pt; color:var(--meta); letter-spacing:1.4px; text-transform:uppercase; margin-top:1mm; }
.chips{ display:flex; flex-wrap:wrap; gap:1.6mm; margin-top:7mm; }
.chip{ font-size:7.5pt; letter-spacing:.5px; text-transform:uppercase; font-weight:600; padding:2.1mm 3mm; border-radius:1mm; line-height:1; white-space:nowrap; }
.chip--alvo{ background:var(--action); color:#fff; }
.chip--out{ background:transparent; color:var(--meta); border:1px solid var(--line); }
.chip--out b{ color:var(--ink); font-weight:700; }
.photos{ position:relative; display:flex; gap:6mm; margin-top:8mm; height:58mm; }
.photo{ position:relative; flex:1; height:100%; border:1px solid var(--line); border-radius:2mm; overflow:hidden; background:#f2f1ed; padding:1.5mm; }
.photo img{ width:100%; height:100%; object-fit:contain; display:block; }
.photo .tag{ position:absolute; top:2.5mm; left:2.5mm; background:var(--ink); color:#fff; font-size:7pt; letter-spacing:1.2px; font-weight:700; padding:1.4mm 2.4mm; border-radius:.8mm; }
.arrow{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); z-index:3; width:8mm; height:8mm; border-radius:50%; background:var(--paper); border:1px solid var(--line); display:flex; align-items:center; justify-content:center; }
.arrow svg{ width:4.4mm; height:4.4mm; }
.fx-body{ display:flex; gap:9mm; margin-top:8mm; flex:1; }
.steps{ flex:1; }
.steps-h{ font-size:7.5pt; letter-spacing:1.6px; text-transform:uppercase; color:var(--meta); font-weight:600; margin-bottom:3mm; display:flex; align-items:center; gap:3mm; }
.steps-h::after{ content:""; flex:1; height:1px; background:var(--line); }
.step{ display:flex; gap:4mm; margin-bottom:3.2mm; }
.step .n{ flex-shrink:0; width:6mm; height:6mm; border-radius:50%; background:var(--action); color:#fff; font-family:var(--disp); font-weight:800; font-size:9pt; display:flex; align-items:center; justify-content:center; margin-top:.3mm; }
.step p{ font-size:10pt; line-height:1.55; color:#24272d; }
.video{ width:46mm; flex-shrink:0; }
.video-card{ border:1px solid var(--line); border-radius:2mm; background:#fff; padding:5mm 5mm 4.5mm; text-align:center; }
.video-h{ font-size:7pt; letter-spacing:1.4px; text-transform:uppercase; color:var(--action); font-weight:700; margin-bottom:3.5mm; }
.qr{ width:30mm; height:30mm; margin:0 auto; display:block; padding:2mm; background:#fff; border:1px solid #efeee9; border-radius:1mm; }
.qr img{ width:100%; height:100%; display:block; image-rendering:pixelated; }
.video-cap{ font-size:7.5pt; line-height:1.4; color:var(--meta); margin-top:3.5mm; }
.fx-foot{ margin-top:auto; padding-top:4mm; border-top:.5pt solid var(--action); display:flex; justify-content:space-between; align-items:center; }
.fx-foot .g{ font-size:7.5pt; letter-spacing:1.4px; text-transform:uppercase; color:var(--meta); font-weight:600; }
.fx-foot .p{ font-family:var(--disp); font-weight:800; font-size:11pt; color:var(--ink); }

/* ============ ÍNDICE ============ */
.indice{ color:var(--ink); }
.indice .cap-titulo{ font-family:var(--disp); font-weight:800; font-stretch:condensed; font-size:28pt; line-height:1; margin:0 0 3mm; padding-bottom:3.5mm; border-bottom:2px solid var(--action); }
.indice .lead{ font-size:10pt; color:var(--meta); margin-bottom:6mm; }
.indice .cols{ columns:2; column-gap:12mm; }
.indice .blk{ break-inside:avoid; margin-bottom:5mm; }
.indice .blk h3{ font-family:var(--disp); font-weight:700; font-stretch:condensed; font-size:12.5pt; color:var(--action); margin-bottom:2mm; display:flex; align-items:baseline; gap:2mm; }
.indice .blk h3 .q{ font-size:8pt; color:var(--meta); font-family:var(--body); font-weight:600; }
.indice .blk ul{ list-style:none; }
.indice .blk li{ font-size:8.5pt; line-height:1.5; color:#2a2d33; padding:.4mm 0 .4mm 3mm; position:relative; border-bottom:1px solid #efeee9; }
.indice .blk li::before{ content:""; position:absolute; left:0; top:2.3mm; width:1.4mm; height:1.4mm; background:var(--action); border-radius:50%; }
.aviso{ margin-top:8mm; padding-top:4mm; border-top:1px solid var(--line); font-size:8pt; line-height:1.5; color:var(--meta); }
.aviso b{ color:var(--ink); }
"""

# ----------------------------------------------------------------- Markdown -> HTML
def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s

def md_para_html(md):
    L = md.split("\n"); out = []; i = 0; ul = ol = False
    def fecha():
        nonlocal ul, ol
        if ul: out.append("</ul>"); ul = False
        if ol: out.append("</ol>"); ol = False
    while i < len(L):
        ln = L[i]
        if ln.startswith("|") and i + 1 < len(L) and re.match(r"^\|[\s:|-]+\|?$", L[i + 1]):
            fecha()
            head = [c.strip() for c in ln.strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
            i += 2
            while i < len(L) and L[i].startswith("|"):
                cels = [c.strip() for c in L[i].strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cels) + "</tr>")
                i += 1
            out.append("</tbody></table>"); continue
        if ln.startswith("### "):   fecha(); out.append(f"<h4>{inline(ln[4:])}</h4>")
        elif ln.startswith("## "):  fecha(); out.append(f"<h3>{inline(ln[3:])}</h3>")
        elif ln.startswith("# "):   fecha(); out.append(f"<h2 class='cap-titulo'>{inline(ln[2:])}</h2>")
        elif ln.startswith("> "):   fecha(); out.append(f"<blockquote>{inline(ln[2:])}</blockquote>")
        elif re.match(r"^\d+\.\s", ln):
            if not ol: fecha(); out.append("<ol>"); ol = True
            item_txt = re.sub(r"^\d+\.\s", "", ln)
            out.append(f"<li>{inline(item_txt)}</li>")
        elif ln.startswith("- "):
            if not ul: fecha(); out.append("<ul>"); ul = True
            out.append(f"<li>{inline(ln[2:])}</li>")
        elif ln.strip() == "---":   fecha(); out.append("<hr>")
        elif ln.strip():            fecha(); out.append(f"<p>{inline(ln)}</p>")
        i += 1
    fecha()
    return "\n".join(out)

ARROW = ('<div class="arrow"><svg viewBox="0 0 24 24" fill="none">'
         '<path d="M4 12h15M13 6l6 6-6 6" stroke="#E8590C" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
e = html.escape

# --------------------------------------------------------------------------- i18n
# Mapas de VALORES do JSON (que estão em PT) para EN. No modo pt, usa-se o valor cru.
GRP_EN = {  # por slug do grupo (campo "grupo")
    "peito": "Chest", "costas": "Back", "ombros": "Shoulders", "biceps": "Biceps",
    "triceps": "Triceps", "antebraco": "Forearms & Grip", "abdomen": "Abs & Core",
    "quadriceps": "Legs — Quadriceps & Glutes (front focus)",
    "posteriores": "Legs — Hamstrings & Glutes", "panturrilha": "Calves",
    "cardio": "Cardio & Full Body", "pescoco": "Neck",
}
MUS_EN = {
    "Abdômen": "Abs", "Abdutores": "Abductors", "Adutores": "Adductors", "Bíceps": "Biceps",
    "Panturrilhas": "Calves", "Peitoral": "Chest", "Antebraços": "Forearms", "Glúteos": "Glutes",
    "Posteriores de coxa": "Hamstrings", "Dorsais": "Lats", "Lombar": "Lower back",
    "Meio das costas": "Middle back", "Pescoço": "Neck", "Quadríceps": "Quadriceps",
    "Ombros": "Shoulders", "Trapézio": "Traps", "Tríceps": "Triceps",
}
EQP_EN = {
    "Barra": "Barbell", "Halteres": "Dumbbell", "Peso corporal": "Bodyweight",
    "Cabo/Polia": "Cable", "Máquina": "Machine", "Kettlebell": "Kettlebell", "Elástico": "Band",
    "Medicine ball": "Medicine ball", "Bola suíça": "Exercise ball", "Barra W": "EZ bar",
    "Rolo de espuma": "Foam roll", "Acessórios": "Other", "Sem equipamento": "No equipment",
}
LVL_EN = {"Iniciante": "Beginner", "Intermediário": "Intermediate", "Avançado": "Advanced"}
MEC_EN = {"Composto": "Compound", "Isolado": "Isolation"}
FRC_EN = {"Empurrar": "Push", "Puxar": "Pull", "Estático": "Static"}

# Strings de interface por idioma
T = {
    "pt": {
        "html_lang": "pt-BR", "title": "Guia Completo de Exercícios — Atlas de Treino",
        "out": REPO / "build/guia.html", "capdir": REPO / "content/capitulos",
        "instr": "instrucoes", "qr": "qrcode", "footer_run": "ATLAS DE TREINO — GUIA COMPLETO DE EXERCÍCIOS",
        "cover_tag": "GCE · 2026", "cover_manual": "Manual Técnico de Treino", "cover_fmt": "A4 · PT-BR",
        "cover_lines": [("t1", "GUIA"), ("t1", "COMPLETO"), ("t2", "DE"), ("t3", "EXERCÍCIOS")],
        "cover_sub": "{n} exercícios ilustrados com fotos, passo a passo e vídeos — para treinar em casa ou na academia.",
        "spec": ["Exercícios", "Grupos", "Equipamentos", "Rotinas"],
        "toc_eyebrow": "Atlas de Treino · Conteúdo", "toc_title": "SUMÁRIO", "toc_chapter": "Capítulo",
        "toc_exercises": "exercícios", "toc_index": "Índice por Equipamento", "toc_groups": "grupos",
        "toc_foot": "17 capítulos · {n} fichas técnicas · 6 rotinas prontas",
        "div_top": "Atlas de Treino — Grupo Muscular {i} / {t}", "div_chapno": "CAPÍTULO {c}",
        "div_sub": "{n} exercícios ilustrados — cada ficha traz o músculo alvo, o equipamento, o nível, fotos da posição inicial e final, execução passo a passo e QR code com vídeo.",
        "div_foot_name": "Guia Completo de Exercícios", "div_foot_page": "Pág. {n}",
        "chip_alvo": "Alvo", "chip_equip": "Equip.", "chip_nivel": "Nível", "chip_mec": "Mecânica",
        "chip_forca": "Força", "chip_aux": "Aux.", "card_lbl": "Ficha", "steps_h": "Passo a passo",
        "video_h": "Vídeo do exercício", "video_cap": "Aponte a câmera do celular para o código e assista à demonstração em vídeo.",
        "idx_title": "ÍNDICE POR EQUIPAMENTO",
        "idx_lead": "Todos os {n} exercícios organizados pelo equipamento necessário — encontre rápido o que dá para treinar com o que você tem à mão.",
        "aviso": "<b>Aviso legal:</b> este material tem caráter educacional e não substitui a orientação individualizada de um profissional de educação física ou médico. Se você tem qualquer condição de saúde, lesão prévia ou dor persistente, consulte um profissional antes de iniciar qualquer programa de exercícios. Fotos e dados-base: free-exercise-db (domínio público). Texto em português: conteúdo original.",
    },
    "en": {
        "html_lang": "en", "title": "Complete Exercise Guide — Training Atlas",
        "out": REPO / "build/guide-en.html", "capdir": REPO / "content/capitulos-en",
        "instr": "instrucoes_en", "qr": "qrcode_en", "footer_run": "TRAINING ATLAS — COMPLETE EXERCISE GUIDE",
        "cover_tag": "CEG · 2026", "cover_manual": "Technical Training Manual", "cover_fmt": "A4 · EN",
        "cover_lines": [("t1", "COMPLETE"), ("t1", "EXERCISE"), ("t3", "GUIDE")],
        "cover_sub": "{n} illustrated exercises with photos, step-by-step instructions and videos — to train at home or at the gym.",
        "spec": ["Exercises", "Groups", "Equipment", "Routines"],
        "toc_eyebrow": "Training Atlas · Contents", "toc_title": "CONTENTS", "toc_chapter": "Chapter",
        "toc_exercises": "exercises", "toc_index": "Index by Equipment", "toc_groups": "groups",
        "toc_foot": "17 chapters · {n} technical cards · 6 ready-made routines",
        "div_top": "Training Atlas — Muscle Group {i} / {t}", "div_chapno": "CHAPTER {c}",
        "div_sub": "{n} illustrated exercises — each card shows the target muscle, equipment, level, photos of the start and end positions, step-by-step execution and a QR code with video.",
        "div_foot_name": "Complete Exercise Guide", "div_foot_page": "P. {n}",
        "chip_alvo": "Target", "chip_equip": "Equip.", "chip_nivel": "Level", "chip_mec": "Mechanics",
        "chip_forca": "Force", "chip_aux": "Sec.", "card_lbl": "Card", "steps_h": "Step by step",
        "video_h": "Exercise video", "video_cap": "Point your phone camera at the code and watch the video demonstration.",
        "idx_title": "INDEX BY EQUIPMENT",
        "idx_lead": "All {n} exercises organized by the equipment needed — quickly find what you can train with whatever you have on hand.",
        "aviso": "<b>Disclaimer:</b> this material is educational and does not replace individualized guidance from a certified fitness professional or physician. If you have any health condition, previous injury or persistent pain, consult a professional before starting any exercise program. Photos and base data: free-exercise-db (public domain). English text: original content.",
    },
}

# --------------------------------------------------------------------------- build
def main(lang="pt"):
    t = T[lang]
    EX = json.loads(EXPATH.read_text(encoding="utf-8"))
    caps = [p.read_text(encoding="utf-8") for p in sorted(t["capdir"].glob("*.md"))]
    cap_titles = [c.split("\n")[0].lstrip("# ").strip() for c in caps]
    cap_html   = [md_para_html(c) for c in caps]

    def gtitulo(x):  # título do grupo no idioma
        return GRP_EN[x["grupo"]] if lang == "en" else x["grupo_titulo"]
    def mapv(dic, v):
        return dic.get(v, v) if lang == "en" else v
    def nome(x):     # nome de exibição do exercício
        return x["nome_original"] if lang == "en" else x["nome"]

    groups, order = {}, []
    for x in EX:
        if x["grupo"] not in groups:
            groups[x["grupo"]] = {"titulo": gtitulo(x), "itens": []}; order.append(x["grupo"])
        groups[x["grupo"]]["itens"].append(x)
    n_eq = len({x["equipamento"] for x in EX})
    C = sum(CHAPTER_PAGES)

    css = CSS.replace("ATLAS DE TREINO — GUIA COMPLETO DE EXERCÍCIOS", t["footer_run"])

    P = [f"<!DOCTYPE html><html lang='{t['html_lang']}'><head><meta charset='utf-8'>"
         f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<title>{e(t['title'])}</title><style>{css}</style></head><body>"]

    # CAPA
    lines = "".join(f'<div class="t {cls}">{txt}</div>' for cls, txt in t["cover_lines"])
    specs = "".join(f'<div class="spec"><div class="l">{lbl}</div><div class="n">{val}</div></div>'
                    for lbl, val in zip(t["spec"], [len(EX), len(order), n_eq, 6]))
    P.append(f"""<section class="sheet sheet--bleed capa"><div class="grid"></div><div class="ghost">{len(EX)}</div>
      <div class="top"><span class="o">{t['cover_tag']}</span><span>{t['cover_manual']}</span><span>{t['cover_fmt']}</span></div>
      <div class="mid">{lines}
        <div class="subwrap"><div class="bar"></div><p class="sub">{t['cover_sub'].format(n=len(EX))}</p></div></div>
      <div class="specs">{specs}</div></section>""")

    # SUMÁRIO
    rows = ""
    for idx, tt in enumerate(cap_titles):
        rows += f"<div class='sum-row'><span class='n'>{idx+1:02d}</span><span class='t'>{e(tt)}</span><span class='dots'></span><span class='c muted'>{t['toc_chapter']}</span></div>"
    for idx, g in enumerate(order):
        s = groups[g]
        rows += f"<div class='sum-row'><span class='n'>{idx+5:02d}</span><span class='t'>{e(s['titulo'])}</span><span class='dots'></span><span class='c'>{len(s['itens'])} {t['toc_exercises']}</span></div>"
    rows += f"<div class='sum-row'><span class='n'>17</span><span class='t'>{t['toc_index']}</span><span class='dots'></span><span class='c muted'>{n_eq} {t['toc_groups']}</span></div>"
    P.append(f"""<section class="sheet sheet--bleed sumario"><div class="sum-eyebrow"><span class="r"></span>{t['toc_eyebrow']}</div>
      <h1 class="sum-title">{t['toc_title']}</h1><div class="sum-list">{rows}</div>
      <div class="sum-foot">{t['toc_foot'].format(n=len(EX))}</div></section>""")

    # CAPÍTULOS
    for h in cap_html:
        P.append(f"<section class='flow capitulo'>{h}</section>")

    # DIVISORES + FICHAS
    page_no = 2 + C
    ficha = 0
    for gi, g in enumerate(order):
        s = groups[g]; chap = f"{gi+5:02d}"; page_no += 1
        items = "".join(f"<div class='item'><span class='n'>{i+1:02d}</span>{e(nome(x))}</div>" for i, x in enumerate(s["itens"]))
        P.append(f"""<section class="sheet sheet--bleed divisor"><div class="grid"></div><div class="ghostnum">{chap}</div>
          <div class="div-top"><span class="rule"></span>{t['div_top'].format(i=f'{gi+1:02d}', t=len(order))}</div>
          <div class="div-mid"><div class="div-chapno">{t['div_chapno'].format(c=chap)}</div><div class="div-name">{e(s['titulo']).upper()}</div>
            <p class="div-sub">{t['div_sub'].format(n=len(s['itens']))}</p></div>
          <div class="div-list">{items}</div>
          <div class="div-foot"><span>{t['div_foot_name']}</span><span>{t['div_foot_page'].format(n=page_no)}</span></div></section>""")
        for x in s["itens"]:
            ficha += 1; page_no += 1
            chips = (f"<span class='chip chip--alvo'>{t['chip_alvo']} · {e(mapv(MUS_EN, x['musculo_alvo']))}</span>"
                     f"<span class='chip chip--out'><b>{t['chip_equip']}</b> {e(mapv(EQP_EN, x['equipamento']))}</span>"
                     f"<span class='chip chip--out'><b>{t['chip_nivel']}</b> {e(mapv(LVL_EN, x['nivel']))}</span>")
            if x.get("mecanica") and x["mecanica"] != "—":
                chips += f"<span class='chip chip--out'><b>{t['chip_mec']}</b> {e(mapv(MEC_EN, x['mecanica']))}</span>"
            if x.get("forca") and x["forca"] != "—":
                chips += f"<span class='chip chip--out'><b>{t['chip_forca']}</b> {e(mapv(FRC_EN, x['forca']))}</span>"
            if x.get("musculos_secundarios"):
                sec = ", ".join(mapv(MUS_EN, m) for m in x["musculos_secundarios"])
                chips += f"<span class='chip chip--out'><b>{t['chip_aux']}</b> {e(sec)}</span>"
            instr = x[t["instr"]] or x.get("instrucoes", [])
            steps = "".join(f"<div class='step'><span class='n'>{i+1}</span><p>{e(p)}</p></div>" for i, p in enumerate(instr))
            orig = "" if lang == "en" else e(x["nome_original"])
            P.append(f"""<section class="sheet ficha"><div class="fx-head"><div><h1 class="fx-title">{e(nome(x)).upper()}</h1><div class="fx-orig">{orig}</div></div><div class="fx-idx"><div class="num">{ficha:03d}</div><div class="lbl">{t['card_lbl']}</div></div></div>
              <div class="chips">{chips}</div>
              <div class="photos"><div class="photo"><span class="tag">{'START' if lang=='en' else 'INÍCIO'}</span><img src="../{x['imagens'][0]}" alt=""></div>{ARROW}<div class="photo"><span class="tag">{'END' if lang=='en' else 'FIM'}</span><img src="../{x['imagens'][1]}" alt=""></div></div>
              <div class="fx-body"><div class="steps"><div class="steps-h">{t['steps_h']}</div>{steps}</div>
                <aside class="video"><div class="video-card"><div class="video-h">{t['video_h']}</div><div class="qr"><img src="../{x[t['qr']]}" alt="QR"></div><p class="video-cap">{t['video_cap']}</p></div></aside></div>
              <div class="fx-foot"><span class="g">{e(s['titulo'])}</span><span class="p">{page_no}</span></div></section>""")

    # ÍNDICE POR EQUIPAMENTO
    por_eq = {}
    for x in EX:
        por_eq.setdefault(mapv(EQP_EN, x["equipamento"]), []).append(nome(x))
    blocks = ""
    for eq, nomes in sorted(por_eq.items(), key=lambda kv: -len(kv[1])):
        lis = "".join(f"<li>{e(n)}</li>" for n in sorted(nomes, key=lambda s: s.lower()))
        blocks += f"<div class='blk'><h3>{e(eq)} <span class='q'>{len(nomes)}</span></h3><ul>{lis}</ul></div>"
    P.append(f"""<section class="flow indice"><h1 class="cap-titulo">{t['idx_title']}</h1>
      <p class="lead">{t['idx_lead'].format(n=len(EX))}</p>
      <div class="cols">{blocks}</div>
      <div class="aviso">{t['aviso']}</div></section>""")

    P.append("</body></html>")
    t["out"].write_text("\n".join(P), encoding="utf-8")
    print(f"OK [{lang}] -> {t['out'].name}  ({t['out'].stat().st_size // 1024} KB, {len(EX)} exercícios, {len(order)} grupos, última pág. {page_no})")

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "pt")
