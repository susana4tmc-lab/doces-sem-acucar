import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, CREAM, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.CREAM, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
W, H = 1600, 400

def gingham(y, h):
    g = [f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="#FFF6EA"/>', f'<g fill="{CHERRY}" opacity="0.45">']
    g += [f'<rect x="{x}" y="{y}" width="20" height="{h}"/>' for x in range(0, W, 40)]
    g.append(f'</g><g fill="{CHERRY}" opacity="0.45">')
    g += [f'<rect x="0" y="{yy}" width="{W}" height="20"/>' for yy in range(y, y + h, 40)]
    g.append('</g>')
    return "\n".join(g)

def apple(tx, ty, s=1.0):
    return f'''<g transform="translate({tx} {ty}) scale({s})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M0 -26 Q-34 -40 -40 -4 Q-40 32 -10 36 Q0 32 10 36 Q40 32 40 -4 Q34 -40 0 -26 Z" fill="{CHERRY}"/>
  <path d="M0 -26 Q2 -40 8 -46" fill="none"/>
  <path d="M6 -38 Q22 -54 34 -42 Q20 -30 6 -38 Z" fill="#7FB069" stroke-width="3"/>
  <path d="M-24 -10 Q-26 2 -20 12" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round"/>
</g>'''

def muffin(x, y, s=1.0, cup=MUSTARD):
    return f'''<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M-34 0 L34 0 L26 36 L-26 36 Z" fill="{cup}"/>
  <path d="M-40 2 Q-46 -20 -26 -32 Q-10 -46 8 -40 Q30 -44 40 -24 Q48 -6 40 2 Z" fill="#C98A45"/>
  <path d="M-12 -30 L4 -34 L6 -24 L-10 -20 Z" fill="#F6E7B8" stroke-width="2.5"/>
</g>'''

def pencil(x, y, rot):
    return f'''<g transform="translate({x} {y}) rotate({rot})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <rect x="-70" y="-10" width="120" height="20" fill="{MUSTARD}"/>
  <rect x="-86" y="-10" width="16" height="20" fill="#F2A7A0"/>
  <path d="M50 -10 L76 0 L50 10 Z" fill="#F3D9B1"/>
  <path d="M68 -3 L76 0 L68 3 Z" fill="{INK}"/>
</g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<rect width="{W}" height="{H}" fill="{TEAL}"/>
{r.halftone(0, 0, W, 300, step=18, color="#FFFFFF", op=0.16)}
{r.sunburst(800, 470, 760, n=36)}
<circle cx="800" cy="470" r="300" fill="#F7D58E"/>
{gingham(310, 90)}
<rect x="0" y="310" width="{W}" height="6" fill="{INK}" opacity="0.15"/>
{r.star(150, 70, 18, "#FFFFFF")}{r.star(1450, 90, 14, "#FFFFFF")}{r.star(1380, 40, 8, CREAM)}{r.star(240, 140, 9, CREAM)}
<!-- cartão de receita / título -->
<g transform="translate(800 178)">
  <rect x="-430" y="-122" width="860" height="230" rx="64" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>
  <rect x="-414" y="-106" width="828" height="198" rx="52" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="9 9"/>
  <text x="0" y="-12" text-anchor="middle" font-family="Pacifico" font-size="70" fill="{CHERRY}">Partilhe a sua receita</text>
  <text x="0" y="56" text-anchor="middle" font-family="Fredoka SemiBold" font-size="26" letter-spacing="5" fill="{INK}">DOCES SEM AÇÚCAR · RECEITAS PARA A FAMÍLIA</text>
</g>
{r.banana(70, 250, -10, 1.15)}
{apple(330, 352, 1.05)}
{muffin(1270, 340, 1.15, TEAL)}
{muffin(1390, 352, 1.0, CHERRY)}
{pencil(1500, 300, -30)}
</svg>'''
open(S + "/banner-formulario.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/banner-formulario.png", output_width=1600)
print("ok")
