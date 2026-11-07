import importlib.util, sys, random
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
XGREEN = "#2F6B4F"
random.seed(21)

def slice_(x, y, rx=26, ry=24):
    bits = "".join(
        f'<rect x="{x+random.uniform(-rx*0.6, rx*0.5):.0f}" y="{y+random.uniform(-ry*0.6, ry*0.5):.0f}" width="{random.choice([5,6,7])}" height="{random.choice([4,5,6])}" rx="1" fill="{random.choice(["#E8C98C","#C98B52","#F2E3C4","#D9B37A"])}"/>'
        for _ in range(9))
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#4A2A18" stroke="{INK}" stroke-width="3"/>' + bits +
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="#6E4027" stroke-width="3" opacity="0.8"/>')

def holly(x, y, s=1.0, rot=0):
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round">
  <path d="M0 0 Q-14 -8 -30 -4 Q-26 -10 -32 -16 Q-22 -16 -18 -22 Q-12 -14 0 0 Z" fill="#3E8E5A"/>
  <path d="M0 0 Q14 -8 30 -4 Q26 -10 32 -16 Q22 -16 18 -22 Q12 -14 0 0 Z" fill="#4FA36A"/>
  <circle cx="-5" cy="-3" r="6" fill="{CHERRY}"/><circle cx="6" cy="-4" r="6" fill="{CHERRY}"/><circle cx="0" cy="-10" r="6" fill="{CHERRY}"/>
</g>'''

scene = f'''
  <ellipse cx="400" cy="408" rx="210" ry="18" fill="{INK}" opacity="0.18"/>
  <!-- tábua -->
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M210 400 L590 400 L626 352 L246 352 Z" fill="#E0A66A"/>
    <path d="M210 400 L590 400 L590 410 L210 410 Z" fill="#B97A45"/>
    <path d="M590 400 L626 352 L626 362 L590 410 Z" fill="#9E6436"/>
  </g>
  <!-- salame inteiro, polvilhado de cacau, com fio -->
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M262 318 L438 318 Q462 318 462 344 Q462 370 438 370 L262 370 Z" fill="#5A321D"/>
    <ellipse cx="262" cy="344" rx="16" ry="26" fill="#6E4027"/>
  </g>
  <g fill="#8A5636" opacity="0.8">{"".join(f'<circle cx="{random.uniform(280,450):.0f}" cy="{random.uniform(322,366):.0f}" r="1.8"/>' for _ in range(40))}</g>
  <g stroke="#FFF6EA" stroke-width="3" fill="none">
    <path d="M300 318 L300 370 M340 318 L340 370 M380 318 L380 370 M420 318 L420 370"/>
  </g>
  <!-- rodelas cortadas -->
  {slice_(500, 360)}{slice_(548, 368)}{slice_(522, 330)}
  <!-- frasco de manteiga de amendoim -->
  <g transform="translate(150 368)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-32 -38 Q-36 30 -26 34 L26 34 Q36 30 32 -38 Z" fill="#C98B52"/>
    <rect x="-36" y="-56" width="72" height="20" rx="6" fill="{CHERRY}"/>
    <rect x="-26" y="-14" width="52" height="24" rx="12" fill="#FFF6EA" stroke-width="2.5"/>
  </g>
  <text x="150" y="369" text-anchor="middle" font-family="Fredoka SemiBold" font-size="8.5" fill="{INK}">AMENDOIM</text>
  <!-- tâmaras -->
  {"".join(f'<g transform="translate({x} {y}) rotate({a})"><ellipse rx="14" ry="7" fill="#6B3A1E" stroke="{INK}" stroke-width="2.5"/><path d="M-8 -2 q8 -3 16 0" stroke="#8E5530" stroke-width="2" fill="none"/></g>' for x,y,a in [(66,410,15),(92,420,-20),(222,420,30)])}
  <!-- tablete de chocolate -->
  <g transform="translate(696 384) rotate(-10)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <rect x="-44" y="-26" width="88" height="52" rx="4" fill="#4E2A19"/>
    <path d="M-44 -26 L-44 26 L-12 26 L-12 -26 Z" fill="{XGREEN}"/>
    <path d="M14 -26 L14 26 M-12 0 L44 0" stroke="#3A1E11" stroke-width="2.5"/>
  </g>
  <text x="668" y="392" transform="rotate(-100 668 392)" text-anchor="middle" font-family="Fredoka SemiBold" font-size="10" fill="#FFFFFF">70%</text>
'''
svg = r.frame("Salame de chocolate", "SEM AÇÚCAR · SEM FORNO", scene, accent=XGREEN)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="0" text-anchor="middle" font-family="Pacifico" font-size="30"')
# estrelas douradas extra (Natal)
open(S + "/salame-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/salame-retro.png", output_width=1600)
print("ok")
