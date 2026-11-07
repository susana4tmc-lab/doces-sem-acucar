"""Ícone da app 'Doces sem açúcar' (estilo retro do livro) em vários tamanhos + favicon."""
import importlib.util, sys, math
S = sys.argv[1]; OUT = sys.argv[2]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, CREAM, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.CREAM, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
N = 512

def rays(cx, cy, rad, n=20):
    out = []
    for i in range(0, n, 2):
        a1, a2 = 2*math.pi*i/n, 2*math.pi*(i+1)/n
        out.append(f'<path d="M{cx} {cy} L{cx+rad*math.cos(a1):.1f} {cy+rad*math.sin(a1):.1f} L{cx+rad*math.cos(a2):.1f} {cy+rad*math.sin(a2):.1f} Z" fill="{MUSTARD}"/>')
    return "".join(out)

def icon(full_bleed=True):
    # conteúdo dentro da zona segura central (~80%) para ícones "maskable"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}" width="{N}" height="{N}">
<rect width="{N}" height="{N}" fill="{TEAL}"/>
{r.halftone(0, 0, N, N, step=22, color="#FFFFFF", op=0.16)}
<circle cx="256" cy="268" r="236" fill="#F2C46A"/>
{rays(256, 268, 236)}
<circle cx="256" cy="268" r="150" fill="#F7D58E"/>
<!-- muffin -->
<g transform="translate(256 300) scale(3.1)" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round">
  <path d="M-34 0 L34 0 L26 36 L-26 36 Z" fill="{CHERRY}"/>
  <path d="M-24 4 L-20 33 M-12 4 L-10 33 M0 4 L0 33 M12 4 L10 33 M24 4 L20 33" stroke-width="1.6" opacity="0.5"/>
  <path d="M-40 2 Q-46 -20 -26 -32 Q-10 -46 8 -40 Q30 -44 40 -24 Q48 -6 40 2 Z" fill="#C98A45"/>
  <path d="M-14 -26 L2 -30 L4 -20 L-12 -16 Z" fill="#F6E7B8" stroke-width="2"/>
  <path d="M10 -18 L24 -22 L26 -12 L12 -8 Z" fill="#F6E7B8" stroke-width="2"/>
  <path d="M2 -40 Q4 -52 14 -56" fill="none" stroke-width="2.6"/>
  <path d="M12 -54 Q24 -64 32 -54 Q22 -46 12 -54 Z" fill="#7FB069" stroke-width="2"/>
</g>
{r.star(118, 112, 22, "#FFFFFF")}{r.star(402, 132, 15, "#FFFFFF")}
</svg>'''

svg = icon()
open(OUT + "/icone.svg", "w").write(svg)
for size, name in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (48, "favicon-48.png"), (32, "favicon-32.png")]:
    r.cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{OUT}/{name}", output_width=size, output_height=size)
print("ok")
