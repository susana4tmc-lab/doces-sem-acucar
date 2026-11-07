"""Gera a versão online (telemóvel) do livro 'Doces sem açúcar' a partir do markdown exportado."""
import re, sys, json, html
import markdown

S, md_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(md_path, encoding="utf-8").read()
src = re.sub(r"&#91;image:[^\n]*\n", "", src)

IMG = [
    ("Bolo mole", "bolo-mole", "#3E9C9A"), ("Brownie", "brownie", "#E2703A"),
    ("Bolo de banana e canela", "bolo-banana", "#D9483B"), ("Bolo de banana com mel", "bolo-nozes", "#7A8B3C"),
    ("Mousse", "mousse", "#2F5D7C"), ("Frutos secos", "afogados", "#B4527F"),
    ("Panquecas", "panquecas", "#6C4F8C"), ("Bolinhas", "bolinhas", "#2E7D5B"),
    ("Muffins", "muffins", "#4F9FC4"), ("Ahhh", "nada", "#8C5A3C"),
    ("Tiramisu", "tiramisu", "#6B4A3A"), ("Bolo de chocolate e feijão", "feijao", "#556B2F"),
    ("Bolo Red Velvet", "redvelvet", "#C24A6A"),
    ("Salame", "salame", "#2F6B4F"),
]


def md(t):
    return markdown.markdown(t, extensions=["tables", "sane_lists"])


def slug(t):
    t = t.lower()
    for a, b in zip("áàâãéêíóôõúçü", "aaaaeeiooouc u".replace(" ", "u")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:48].strip("-")


def items(block):
    return [re.sub(r"^\s*(?:-|\d+\.)\s+", "", l).strip() for l in block.strip().split("\n") if l.strip()]


def inline(t):
    h = markdown.markdown(t)
    return h[3:-4] if h.startswith("<p>") else h


parts = re.split(r"^## ", src, flags=re.M)
sections = [(p.partition("\n")[0].strip(), p.partition("\n")[2].strip()) for p in parts[1:]]

# alergénios a partir da tabela
allerg = {}
m = re.search(r"\| Receita \| Glúten.*?\n\| ---.*?\n((?:\|.*\n?)+)", src)
if m:
    for row in m.group(1).strip().split("\n"):
        c = [x.strip() for x in row.strip("|").split("|")]
        allerg[c[0]] = {"gluten": c[1], "lactose": c[2], "ovo": c[3], "frutos": c[4]}

recipes, chapters = [], []
for title, body in sections:
    if title == "Índice":
        continue
    if title == "Receitas":
        for rp in re.split(r"^### ", body, flags=re.M)[1:]:
            rt, _, rb = rp.partition("\n")
            rt = rt.strip()
            mm = re.search(r"\*\*Ingredientes\*\*(.*?)\*\*Preparação\*\*(.*?)\*\*Dica:\*\*(.*)$", rb, re.S)
            intro = rb[: rb.find("**Ingredientes**")].strip()
            meta_line = next((l for l in intro.split("\n\n") if l.startswith("**Tempo")), "")
            desc = "\n\n".join(l for l in intro.split("\n\n") if not l.startswith("**Tempo"))
            meta = {}
            for it in meta_line.split("·"):
                k, _, v = it.partition(":**")
                if v:
                    meta[k.replace("**", "").strip()] = v.strip()
            rest = mm.group(3).strip()
            credit = ""
            cm = re.search(r"\n\s*\*([^*\n]+)\*\s*$", rest)
            if cm:
                credit, rest = cm.group(1), rest[: cm.start()].strip()
            tip = rest[:1].upper() + rest[1:]
            img, color = next(((f, c) for k, f, c in IMG if rt.startswith(k)), ("capa", "#E2703A"))
            al = next((v for k, v in allerg.items() if k.split("…")[0][:18] == rt.split("…")[0][:18]), None)
            recipes.append({
                "id": slug(rt), "title": rt, "desc": inline(desc), "meta": meta, "img": f"img/{img}.jpg",
                "color": color, "ingr": [inline(x) for x in items(mm.group(1))],
                "prep": [inline(x) for x in items(mm.group(2))], "tip": inline(tip), "credit": credit,
                "allerg": al,
            })
    else:
        chapters.append({"id": "ler-" + slug(title), "title": title, "html": md(body)})

