"""Monta o livro 'Doces sem açúcar' em PDF (A5? não: A4) a partir do markdown exportado."""
import re, sys, html
import markdown
from weasyprint import HTML

S = sys.argv[1]
md_path = sys.argv[2]
out = sys.argv[3]
src = open(md_path, encoding="utf-8").read()

IMAGES = {
    "Bolo mole": ("bolo-mole-retro.png", "#3E9C9A"),
    "Brownie": ("brownie-retro.png", "#E2703A"),
    "Bolo de banana e canela": ("bolo-banana-retro.png", "#D9483B"),
    "Bolo de banana com mel": ("bolo-nozes-retro.png", "#7A8B3C"),
    "Mousse": ("mousse-retro.png", "#2F5D7C"),
    "Frutos secos": ("afogados-retro.png", "#B4527F"),
    "Panquecas": ("panquecas-retro.png", "#6C4F8C"),
    "Bolinhas": ("bolinhas-retro.png", "#2E7D5B"),
    "Muffins": ("muffins-retro.png", "#4F9FC4"),
    "Ahhh": ("nada-retro.png", "#8C5A3C"),
    "Tiramisu": ("tiramisu-retro.png", "#6B4A3A"),
    "Bolo de chocolate e feijão": ("feijao-retro.png", "#556B2F"),
    "Bolo Red Velvet": ("redvelvet-retro.png", "#C24A6A"),
    "Salame": ("salame-retro.png", "#2F6B4F"),
}


def md(t):
    return markdown.markdown(t, extensions=["tables", "sane_lists"])


