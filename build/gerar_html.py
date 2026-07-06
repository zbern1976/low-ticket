#!/usr/bin/env python3
"""Monta build/guia.html a partir de content/exercicios.json e content/capitulos/*.md.

Layout baseline limpo e funcional — a identidade visual final pode ser aplicada
seguindo design/PROMPT-DESIGN.md.
"""
import html
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EX = json.loads((REPO / "content/exercicios.json").read_text())
CAP_DIR = REPO / "content/capitulos"


def md_para_html(md: str) -> str:
    """Conversor Markdown mínimo (títulos, listas, tabelas, negrito, itálico, quote)."""
    linhas = md.split("\n")
    out, i = [], 0
    em_ul, em_ol = False, False

    def inline(s):
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
        return s

    def fecha_listas():
        nonlocal em_ul, em_ol
        if em_ul:
            out.append("</ul>"); em_ul = False
        if em_ol:
            out.append("</ol>"); em_ol = False

    while i < len(linhas):
        ln = linhas[i]
        if ln.startswith("|") and i + 1 < len(linhas) and re.match(r"^\|[\s:|-]+\|?$", linhas[i + 1]):
            fecha_listas()
            cab = [c.strip() for c in ln.strip("|").split("|")]
            out.append('<table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in cab) + "</tr></thead><tbody>")
            i += 2
            while i < len(linhas) and linhas[i].startswith("|"):
                cels = [c.strip() for c in linhas[i].strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cels) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        if ln.startswith("### "):
            fecha_listas(); out.append(f"<h4>{inline(ln[4:])}</h4>")
        elif ln.startswith("## "):
            fecha_listas(); out.append(f"<h3>{inline(ln[3:])}</h3>")
        elif ln.startswith("# "):
            fecha_listas(); out.append(f"<h2 class='cap-titulo'>{inline(ln[2:])}</h2>")
        elif ln.startswith("> "):
            fecha_listas(); out.append(f"<blockquote>{inline(ln[2:])}</blockquote>")
        elif re.match(r"^\d+\.\s", ln):
            if not em_ol:
                fecha_listas(); out.append("<ol>"); em_ol = True
            texto_item = re.sub(r"^\d+\.\s", "", ln)
            out.append(f"<li>{inline(texto_item)}</li>")
        elif ln.startswith("- "):
            if not em_ul:
                fecha_listas(); out.append("<ul>"); em_ul = True
            out.append(f"<li>{inline(ln[2:])}</li>")
        elif ln.strip() == "---":
            fecha_listas(); out.append("<hr>")
        elif ln.strip():
            fecha_listas(); out.append(f"<p>{inline(ln)}</p>")
        i += 1
    fecha_listas()
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; color: #1a1d21; font-size: 10.5pt; line-height: 1.55; }
.pagina { page-break-after: always; }

/* Capa */
.capa { display: flex; flex-direction: column; justify-content: center; min-height: 250mm; text-align: center; }
.capa .selo { font-size: 10pt; letter-spacing: 3px; text-transform: uppercase; color: #e8590c; font-weight: 700; margin-bottom: 12mm; }
.capa h1 { font-size: 34pt; line-height: 1.15; margin-bottom: 8mm; }
.capa .sub { font-size: 13pt; color: #495057; max-width: 130mm; margin: 0 auto 16mm; }
.capa .stats { display: flex; justify-content: center; gap: 14mm; }
.capa .stat b { display: block; font-size: 22pt; color: #e8590c; }
.capa .stat span { font-size: 9pt; text-transform: uppercase; letter-spacing: 1px; color: #868e96; }

/* Sumário */
.sumario h2, .cap-titulo { font-size: 20pt; margin-bottom: 6mm; border-bottom: 3px solid #e8590c; padding-bottom: 2mm; }
.sumario ol { margin: 4mm 0 0 6mm; }
.sumario li { font-size: 12pt; padding: 1.6mm 0; }
.sumario .qtd { color: #868e96; font-size: 9.5pt; }

/* Capítulos em markdown */
.capitulo h3 { font-size: 13.5pt; margin: 5mm 0 2mm; color: #1a1d21; }
.capitulo h4 { font-size: 11.5pt; margin: 4mm 0 1.5mm; }
.capitulo p { margin: 2mm 0; }
.capitulo ul, .capitulo ol { margin: 2mm 0 2mm 6mm; }
.capitulo li { margin: 1mm 0; }
.capitulo blockquote { border-left: 3px solid #e8590c; background: #fff4ec; padding: 3mm 4mm; margin: 3mm 0; font-size: 10pt; }
.capitulo table { border-collapse: collapse; width: 100%; margin: 3mm 0; }
.capitulo th, .capitulo td { border: 1px solid #dee2e6; padding: 1.8mm 3mm; text-align: left; font-size: 9.5pt; }
.capitulo th { background: #f1f3f5; }
.capitulo hr { border: none; border-top: 1px solid #dee2e6; margin: 5mm 0; }

/* Divisor de seção */
.divisor { display: flex; flex-direction: column; justify-content: center; min-height: 250mm; }
.divisor .num { font-size: 60pt; font-weight: 800; color: #ffe3d1; line-height: 1; }
.divisor h2 { font-size: 26pt; margin: 2mm 0 4mm; }
.divisor p { color: #495057; max-width: 140mm; }
.divisor ul { columns: 2; margin: 6mm 0 0 5mm; font-size: 9.5pt; color: #495057; }

/* Card de exercício */
.exercicio { border: 1px solid #e9ecef; border-radius: 3mm; padding: 3.5mm 4.5mm; margin-bottom: 4mm; break-inside: avoid; }
.exercicio h3 { font-size: 12.5pt; margin-bottom: 0.5mm; }
.exercicio .original { font-size: 8.5pt; color: #adb5bd; margin-bottom: 2mm; }
.chips { display: flex; flex-wrap: wrap; gap: 1.5mm; margin-bottom: 3mm; }
.chip { font-size: 8pt; background: #f1f3f5; border-radius: 10mm; padding: 0.8mm 2.6mm; color: #495057; }
.chip.alvo { background: #ffe3d1; color: #c14a00; font-weight: 600; }
.fotos { display: flex; gap: 3mm; margin-bottom: 3mm; }
.fotos img { width: calc(50% - 1.5mm); max-height: 48mm; object-fit: cover; border-radius: 2mm; border: 1px solid #e9ecef; }
.corpo { display: flex; gap: 4mm; }
.passos { flex: 1; }
.passos ol { margin-left: 5mm; font-size: 9.5pt; }
.passos li { margin-bottom: 1.2mm; }
.video { width: 26mm; text-align: center; flex-shrink: 0; }
.video img { width: 24mm; height: 24mm; }
.video span { display: block; font-size: 7pt; color: #868e96; line-height: 1.3; margin-top: 1mm; }

/* Índice */
.indice h3 { font-size: 12pt; margin: 4mm 0 2mm; color: #e8590c; }
.indice ul { columns: 2; list-style: none; font-size: 9pt; }
.indice li { padding: 0.6mm 0; }
.rodape-final { margin-top: 10mm; padding-top: 4mm; border-top: 1px solid #dee2e6; font-size: 8pt; color: #868e96; }
"""


def main():
    secoes, ordem = {}, []
    for e in EX:
        if e["grupo"] not in secoes:
            secoes[e["grupo"]] = {"titulo": e["grupo_titulo"], "itens": []}
            ordem.append(e["grupo"])
        secoes[e["grupo"]]["itens"].append(e)

    partes = [f"<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'>"
              f"<title>Guia Completo de Exercícios</title><style>{CSS}</style></head><body>"]

    # Capa
    n_eq = len({e["equipamento"] for e in EX})
    partes.append(f"""
    <div class='pagina capa'>
      <div class='selo'>Guia Prático · Edição Completa</div>
      <h1>Guia Completo<br>de Exercícios</h1>
      <p class='sub'>{len(EX)} exercícios ilustrados com instruções passo a passo, fotos de execução e
      vídeos demonstrativos — para treinar em casa ou na academia.</p>
      <div class='stats'>
        <div class='stat'><b>{len(EX)}</b><span>exercícios</span></div>
        <div class='stat'><b>{len(ordem)}</b><span>grupos musculares</span></div>
        <div class='stat'><b>{n_eq}</b><span>tipos de equipamento</span></div>
        <div class='stat'><b>6</b><span>rotinas prontas</span></div>
      </div>
    </div>""")

    # Sumário
    caps = sorted(CAP_DIR.glob("*.md"))
    itens_sumario = "".join(
        f"<li>{html.escape(re.sub(r'^# ', '', c.read_text().split(chr(10))[0]))}</li>" for c in caps
    )
    itens_sumario += "".join(
        f"<li>{html.escape(secoes[g]['titulo'])} <span class='qtd'>({len(secoes[g]['itens'])} exercícios)</span></li>"
        for g in ordem
    )
    partes.append(f"<div class='pagina sumario'><h2>Sumário</h2><ol>{itens_sumario}"
                  f"<li>Índice por equipamento</li></ol></div>")

    # Capítulos
    for c in caps:
        partes.append(f"<div class='pagina capitulo'>{md_para_html(c.read_text())}</div>")

    # Seções de exercícios
    for idx, g in enumerate(ordem, 1):
        s = secoes[g]
        lista = "".join(f"<li>{html.escape(e['nome'])}</li>" for e in s["itens"])
        partes.append(f"""
        <div class='pagina divisor'>
          <div class='num'>{idx:02d}</div>
          <h2>{html.escape(s['titulo'])}</h2>
          <p>{len(s['itens'])} exercícios neste capítulo. Cada ficha traz músculo alvo, equipamento,
          nível, fotos da posição inicial e final, execução passo a passo e QR code com vídeos.</p>
          <ul>{lista}</ul>
        </div>""")
        cards = []
        for e in s["itens"]:
            chips = (
                f"<span class='chip alvo'>{html.escape(e['musculo_alvo'])}</span>"
                f"<span class='chip'>{html.escape(e['equipamento'])}</span>"
                f"<span class='chip'>{html.escape(e['nivel'])}</span>"
                f"<span class='chip'>{html.escape(e['mecanica'])}</span>"
            )
            if e["musculos_secundarios"]:
                sec = ", ".join(e["musculos_secundarios"][:3])
                chips += f"<span class='chip'>Auxiliares: {html.escape(sec)}</span>"
            fotos = "".join(f"<img src='../{p}' alt=''>" for p in e["imagens"])
            passos = "".join(f"<li>{html.escape(p)}</li>" for p in e["instrucoes"])
            cards.append(f"""
            <div class='exercicio'>
              <h3>{html.escape(e['nome'])}</h3>
              <div class='original'>{html.escape(e['nome_original'])}</div>
              <div class='chips'>{chips}</div>
              <div class='fotos'>{fotos}</div>
              <div class='corpo'>
                <div class='passos'><ol>{passos}</ol></div>
                <div class='video'><img src='../{e['qrcode']}' alt='QR'><span>Aponte a câmera<br>para ver vídeos</span></div>
              </div>
            </div>""")
        partes.append(f"<div class='pagina'>{''.join(cards)}</div>")

    # Índice por equipamento
    por_eq = {}
    for e in EX:
        por_eq.setdefault(e["equipamento"], []).append(e["nome"])
    blocos = "".join(
        f"<h3>{html.escape(eq)} ({len(nomes)})</h3><ul>" +
        "".join(f"<li>{html.escape(n)}</li>" for n in sorted(nomes)) + "</ul>"
        for eq, nomes in sorted(por_eq.items(), key=lambda kv: -len(kv[1]))
    )
    partes.append(f"""
    <div class='indice'><h2 class='cap-titulo'>Índice por Equipamento</h2>{blocos}
    <div class='rodape-final'>Fotos: free-exercise-db (domínio público). Conteúdo em português: original.
    Este material é educacional e não substitui orientação profissional individualizada.</div></div>""")

    partes.append("</body></html>")
    out = REPO / "build/guia.html"
    out.write_text("\n".join(partes), encoding="utf-8")
    print(f"OK -> {out} ({out.stat().st_size // 1024} KB, {len(EX)} exercícios)")


if __name__ == "__main__":
    main()