DATA = json.dumps({"recipes": recipes, "chapters": chapters}, ensure_ascii=False)

page = r'''<!doctype html>
<html lang="pt">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Doces sem açúcar</title>
<meta name="description" content="Receitas doces sem açúcar para as famílias da EB João Villaret. Dia da Alimentação 2026, Saúde Escolar UCC Loures.">
<meta name="theme-color" content="#2F8B89">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="icons/favicon-48.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="Doces">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta property="og:title" content="Doces sem açúcar — Receitas para a família">
<meta property="og:description" content="Receitas doces sem açúcar da EB João Villaret.">
<meta property="og:image" content="img/capa.jpg">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pacifico&family=Fredoka:wght@400;500;600&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700&display=swap">
<style>
/* Layout: caderno de receitas retro de uma coluna, cartões de receita em grelha que passa a uma coluna no telemóvel */
:root {
  --paper: #FFF8EC; --card: #FFFFFF; --cream: #F6E8CC; --ink: #3B2414; --ink-soft: #6E5440;
  --teal: #2F8B89; --cherry: #C93A2E; --mustard: #E3A23A; --line: #E9D9BF; --chip: #F6E8CC;
  --display: "Pacifico", "Brush Script MT", cursive;
  --label: "Fredoka", "Trebuchet MS", system-ui, sans-serif;
  --body: "Nunito Sans", "Segoe UI", system-ui, sans-serif;
  --lift: 0%;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #22180F; --card: #2E2217; --cream: #3A2B1D; --ink: #F5E8D2; --ink-soft: #C9B396;
  --teal: #5FC2BF; --cherry: #F0705F; --mustard: #F0B95A; --line: #4A3826; --chip: #3A2B1D; --lift: 55%; color-scheme: dark } }
:root[data-theme="dark"] {
  --paper: #22180F; --card: #2E2217; --cream: #3A2B1D; --ink: #F5E8D2; --ink-soft: #C9B396;
  --teal: #5FC2BF; --cherry: #F0705F; --mustard: #F0B95A; --line: #4A3826; --chip: #3A2B1D; --lift: 55%; color-scheme: dark }

* { box-sizing: border-box; }
:root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
html { color-scheme: light; }
img { max-width: 100%; }
[hidden] { display: none !important; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--body); font-size: 17px; line-height: 1.55;
  -webkit-text-size-adjust: 100%; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--teal); }
.wrap { max-width: 760px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
h1, h2 { font-family: var(--display); font-weight: 400; color: var(--cherry); line-height: 1.25; text-wrap: balance; margin: 0; }
h3 { font-family: var(--label); font-weight: 600; color: var(--teal); margin: 1.4em 0 .4em; font-size: 1.08rem; }
a { color: var(--teal); }
button { font: inherit; color: inherit; cursor: pointer; }
:focus-visible { outline: 3px solid var(--mustard); outline-offset: 2px; border-radius: 6px; }

/* barra superior */
.bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--teal); color: #fff;
  border-bottom: 4px solid var(--ink); }
.bar .wrap { display: flex; align-items: center; gap: 10px; min-height: 56px; }
.bar .brand { font-family: var(--display); font-size: 1.35rem; color: #fff; text-decoration: none; white-space: nowrap; }
.bar .back { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,.16); border: 0; border-radius: 999px;
  padding: 6px 14px 6px 10px; font-family: var(--label); font-weight: 500; color: #fff; }
.bar .back[hidden] { display: none; }
.bar .spacer { flex: 1; }

/* capa */
.hero { background: var(--teal); background-image: radial-gradient(rgba(255,255,255,.18) 1.6px, transparent 1.8px); background-size: 16px 16px;
  border-bottom: 4px solid var(--ink); }
.hero .wrap { padding-block: 26px 30px; display: grid; gap: 18px; justify-items: center; text-align: center; }
.badge { background: var(--cream); border: 4px solid var(--ink); border-radius: 44px; padding: 16px 26px 14px; box-shadow: 0 6px 0 rgba(0,0,0,.18); max-width: 100%; }
.badge h1 { font-size: clamp(2.3rem, 9vw, 3.4rem); }
.badge p { margin: 4px 0 0; font-family: var(--label); font-weight: 600; letter-spacing: .18em; text-transform: uppercase; font-size: .78rem; color: var(--ink); }
.ribbon { background: var(--cherry); color: #fff; border: 3px solid var(--ink); border-radius: 6px; padding: 6px 18px; font-family: var(--label); font-weight: 600; }
.hero .sub { color: #fff; font-family: var(--label); font-size: .95rem; margin: 0; }

section.block { padding-block: 26px 8px; }
.sechead { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 14px; }
.sechead h2 { font-size: 1.9rem; }
.sechead span { font-family: var(--label); color: var(--ink-soft); font-size: .9rem; }

/* filtro */
.filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 16px; }
.filters button { border: 2px solid var(--ink); background: var(--card); border-radius: 999px; padding: 5px 13px; font-family: var(--label); font-size: .88rem; }
.filters button[aria-pressed="true"] { background: var(--ink); color: var(--paper); }

/* cartões */
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.rcard { display: grid; grid-template-rows: auto 1fr; text-decoration: none; color: inherit; background: var(--card); border: 3px solid var(--ink);
  border-radius: 18px; overflow: hidden; transition: transform .15s ease; }
.rcard:hover { transform: translateY(-3px); }
.rcard img { display: block; width: 100%; aspect-ratio: 800/460; object-fit: cover; border-bottom: 3px solid var(--ink); }
.rcard .t { padding: 10px 14px 14px; display: grid; gap: 6px; align-content: start; }
[style*="--c"] { --ct: color-mix(in srgb, var(--c), #fff var(--lift)); }
.rcard .t b { font-family: var(--label); font-weight: 600; font-size: 1.05rem; line-height: 1.25; color: var(--ct); }
.rcard .t small { color: var(--ink-soft); font-size: .86rem; }
.empty { padding: 16px; border: 2px dashed var(--line); border-radius: 14px; color: var(--ink-soft); }

.reads { display: grid; gap: 10px; }
.reads a { display: flex; align-items: center; justify-content: space-between; gap: 10px; background: var(--card); border: 2px solid var(--line);
  border-radius: 14px; padding: 14px 16px; text-decoration: none; color: var(--ink); font-family: var(--label); font-weight: 500; }
.reads a::after { content: "›"; font-size: 1.4rem; color: var(--cherry); line-height: 1; }
.partners { padding-block: 26px 40px; text-align: center; }
.partners img { width: min(420px, 100%); border-radius: 22px; }

/* receita */
.rhead { padding-block: 18px 6px; display: grid; gap: 12px; }
.rhead img { width: 100%; border-radius: 18px; border: 3px solid var(--ink); }
.rhead h1 { font-size: clamp(1.9rem, 7.5vw, 2.6rem); color: var(--ct); }
.desc { margin: 0; font-style: italic; color: var(--ink-soft); }
.pills { display: flex; flex-wrap: wrap; gap: 8px; }
.pill { background: var(--chip); border: 2px solid var(--ink); border-radius: 999px; padding: 3px 12px; font-size: .88rem; }
.pill b { font-family: var(--label); font-weight: 600; }
.al { display: flex; flex-wrap: wrap; gap: 6px; }
.al span { font-family: var(--label); font-size: .8rem; border-radius: 6px; padding: 2px 8px; border: 1.5px solid var(--line); color: var(--ink-soft); }
.al span.yes { border-color: var(--cherry); color: var(--cherry); }
.panel { background: var(--card); border: 2px solid var(--line); border-top: 6px solid var(--c); border-radius: 16px; padding: 14px 16px 10px; margin-top: 16px; }
.panel h2 { font-family: var(--label); font-weight: 600; font-size: .95rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ct); margin-bottom: 8px; }
.panel .hint { font-size: .82rem; color: var(--ink-soft); margin: -4px 0 8px; }
.ingr { list-style: none; margin: 0; padding: 0; }
.ingr li + li { border-top: 1px dashed var(--line); }
.ingr label { display: flex; gap: 12px; align-items: flex-start; padding: 9px 2px; cursor: pointer; }
.ingr input { appearance: none; flex: none; width: 22px; height: 22px; margin-top: 2px; border: 2px solid var(--ct); border-radius: 6px; display: grid; place-items: center; background: var(--card); }
.ingr input:checked { background: var(--c); }
.ingr input:checked::after { content: ""; width: 6px; height: 11px; border: solid #fff; border-width: 0 3px 3px 0; transform: rotate(45deg) translate(-1px,-1px); }
.ingr input:checked + span { text-decoration: line-through; color: var(--ink-soft); }
.steps { margin: 0; padding: 0; list-style: none; counter-reset: s; }
.steps li { counter-increment: s; display: grid; grid-template-columns: 34px 1fr; gap: 10px; padding: 9px 0; }
.steps li + li { border-top: 1px dashed var(--line); }
.steps li::before { content: counter(s); width: 30px; height: 30px; border-radius: 50%; background: var(--c); color: #fff; display: grid; place-items: center;
  font-family: var(--label); font-weight: 600; }
.tip { margin-top: 16px; border: 2.5px dashed var(--ct); border-radius: 16px; padding: 12px 16px; }
.tip strong { display: inline-block; font-family: var(--label); font-weight: 600; background: var(--c); color: #fff; border-radius: 8px; padding: 1px 10px; font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 6px; }
.tip p { margin: 0; }
.credit { text-align: right; font-family: var(--label); color: var(--ct); margin: 10px 0 0; }
.tools { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
.tools button { border: 2px solid var(--ink); background: var(--card); border-radius: 999px; padding: 8px 16px; font-family: var(--label); font-weight: 500; }
.tools button[aria-pressed="true"] { background: var(--mustard); color: #3B2414; }
.tools small { flex-basis: 100%; color: var(--ink-soft); font-size: .82rem; }
.pager { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding-block: 22px 40px; }
.pager a { display: grid; gap: 2px; text-decoration: none; color: var(--ink); background: var(--card); border: 2px solid var(--line); border-radius: 14px; padding: 10px 14px; min-width: 0; }
.pager a small { font-family: var(--label); color: var(--ink-soft); font-size: .78rem; }
.pager a span { font-family: var(--label); font-weight: 500; overflow-wrap: anywhere; }
.pager a.next { text-align: right; grid-column: 2; }

/* capítulos */
.read { padding-block: 20px 40px; }
.read h1 { font-size: clamp(1.9rem, 7.5vw, 2.5rem); margin-bottom: 12px; }
.read p, .read li { max-width: 65ch; }
.read ul, .read ol { padding-left: 1.3em; }
.read li { margin-bottom: .35em; }
.tbl { overflow-x: auto; margin: 10px 0 16px; border: 2px solid var(--ink); border-radius: 12px; }
.tbl table { border-collapse: collapse; width: 100%; font-size: .9rem; min-width: 520px; }
.tbl th { background: var(--teal); color: #fff; font-family: var(--label); font-weight: 600; text-align: left; padding: 8px 10px; }
.tbl td { padding: 8px 10px; border-top: 1px solid var(--line); vertical-align: top; }
.tbl tr:nth-child(even) td { background: var(--chip); }
.share { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px 20px;
  background: var(--cream); border: 3px solid var(--ink); border-radius: 22px; padding: 18px 20px; }
.share > div { flex: 1 1 280px; min-width: 0; }
.share h2 { font-size: 1.6rem; }
.share p { margin: 6px 0 0; }
.cta { display: inline-block; background: var(--cherry); color: #fff; border: 3px solid var(--ink); border-radius: 999px; padding: 10px 20px;
  font-family: var(--label); font-weight: 600; text-decoration: none; box-shadow: 0 4px 0 var(--ink); }
.cta:active { transform: translateY(2px); box-shadow: 0 2px 0 var(--ink); }
.sharelink { flex-basis: 100%; font-family: var(--label); font-weight: 500; color: var(--ct); }
.foot { text-align: center; padding-block: 0 34px; color: var(--ink-soft); font-size: .85rem; font-family: var(--label); }
@media (prefers-reduced-motion: reduce) { .rcard { transition: none; } .rcard:hover { transform: none; } }
</style>

<header class="bar"><div class="wrap">
  <a class="brand" href="#">Doces sem açúcar</a>
  <span class="spacer"></span>
  <button class="back" id="back" type="button" hidden>‹ Receitas</button>
</div></header>
<main id="app"></main>

<script>
const DATA = __DATA__;
const FORM = "https://forms.gle/4NQwqCLPMVdaoxg66";
const app = document.getElementById("app");
const back = document.getElementById("back");
back.addEventListener("click", () => { location.hash = ""; });
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const store = {
  get(k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
};
const FILTERS = [["todas", "Todas"], ["gluten", "Sem glúten"], ["lactose", "Sem lactose"], ["ovo", "Sem ovo"], ["frutos", "Sem frutos secos"], ["forno", "Sem forno"]];
let filter = "todas";
const ALN = { gluten: "Glúten", lactose: "Lactose", ovo: "Ovo", frutos: "Frutos secos" };
const free = (r, k) => {
  if (k === "forno") return /não precisa/i.test(r.meta.Forno || "");
  if (!r.allerg) return false;
  const v = r.allerg[k] || "";
  if (k === "gluten" && v.startsWith("Aveia")) return true;
  return v === "—" || v === "Opcional";
};

function home() {
  back.hidden = true;
  const list = DATA.recipes.filter(r => filter === "todas" || free(r, filter));
  app.innerHTML = `
  <div class="hero"><div class="wrap">
    <div class="badge"><h1>Doces sem açúcar</h1><p>Receitas para a família</p></div>
    <div class="ribbon">a fruta adoça, com casca e tudo!</div>
    <p class="sub">Dia da Alimentação 2026 · EB João Villaret · Saúde Escolar UCC Loures</p>
  </div></div>
  <section class="block wrap" aria-labelledby="h-rec">
    <div class="sechead"><h2 id="h-rec">Receitas</h2><span>${list.length} de ${DATA.recipes.length}</span></div>
    <div class="filters" role="group" aria-label="Filtrar receitas">
      ${FILTERS.map(([k, l]) => `<button type="button" data-f="${k}" aria-pressed="${k === filter}">${l}</button>`).join("")}
    </div>
    ${filter === "gluten" ? `<p class="hint" style="margin:-6px 0 14px;font-size:.85rem;color:var(--ink-soft)">Inclui receitas com aveia: usar aveia certificada sem glúten.</p>` : ""}
    <div class="grid">
      ${list.map(r => `<a class="rcard" href="#${r.id}" style="--c:${r.color}">
        <img src="${r.img}" alt="" loading="lazy">
        <span class="t"><b>${esc(r.title)}</b><small>${esc(r.meta.Tempo || "")}</small></span></a>`).join("") ||
        `<p class="empty">Nenhuma receita com este filtro.</p>`}
    </div>
  </section>
  <section class="block wrap"><div class="share">
    <div><h2>Tem uma receita sem açúcar?</h2>
    <p>Partilhe-a connosco. A equipa de Saúde Escolar lê todas as receitas e algumas entram na próxima edição do livro.</p></div>
    <a class="cta" href="${FORM}" target="_blank" rel="noopener">Partilhar a minha receita</a>
  </div></section>
  <section class="block wrap" aria-labelledby="h-ler">
    <div class="sechead"><h2 id="h-ler">Para saber mais</h2></div>
    <div class="reads">${DATA.chapters.map(c => `<a href="#${c.id}">${esc(c.title)}</a>`).join("")}</div>
  </section>
  <section class="partners wrap"><img src="img/contracapa.jpg" alt="Obrigado! Um livro feito em parceria: Agrupamento de Escolas João Villaret, Associação de Pais e UCC Loures."></section>`;
  app.querySelectorAll("[data-f]").forEach(b => b.addEventListener("click", () => { filter = b.dataset.f; home(); }));
}

let wake = null;
async function toggleWake(btn) {
  if (wake) { try { await wake.release(); } catch (e) {} wake = null; btn.setAttribute("aria-pressed", "false"); return; }
  try { wake = await navigator.wakeLock.request("screen"); btn.setAttribute("aria-pressed", "true");
    wake.addEventListener("release", () => { wake = null; btn.setAttribute("aria-pressed", "false"); });
  } catch (e) { btn.nextElementSibling.textContent = "Este telemóvel não permite manter o ecrã ligado a partir desta página."; }
}

function recipe(r) {
  back.hidden = false;
  const i = DATA.recipes.indexOf(r), prev = DATA.recipes[i - 1], next = DATA.recipes[i + 1];
  const done = store.get("chk-" + r.id) || [];
  const al = r.allerg ? Object.entries(ALN).map(([k, l]) => {
    const v = r.allerg[k]; const yes = v && v !== "—";
    return `<span class="${yes ? "yes" : ""}">${yes ? l + (v === "Sim" ? "" : ": " + esc(v)) : "Sem " + l.toLowerCase()}</span>`; }).join("") : "";
  app.innerHTML = `<article class="wrap" style="--c:${r.color}">
    <div class="rhead">
      <img src="${r.img}" alt="Ilustração: ${esc(r.title)}">
      <h1>${esc(r.title)}</h1>
      <p class="desc">${r.desc}</p>
      <div class="pills">${Object.entries(r.meta).map(([k, v]) => `<span class="pill"><b>${esc(k)}:</b> ${esc(v)}</span>`).join("")}</div>
      ${al ? `<div class="al" aria-label="Alergénios">${al}</div>` : ""}
    </div>
    <div class="panel"><h2>Ingredientes</h2><p class="hint">Toque para riscar o que já juntou.</p>
      <ul class="ingr">${r.ingr.map((x, n) => `<li><label><input type="checkbox" id="i-${r.id}-${n}" data-n="${n}" ${done.includes(n) ? "checked" : ""}><span>${x}</span></label></li>`).join("")}</ul>
    </div>
    <div class="panel"><h2>Preparação</h2><ol class="steps">${r.prep.map(x => `<li><span>${x}</span></li>`).join("")}</ol></div>
    <div class="tip"><strong>Dica</strong><p>${r.tip}</p></div>
    ${r.credit ? `<p class="credit">${esc(r.credit)}</p>` : ""}
    <div class="tools">
      <button type="button" id="wake" aria-pressed="${wake ? "true" : "false"}">Manter o ecrã ligado</button><small></small>
      <button type="button" id="clear">Limpar ingredientes riscados</button>
      <a class="sharelink" href="${FORM}" target="_blank" rel="noopener">Partilhar uma receita da minha família ›</a>
    </div>
    <nav class="pager" aria-label="Outras receitas">
      ${prev ? `<a href="#${prev.id}"><small>‹ Anterior</small><span>${esc(prev.title)}</span></a>` : "<span></span>"}
      ${next ? `<a class="next" href="#${next.id}"><small>Seguinte ›</small><span>${esc(next.title)}</span></a>` : ""}
    </nav>
  </article>`;
  app.querySelectorAll(".ingr input").forEach(cb => cb.addEventListener("change", () => {
    const sel = [...app.querySelectorAll(".ingr input:checked")].map(c => +c.dataset.n); store.set("chk-" + r.id, sel); }));
  document.getElementById("clear").addEventListener("click", () => {
    app.querySelectorAll(".ingr input").forEach(c => c.checked = false); store.set("chk-" + r.id, []); });
  const wb = document.getElementById("wake");
  if (!("wakeLock" in navigator)) { wb.hidden = true; wb.nextElementSibling.hidden = true; }
  else wb.addEventListener("click", () => toggleWake(wb));
}

function chapter(c) {
  back.hidden = false;
  app.innerHTML = `<article class="read wrap"><h1>${esc(c.title)}</h1>${c.html}</article>`;
  app.querySelectorAll(".read table").forEach(t => { const d = document.createElement("div"); d.className = "tbl"; t.replaceWith(d); d.appendChild(t); });
  app.querySelectorAll(".read a[href^='http']").forEach(a => { a.target = "_blank"; a.rel = "noopener"; });
}

function route() {
  const id = decodeURIComponent(location.hash.slice(1));
  const r = DATA.recipes.find(x => x.id === id), c = DATA.chapters.find(x => x.id === id);
  if (r) recipe(r); else if (c) chapter(c); else home();
  window.scrollTo(0, 0);
  if (r || c) document.title = (r || c).title + " · Doces sem açúcar"; else document.title = "Doces sem açúcar";
}
window.addEventListener("hashchange", route);
route();
</script>
'''.replace("__DATA__", DATA)
open(out, "w", encoding="utf-8").write(page)
print(len(recipes), "receitas;", len(chapters), "capítulos;", sum(1 for r in recipes if r["allerg"]), "com alergénios")
for r in recipes:
    print(r["id"], "|", r["meta"].get("Forno"), "|", r["allerg"] is not None)
