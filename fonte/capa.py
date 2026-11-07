import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, CREAM, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.CREAM, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
W, H = 600, 820


def gingham(y, h):
    g = [f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="#FFF6EA"/>', f'<g fill="{CHERRY}" opacity="0.45">']
    g += [f'<rect x="{x}" y="{y}" width="20" height="{h}"/>' for x in range(0, W, 40)]
    g.append(f'</g><g fill="{CHERRY}" opacity="0.45">')
    g += [f'<rect x="0" y="{yy}" width="{W}" height="20"/>' for yy in range(y, y + h, 40)]
    g.append('</g>')
    return "\n".join(g)


def cake_round(tx, ty, s=1.0):
    return f'''<g transform="translate({tx} {ty}) scale({s})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <ellipse cx="0" cy="40" rx="110" ry="22" fill="#FFFFFF"/>
  <path d="M-85 0 L-85 38 Q0 58 85 38 L85 0 Z" fill="{MUSTARD}"/>
  <ellipse cx="0" cy="0" rx="85" ry="18" fill="{ORANGE}"/>
  <g fill="#FFFFFF" stroke="none">{"".join(f'<rect x="{x}" y="{y}" width="8" height="3" rx="1.5" transform="rotate({a} {x} {y})"/>' for x,y,a in [(-50,-4,20),(-25,4,-30),(0,-8,40),(25,2,-10),(48,-6,60),(-10,8,10),(15,-12,-45),(-38,-12,30)])}</g>
</g>'''


def brownies(tx, ty):
    return f'<g transform="translate({tx} {ty})">' + r.brownie_sq(0, 0) + r.brownie_sq(78, 0, banana_top=True) + r.brownie_sq(36, 34, dots=((20, 14), (50, 20))) + '</g>'


def loaf(tx, ty):
    return f'''<g transform="translate({tx} {ty})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M0 0 L0 50 L150 50 L150 0 Z" fill="#B8733C"/>
  <path d="M150 0 L176 -10 L176 40 L150 50 Z" fill="#9C5A2C"/>
  <path d="M0 0 Q0 -30 60 -32 L130 -34 Q176 -34 176 -10 L150 0 Q80 10 0 0 Z" fill="#9C5A2C"/>
  <path d="M20 -12 Q80 -28 140 -24 Q146 -18 140 -14 Q80 -14 24 -2 Q14 -6 20 -12 Z" fill="#F6E3A1" stroke-width="3"/>
</g>'''


def apple(tx, ty):
    return f'''<g transform="translate({tx} {ty})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M0 -26 Q-34 -40 -40 -4 Q-40 32 -10 36 Q0 32 10 36 Q40 32 40 -4 Q34 -40 0 -26 Z" fill="{CHERRY}"/>
  <path d="M0 -26 Q2 -40 8 -46" fill="none"/>
  <path d="M6 -38 Q22 -54 34 -42 Q20 -30 6 -38 Z" fill="#7FB069" stroke-width="3"/>
  <path d="M-24 -10 Q-26 2 -20 12" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round"/>
</g>'''


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*2}" height="{H*2}">
<defs><clipPath id="c"><rect x="16" y="16" width="{W-32}" height="{H-32}" rx="40"/></clipPath></defs>
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{TEAL}"/>
  {r.halftone(16, 16, W, 620, step=16, color="#FFFFFF", op=0.16)}
  {r.sunburst(300, 560, 430, n=28)}
  <circle cx="300" cy="560" r="190" fill="#F7D58E"/>
  {r.star(70, 300, 16, "#FFFFFF")}{r.star(530, 280, 12, "#FFFFFF")}{r.star(520, 350, 7, CREAM)}{r.star(90, 370, 8, CREAM)}

  <!-- título -->
  <g transform="translate(300 150)">
    <rect x="-250" y="-112" width="500" height="208" rx="60" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>
    <rect x="-238" y="-100" width="476" height="184" rx="50" fill="none" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7 7"/>
    <text x="0" y="-30" text-anchor="middle" font-family="Pacifico" font-size="60" fill="{CHERRY}">Doces</text>
    <text x="0" y="38" text-anchor="middle" font-family="Pacifico" font-size="52" fill="{CHERRY}">sem açúcar</text>
    <text x="0" y="74" text-anchor="middle" font-family="Fredoka SemiBold" font-size="17" letter-spacing="3" fill="{INK}">RECEITAS PARA A FAMÍLIA</text>
  </g>

  <!-- fita com o lema -->
  <g transform="translate(300 320)">
    <path d="M-230 -20 L-200 -20 L-200 24 L-230 24 L-216 2 Z" fill="#B23A2F" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M230 -20 L200 -20 L200 24 L230 24 L216 2 Z" fill="#B23A2F" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
    <rect x="-205" y="-26" width="410" height="44" rx="6" fill="{CHERRY}" stroke="{INK}" stroke-width="3.5"/>
    <text x="0" y="4" text-anchor="middle" font-family="Fredoka SemiBold" font-size="19" fill="#FFFFFF">a fruta adoça, com casca e tudo!</text>
  </g>

  {gingham(560, 260)}
  <rect x="0" y="560" width="{W}" height="6" fill="{INK}" opacity="0.15"/>

  <!-- doces -->
  {loaf(60, 552)}
  {cake_round(410, 566, 0.95)}
  {brownies(215, 640)}
  {r.banana(30, 588, -6, 0.75)}
  {apple(130, 660)}
  {r.eggs(470, 640)}

  <!-- rodapé -->
  <g transform="translate(300 742)">
    <rect x="-262" y="-34" width="524" height="68" rx="34" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>
    <text x="0" y="-6" text-anchor="middle" font-family="Fredoka SemiBold" font-size="17" letter-spacing="1.5" fill="{INK}">DIA DA ALIMENTAÇÃO 2026</text>
    <text x="0" y="18" text-anchor="middle" font-family="Fredoka" font-size="15" fill="{INK}">EB João Villaret · Saúde Escolar · UCC Loures</text>
  </g>
</g>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="40" fill="none" stroke="{INK}" stroke-width="7"/>
</svg>'''
open(S + "/capa.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/capa.png", output_width=1200)
print("ok")
