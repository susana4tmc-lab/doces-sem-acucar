"""Gera as ilustrações retro (anos 60) do livro Doces Sem Açúcar."""
import math, sys
import cairosvg

W, H = 800, 460
INK = "#3B2414"      # contorno castanho-escuro
CREAM = "#F6E8CC"
MUSTARD = "#E9A93B"
ORANGE = "#E2703A"
TEAL = "#3E9C9A"
CHERRY = "#D9483B"
PINK = "#F2B8A8"


def sunburst(cx, cy, r, n=24, c1=MUSTARD, c2="#F2C46A"):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c2}"/>']
    for i in range(n):
        if i % 2:
            continue
        a1 = 2 * math.pi * i / n
        a2 = 2 * math.pi * (i + 1) / n
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        out.append(f'<path d="M{cx} {cy} L{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} Z" fill="{c1}"/>')
    return "\n".join(out)


def halftone(x0, y0, x1, y1, step=14, color=ORANGE, op=0.25):
    dots = []
    y = y0
    row = 0
    while y < y1:
        x = x0 + (step / 2 if row % 2 else 0)
        while x < x1:
            dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.6"/>')
            x += step
        y += step
        row += 1
    return f'<g fill="{color}" opacity="{op}">' + "".join(dots) + "</g>"


def star(cx, cy, r, color):
    # estrelinha de 4 pontas "atómica"
    s = r * 0.28
    return (f'<path d="M{cx} {cy-r} Q{cx+s} {cy-s} {cx+r} {cy} Q{cx+s} {cy+s} {cx} {cy+r} '
            f'Q{cx-s} {cy+s} {cx-r} {cy} Q{cx-s} {cy-s} {cx} {cy-r} Z" fill="{color}"/>')


def gingham(y, h):
    g = [f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="#FFF6EA"/>',
         f'<g fill="{CHERRY}" opacity="0.45">']
    for x in range(0, W, 40):
        g.append(f'<rect x="{x}" y="{y}" width="20" height="{h}"/>')
    g.append('</g>')
    g.append(f'<g fill="{CHERRY}" opacity="0.45">')
    for yy in range(y, y + h, 40):
        g.append(f'<rect x="0" y="{yy}" width="{W}" height="20"/>')
    g.append('</g>')
    g.append(f'<rect x="0" y="{y}" width="{W}" height="6" fill="{INK}" opacity="0.15"/>')
    return "\n".join(g)


def frame(title, subtitle, scene, accent=TEAL):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*2}" height="{H*2}">
<defs><clipPath id="r"><rect x="14" y="14" width="{W-28}" height="{H-28}" rx="34"/></clipPath></defs>
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{accent}"/>
  {halftone(20, 20, W, 330, color="#FFFFFF", op=0.18)}
  {sunburst(400, 300, 330)}
  <circle cx="400" cy="300" r="170" fill="#F7D58E"/>
  {star(110, 70, 16, "#FFFFFF")}{star(700, 95, 12, "#FFFFFF")}{star(650, 40, 8, CREAM)}{star(160, 140, 8, CREAM)}
  {gingham(350, 120)}
  {scene}
  <g transform="translate(400 66)">
    <rect x="-215" y="-44" width="430" height="92" rx="46" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>
    <rect x="-205" y="-34" width="410" height="72" rx="36" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 6"/>
    <text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38" fill="{CHERRY}">{title}</text>
    <text x="0" y="34" text-anchor="middle" font-family="Fredoka SemiBold" font-size="15" letter-spacing="2" fill="{INK}">{subtitle}</text>
  </g>
</g>
<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="34" fill="none" stroke="{INK}" stroke-width="6"/>
</svg>'''


def banana(tx, ty, rot, scale=1.0):
    return f'''<g transform="translate({tx} {ty}) rotate({rot}) scale({scale})" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
  <path d="M0 60 Q60 120 150 70 Q150 86 140 93 Q60 142 -8 72 Z" fill="#F5C842"/>
  <path d="M148 70 L161 59 L165 66 L152 77 Z" fill="#6B4A22"/>
  <path d="M-8 72 L-14 76" />
  <g stroke="none" fill="{INK}"><circle cx="58" cy="100" r="3"/><circle cx="96" cy="97" r="2.5"/><circle cx="32" cy="88" r="2"/></g>
</g>'''


def eggs(x, y):
    return f'''<g stroke="{INK}" stroke-width="3">
  <ellipse cx="{x}" cy="{y}" rx="22" ry="28" fill="#FFFDF5"/>
  <ellipse cx="{x+40}" cy="{y+6}" rx="20" ry="26" fill="#F3DCC0"/>