def slug(t):
    t = t.lower()
    for a, b in zip("áàâãéêíóôõúçü", "aaaaeeiooouuu"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


src = src.replace("### Que receitas têm o quê", '<div class="pb"></div>\n\n### Que receitas têm o quê')
src = src.replace("### E os adoçantes?", '<div class="pb"></div>\n\n### E os adoçantes?')
# remove placeholders de imagens
src = re.sub(r"&#91;image:[^\n]*\n", "", src)
# divide em secções de nível 2
parts = re.split(r"^## ", src, flags=re.M)
sections = []
for p in parts[1:]:
    title, _, body = p.partition("\n")
    sections.append((title.strip(), body.strip()))

toc = []
pages = []


QR_BLOCK = f'''<div class="qrs">
  <div class="qr"><img src="file://{S}/qr-livro.png" alt=""><p><b>Este livro no telemóvel</b>Aponte a câmara para abrir as receitas online.<span>doces-sem-acucar-jv.vercel.app</span></p></div>
  <div class="qr"><img src="file://{S}/qr-receita.png" alt=""><p><b>Partilhe a sua receita</b>Envie-nos uma receita sem açúcar da sua família.<span>forms.gle/4NQwqCLPMVdaoxg66</span></p></div>
</div>'''


def section_page(title, body, extra_class=""):
    sid = slug(title)
    toc.append((title, sid, 0))
    extra = QR_BLOCK if title.startswith("Dicas para habituar") else ""
    return f'<section class="chapter {extra_class}" id="{sid}"><h2>{html.escape(title)}</h2>{md(body)}{extra}</section>'


def recipe_page(title, body):
    sid = slug(title)
    toc.append((title, sid, 1))
    img, color = next(((f, c) for k, (f, c) in IMAGES.items() if title.startswith(k)), (None, "#E2703A"))
    m = re.search(r"\*\*Ingredientes\*\*(.*?)\*\*Preparação\*\*(.*?)(\*\*Dica:\*\*.*)$", body, re.S)
    intro = body[: body.find("**Ingredientes**")].strip()
    ingr, prep, rest = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    # separa a dica do crédito (linha em itálico)
    credit = ""
    cm = re.search(r"\n\s*\*([^*\n]+)\*\s*$", rest)
    if cm:
        credit = cm.group(1)
        rest = rest[: cm.start()].strip()
    tip = rest.replace("**Dica:**", "").strip()
    tip = tip[:1].upper() + tip[1:]
    meta_lines = [l for l in intro.split("\n\n") if l.startswith("**Tempo")]
    desc = "\n\n".join(l for l in intro.split("\n\n") if not l.startswith("**Tempo"))
    meta = ""
    if meta_lines:
        items = [i.strip() for i in meta_lines[0].split("·")]
        meta = "".join(f'<span class="pill">{markdown.markdown(i)[3:-4]}</span>' for i in items)
    longcls = " long" if ingr.count("\n- ") + 1 > 9 else ""
    return f'''<section class="recipe{longcls}" id="{sid}" style="--accent:{color}">
  <h3 class="rtitle">{html.escape(title)}</h3>
  {f'<img class="hero" src="file://{S}/{img}">' if img else ''}
  <div class="desc">{md(desc)}</div>
  <div class="meta">{meta}</div>
  <div class="cols">
    <div class="ingr"><h4>Ingredientes</h4>{md(ingr)}</div>
    <div class="prep"><h4>Preparação</h4>{md(prep)}</div>
  </div>
  <div class="tip"><span class="tiplabel">Dica</span>{md(tip)}</div>
  {f'<p class="credit">{html.escape(credit)}</p>' if credit else ''}
</section>'''


for title, body in sections:
    if title == "Índice":
        continue
    if title == "Receitas":
        rparts = re.split(r"^### ", body, flags=re.M)
        sid = "receitas"
        toc.append(("Receitas", sid, 0))
        pages.append(f'<section class="divider" id="{sid}"><div class="dv"><p class="dvsmall">Mãos à obra!</p><h2>Receitas</h2><p class="dvsub">cada receita com ingredientes, preparação, tempo, doses e uma dica</p></div></section>')
        for rp in rparts[1:]:
            rt, _, rb = rp.partition("\n")
            pages.append(recipe_page(rt.strip(), rb.strip()))
    else:
        cls = "intro" if title in ("Introdução", "Agradecimentos") else ""
        pages.append(section_page(title, body, cls))

# índice com números de página
toc_html = "".join(
    f'<li class="lvl{lvl}"><a href="#{sid}">{html.escape(t)}</a></li>' for t, sid, lvl in toc
)

CSS = f'''
@font-face {{ font-family: "Pacifico"; src: url(file:///root/.fonts/pacifico-latin-400-normal.woff); }}
@font-face {{ font-family: "Fredoka"; src: url(file:///root/.fonts/fredoka-latin-400-normal.woff); }}
@font-face {{ font-family: "Fredoka"; font-weight: 600; src: url(file:///root/.fonts/fredoka-latin-600-normal.woff); }}
@page {{ size: A4; margin: 18mm 17mm 20mm 17mm; background: #FFFBF3;
  @bottom-center {{ content: counter(page); font-family: Fredoka; font-weight: 600; font-size: 10pt; color: #3B2414; }}
  @bottom-left {{ content: "Doces sem açúcar"; font-family: Pacifico; font-size: 10pt; color: #D9483B; }}
}}
@page cover {{ margin: 0; background: #F6E8CC; @bottom-center {{ content: none; }} @bottom-left {{ content: none; }} }}
@page divider {{ background: #3E9C9A; @bottom-center {{ content: none; }} @bottom-left {{ content: none; }} }}
body {{ font-family: Inter, "DejaVu Sans", sans-serif; font-size: 10.5pt; line-height: 1.5; color: #3B2414; }}
.cover {{ page: cover; height: 297mm; display: flex; align-items: center; justify-content: center; }}
.back {{ break-before: page; }}
.cover img {{ height: 285mm; }}
section, .toc {{ break-before: page; }}
h2 {{ font-family: Pacifico; font-weight: normal; font-size: 30pt; color: #D9483B; margin: 0 0 6mm; line-height: 1.2; }}
h2::after {{ content: ""; display: block; width: 40mm; height: 3px; margin-top: 3mm;
  background: repeating-linear-gradient(90deg, #E2703A 0 6px, transparent 6px 11px); }}
h3 {{ font-family: Fredoka; font-weight: 600; font-size: 14pt; color: #3E9C9A; margin: 7mm 0 2mm; }}
h4 {{ font-family: Fredoka; font-weight: 600; font-size: 12pt; color: var(--accent); margin: 0 0 2mm; text-transform: uppercase; letter-spacing: 1.5px; }}
p {{ margin: 0 0 3mm; }}
strong {{ color: #3B2414; }}
ul, ol {{ margin: 0 0 3mm; padding-left: 6mm; }}
li {{ margin-bottom: 1.2mm; }}
table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 2mm 0 5mm; font-size: 9.5pt;
  border: 2px solid #3B2414; border-radius: 6px; overflow: hidden; }}
th {{ background: #3E9C9A; color: #fff; font-family: Fredoka; font-weight: 600; text-align: left; padding: 2mm 3mm; }}
td {{ padding: 2mm 3mm; border-top: 1px solid #E8D9BF; vertical-align: top; }}
tr {{ break-inside: avoid; }}
.pb {{ break-before: page; }}
tr:nth-child(even) td {{ background: #FBF1DF; }}
.toc h2 {{ margin-bottom: 8mm; }}
.toc ul {{ list-style: none; padding: 0; font-family: Fredoka; font-size: 13pt; }}
.toc li {{ margin: 0 0 3.5mm; }}
.toc li.lvl1 {{ margin-left: 9mm; font-size: 12pt; margin-bottom: 2.5mm; }}
.toc li.lvl1::before {{ content: "● "; color: #E2703A; font-size: 8pt; }}
.toc a {{ color: #3B2414; text-decoration: none; }}
.toc a::after {{ content: leader(". ") target-counter(attr(href), page); color: #B07A44; }}
.intro p {{ font-size: 11.5pt; }}
.divider {{ page: divider; height: 255mm; display: flex; align-items: center; justify-content: center; }}
.dv {{ background: #F6E8CC; border: 5px solid #3B2414; border-radius: 30px; padding: 16mm 14mm; text-align: center; width: 140mm; }}
.dv h2 {{ font-size: 56pt; margin: 0; }}
.dv h2::after {{ margin: 3mm auto 0; }}
.dvsmall {{ font-family: Fredoka; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; font-size: 12pt; }}
.dvsub {{ font-family: Fredoka; font-size: 12pt; margin-top: 5mm; }}
.recipe .rtitle {{ font-family: Pacifico; font-weight: normal; font-size: 22pt; color: var(--accent); margin: 0 0 3mm; }}
.hero {{ display: block; width: 116mm; margin: 0 auto 3mm; border-radius: 10px; }}
.long .hero {{ width: 92mm; }}
.tip, .cols {{ break-inside: avoid; }}
#agradecimentos {{ break-before: auto; margin-top: 12mm; }}
.desc p {{ font-size: 11pt; font-style: italic; margin-bottom: 3mm; }}
.meta {{ margin-bottom: 5mm; }}
.pill {{ display: inline-block; background: #F6E8CC; border: 1.5px solid #3B2414; border-radius: 20px; padding: 1mm 3.5mm; margin: 0 2mm 2mm 0; font-size: 9.5pt; }}
.cols {{ display: flex; gap: 8mm; }}
.ingr {{ flex: 0 0 38%; background: #FBF1DF; border-radius: 10px; padding: 4mm 4mm 2mm; border-top: 5px solid var(--accent); }}
.prep {{ flex: 1; padding-top: 2mm; }}
.ingr ul {{ padding-left: 4.5mm; }}
.ingr li::marker {{ color: var(--accent); }}
.prep ol li::marker {{ color: var(--accent); font-family: Fredoka; font-weight: 600; }}
.tip {{ margin-top: 5mm; border: 2px dashed var(--accent); border-radius: 10px; padding: 3mm 4mm 1mm; position: relative; }}
.tiplabel {{ font-family: Fredoka; font-weight: 600; background: var(--accent); color: #fff; border-radius: 12px; padding: 0.5mm 3mm; font-size: 9.5pt; display: inline-block; margin-bottom: 2mm; text-transform: uppercase; letter-spacing: 1px; }}
.credit {{ font-family: Fredoka; text-align: right; margin-top: 4mm; color: var(--accent); }}
.qrs {{ display: flex; flex-direction: column; gap: 6mm; margin-top: 14mm; width: 130mm; break-inside: avoid; }}
.qr {{ flex: 1; display: flex; gap: 4mm; align-items: center; background: #F6E8CC; border: 2px solid #3B2414; border-radius: 12px; padding: 4mm; }}
.qr img {{ width: 40mm; height: 40mm; flex: none; border-radius: 4px; }}
.qr p {{ margin: 0; font-size: 9.5pt; }}
.qr b {{ display: block; font-family: Fredoka; font-weight: 600; font-size: 12pt; color: #D9483B; margin-bottom: 1mm; }}
.qr span {{ display: block; margin-top: 2mm; font-size: 8pt; color: #6E5440; word-break: break-all; }}
'''

A5 = len(sys.argv) > 4 and sys.argv[4] == "a5"
if A5:
    CSS += '''
@page { size: A5; margin: 11mm 11mm 14mm 11mm;
  @bottom-center { font-size: 8pt; } @bottom-left { font-size: 8pt; } }
body { font-size: 8.6pt; line-height: 1.42; }
.cover { height: 210mm; }
.cover img { height: 200mm; }
h2 { font-size: 21pt; margin-bottom: 4mm; }
h2::after { width: 28mm; margin-top: 2mm; }
h3 { font-size: 11pt; margin: 4mm 0 1.5mm; }
h4 { font-size: 9.5pt; letter-spacing: 1px; }
p { margin-bottom: 2mm; }
li { margin-bottom: 0.8mm; }
table { font-size: 7.4pt; }
th, td { padding: 1.3mm 2mm; }
.toc ul { font-size: 10pt; }
.toc li { margin-bottom: 2.2mm; }
.toc li.lvl1 { font-size: 9.2pt; margin-left: 6mm; margin-bottom: 1.6mm; }
.intro p { font-size: 9.2pt; }
.divider { height: 175mm; }
.dv { width: 100mm; padding: 11mm 9mm; border-width: 4px; }
.dv h2 { font-size: 38pt; }
.dvsmall, .dvsub { font-size: 9pt; }
section.recipe { break-before: left; }
.recipe .rtitle { font-size: 20pt; margin: 6mm 0 5mm; text-align: center; }
.hero, .long .hero { width: 126mm; margin-bottom: 6mm; }
.desc p { font-size: 10pt; margin-bottom: 4mm; text-align: center; }
.meta { margin-bottom: 3mm; text-align: center; }
.pill { font-size: 8.2pt; padding: 0.8mm 2.6mm; margin: 0 1.2mm 1.6mm 0; border-width: 1.2px; }
.cols { display: block; break-before: page; }
.ingr { padding: 3mm 3.5mm 1mm; margin-bottom: 4mm; }
.ingr ul { padding-left: 3.5mm; columns: 2; column-gap: 5mm; }
.ingr li { break-inside: avoid; }
.prep { padding-top: 0; }
.cols, .tip { font-size: 9.8pt; }
.recipe h4 { font-size: 10.5pt; }
.tiplabel { font-size: 8pt; }
.notes { break-before: page; }
.notes .line { border-bottom: 1px dashed #C9A27E; height: 8.6mm; }
.notes p { font-family: Fredoka; font-size: 10pt; }
.qrs { flex-direction: column; gap: 5mm; margin-top: 10mm; width: auto; }
.qr img { width: 30mm; height: 30mm; }
.qr p { font-size: 9pt; }
.qr b { font-size: 11pt; }
.tip { margin-top: 3mm; padding: 2mm 3mm 0.5mm; }
.tiplabel { font-size: 7.4pt; }
.credit { margin-top: 2mm; }
#agradecimentos { margin-top: 7mm; }
'''

NOTES = ""
if A5:
    import os
    _n = int(os.environ.get("NOTAS", "1"))  # páginas de notas: ajustar para o total do A5 ser múltiplo de 4
    NOTES = ('<section class="notes"><h2>As nossas notas</h2>'
             '<p>Uma receita sem açúcar da nossa família, ou as nossas adaptações:</p>'
             + '<div class="line"></div>' * 17 + '</section>') + ('<section class="notes"><div class="line"></div>' + '<div class="line"></div>' * 19 + '</section>') * (_n - 1)

doc = f'''<!doctype html><html lang="pt"><head><meta charset="utf-8"><title>Doces sem açúcar</title><style>{CSS}</style></head>
<body>
<div class="cover"><img src="file://{S}/capa.png"></div>
<div class="toc"><h2>Índice</h2><ul>{toc_html}</ul></div>
{"".join(pages)}
{NOTES}
<div class="cover back"><img src="file://{S}/contracapa.png"></div>
</body></html>'''
open(S + "/livro.html", "w", encoding="utf-8").write(doc)
HTML(string=doc, base_url=S).write_pdf(out)
print("ok")