</g>'''


def bolo_mole():
    scene = f'''
  <ellipse cx="400" cy="400" rx="235" ry="40" fill="{INK}" opacity="0.18"/>
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <ellipse cx="400" cy="392" rx="228" ry="40" fill="#FFFFFF"/>
    <ellipse cx="400" cy="388" rx="190" ry="28" fill="#F1F7F6" stroke-width="2"/>
    <!-- corpo -->
    <path d="M245 300 L245 362 Q400 398 555 362 L555 300 Z" fill="{MUSTARD}"/>
    <!-- face cortada -->
    <path d="M470 314 L555 300 L555 362 L470 376 Z" fill="#FBE3A0"/>
    <!-- topo -->
    <path d="M245 300 Q245 274 400 274 Q555 274 555 300 L470 314 Q440 324 400 324 Q245 324 245 300 Z" fill="{ORANGE}"/>
  </g>
  <path d="M470 334 Q512 328 555 321 M470 354 Q512 348 555 341" stroke="#EBC56A" stroke-width="4" fill="none"/>
  <g fill="#FFFFFF">
    {"".join(f'<rect x="{x}" y="{y}" width="9" height="3.5" rx="1.7" transform="rotate({r} {x+4} {y+1})"/>' for x,y,r in [(280,294,20),(312,284,-15),(345,300,35),(376,284,-30),(408,298,10),(436,288,-40),(300,308,50),(366,310,-10),(440,304,25),(332,280,60),(262,300,-25),(415,280,45),(390,300,70),(455,296,-5)])}
  </g>
  {eggs(668, 322)}
  <!-- fatia servida -->
  <g transform="translate(598 340)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <ellipse cx="45" cy="52" rx="75" ry="16" fill="#FFFFFF"/>
    <path d="M0 10 L80 0 L80 38 L0 48 Z" fill="#FBE3A0"/>
    <path d="M0 10 L80 0 L95 -6 L15 4 Z" fill="{ORANGE}"/>
    <path d="M80 0 L95 -6 L95 32 L80 38 Z" fill="{MUSTARD}"/>
  </g>
  {banana(40, 292, -10)}
  <!-- meio coco -->
  <g transform="translate(120 378)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-54 -2 Q-50 44 0 48 Q50 44 54 -2 Z" fill="#7B4A2C"/>
    <ellipse cx="0" cy="-2" rx="54" ry="17" fill="#7B4A2C"/>
    <ellipse cx="0" cy="-2" rx="44" ry="12" fill="#FFFFFF" stroke-width="2.5"/>
    <path d="M-30 22 l6 4 M-8 32 l6 3 M16 30 l5 4 M33 18 l5 4" stroke="#4E2D18" stroke-width="2.5"/>
  </g>
'''
    return frame("Bolo mole", "DE BANANA E COCO · SEM AÇÚCAR", scene, accent=TEAL)


def brownie_sq(tx, ty, rot=0, banana_top=False, dots=()):
    extra = ""
    if banana_top:
        extra = (f'<ellipse cx="40" cy="-7" rx="16" ry="5.5" fill="#FBEAB2" stroke="{INK}" stroke-width="2.5"/>'
                 f'<circle cx="40" cy="-7" r="2" fill="#D9B85A"/>')
    d = "".join(f'<circle cx="{x}" cy="{y}" r="2.3" fill="#24120A"/>' for x, y in dots)
    return f'''<g transform="translate({tx} {ty}) rotate({rot})">
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <path d="M0 0 L70 0 L80 -12 L10 -12 Z" fill="#7A4630"/>
    <path d="M0 0 L70 0 L70 32 L0 32 Z" fill="#4E2A19"/>
    <path d="M70 0 L80 -12 L80 20 L70 32 Z" fill="#3A1E11"/>
  </g>
  <path d="M14 -6 l11 -2 M44 -5 l12 -3" stroke="#A8714F" stroke-width="2.5" stroke-linecap="round"/>
  {d}{extra}
</g>'''


def brownie():
    scene = f'''
  <path d="M215 398 L585 398 L625 348 L255 348 Z" fill="{INK}" opacity="0.18" transform="translate(5 9)"/>
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M215 398 L585 398 L625 348 L255 348 Z" fill="#E0A66A"/>
    <path d="M215 398 L585 398 L585 410 L215 410 Z" fill="#B97A45"/>
    <path d="M585 398 L625 348 L625 360 L585 410 Z" fill="#9E6436"/>
  </g>
  <path d="M265 362 L600 362 M250 382 L592 382" stroke="#C98B52" stroke-width="2"/>
  {brownie_sq(300, 322)}
  {brownie_sq(385, 322)}
  {brownie_sq(278, 358, dots=((20,14),(48,22)))}
  {brownie_sq(363, 358, dots=((30,16),(56,10)))}
  {brownie_sq(478, 364, rot=-6, banana_top=True, dots=((18,14),))}
  {banana(44, 296, -10)}
  <!-- taça de cacau -->
  <g transform="translate(135 386)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-56 -26 Q-50 20 0 24 Q50 20 56 -26 Z" fill="{CHERRY}"/>
    <ellipse cx="0" cy="-26" rx="56" ry="13" fill="#5A321D"/>
    <path d="M-30 -32 Q0 -50 30 -32 Q0 -27 -30 -32 Z" fill="#7A4630" stroke-width="2.5"/>
    <g fill="#FFFFFF" stroke="none"><circle cx="-30" cy="0" r="5"/><circle cx="-8" cy="8" r="5"/><circle cx="16" cy="6" r="5"/><circle cx="36" cy="-4" r="5"/></g>
  </g>
  {eggs(708, 350)}
'''
    return frame("Brownie", "DE CACAU E BANANA · SEM AÇÚCAR", scene, accent=ORANGE)


if __name__ == "__main__":
    out = sys.argv[1]
    for name, fn in (("bolo-mole-retro", bolo_mole), ("brownie-retro", brownie)):
        svg = fn()
        open(f"{out}/{name}.svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{out}/{name}.png", output_width=1600)
        print(name, "ok")


def bolo_banana():
    loaf = f'''
  <ellipse cx="390" cy="402" rx="200" ry="22" fill="{INK}" opacity="0.18"/>
  <!-- grelha / tabuleiro azul-petróleo -->
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M200 396 L580 396 L612 360 L232 360 Z" fill="{TEAL}"/>
    <path d="M200 396 L580 396 L580 406 L200 406 Z" fill="#2E7775"/>
    <path d="M580 396 L612 360 L612 370 L580 406 Z" fill="#256462"/>
  </g>
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <!-- lateral -->
    <path d="M250 300 L250 368 L490 368 L490 300 Z" fill="#B8733C"/>
    <!-- face cortada (fatia retirada) -->
    <path d="M490 300 L540 286 L540 354 L490 368 Z" fill="#E7C27F"/>
    <!-- topo abaulado -->
    <path d="M250 300 Q250 262 330 258 L470 254 Q540 252 540 286 L490 300 Q370 316 250 300 Z" fill="#9C5A2C"/>
  </g>
  <!-- miolo pintalgado de canela -->
  <g fill="#B07A44">{"".join(f'<circle cx="{x}" cy="{y}" r="2"/>' for x,y in [(500,310),(515,322),(528,300),(505,340),(522,346),(532,328),(498,356),(514,296)])}</g>
  <!-- banana em cima, cortada ao comprido -->
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <path d="M275 284 Q370 262 470 266 Q480 272 470 280 Q370 284 280 298 Q266 292 275 284 Z" fill="#F6E3A1"/>
    <path d="M290 288 Q370 272 460 273" stroke="#D9B85A" stroke-width="2.5" fill="none"/>
  </g>
  <!-- fatia servida -->
  <g transform="translate(598 334)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <ellipse cx="38" cy="58" rx="62" ry="14" fill="#FFFFFF"/>
    <path d="M0 0 L60 0 L60 52 L0 52 Z" fill="#E7C27F"/>
    <path d="M0 0 Q4 -16 30 -18 Q56 -16 60 0 Z" fill="#9C5A2C"/>
    <path d="M60 0 L74 -6 L74 46 L60 52 Z" fill="#B8733C"/>
  </g>
  <g fill="#B07A44">{"".join(f'<circle cx="{598+x}" cy="{334+y}" r="2"/>' for x,y in [(12,14),(30,24),(46,12),(20,38),(42,40)])}</g>
  {banana(44, 296, -10)}
  <!-- frasco de canela -->
  <g transform="translate(150 360)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <rect x="-30" y="-46" width="60" height="78" rx="10" fill="#FFFDF5"/>
    <rect x="-34" y="-62" width="68" height="20" rx="6" fill="{CHERRY}"/>
    <rect x="-24" y="-20" width="48" height="30" rx="4" fill="{MUSTARD}" stroke-width="2.5"/>
    <path d="M-30 14 L30 14 L30 22 Q30 32 20 32 L-20 32 Q-30 32 -30 22 Z" fill="#9C5A2C" stroke="none"/>
  </g>
  <text x="150" y="350" text-anchor="middle" font-family="Fredoka SemiBold" font-size="11" fill="{INK}">CANELA</text>
  <!-- paus de canela -->
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <rect x="60" y="398" width="70" height="12" rx="6" fill="#9C5A2C" transform="rotate(-8 95 404)"/>
    <rect x="70" y="412" width="62" height="11" rx="5.5" fill="#B8733C" transform="rotate(4 100 417)"/>
  </g>
  {eggs(690, 300)}
'''
    return frame("Bolo de banana", "COM CANELA · SEM AÇÚCAR", loaf, accent=CHERRY)


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "banana":
    svg = bolo_banana()
    open(f"{sys.argv[1]}/bolo-banana-retro.svg", "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{sys.argv[1]}/bolo-banana-retro.png", output_width=1600)
