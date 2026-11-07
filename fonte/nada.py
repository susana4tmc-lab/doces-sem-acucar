import importlib.util, sys, random
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
BROWN = "#8C5A3C"
random.seed(7)

def coco_ball(x, y, rad=19):
    flakes = "".join(f'<rect x="{x+random.uniform(-rad*0.75, rad*0.6):.1f}" y="{y+random.uniform(-rad*0.75, rad*0.6):.1f}" width="6" height="2.4" rx="1.2" fill="#C9B9A6" transform="rotate({random.randint(-60,60)} {x} {y})"/>' for _ in range(9))
    return (f'<circle cx="{x}" cy="{y}" r="{rad}" fill="#5A321D" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x}" cy="{y}" r="{rad-3}" fill="#FBF5EA" opacity="0.88"/>' + flakes)

balls = "".join(coco_ball(x, y) for x, y in [(352, 352), (396, 356), (440, 352), (374, 326), (418, 326), (396, 300)])

scene = f'''
  <ellipse cx="400" cy="404" rx="170" ry="18" fill="{INK}" opacity="0.18"/>
  <g stroke="{INK}" stroke-width="3.5">
    <ellipse cx="398" cy="374" rx="140" ry="28" fill="{TEAL}"/>
    <ellipse cx="398" cy="370" rx="116" ry="20" fill="#FFF6EA" stroke-width="2"/>
  </g>
  {balls}
  <!-- garfo -->
  <g transform="translate(560 404) rotate(-14)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <rect x="0" y="-5" width="110" height="10" rx="5" fill="#D9DDE0"/>
    <path d="M-4 -12 L-34 -12 M-4 -4 L-34 -4 M-4 4 L-34 4 M-4 12 L-34 12" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M-6 -14 Q4 0 -6 14" fill="#D9DDE0"/>
  </g>
  {r.banana(30, 300, -10)}
  <!-- frasco de mel pequeno -->
  <g transform="translate(200 378)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-24 -28 Q-28 22 -20 26 L20 26 Q28 22 24 -28 Z" fill="{ORANGE}"/>
    <rect x="-27" y="-42" width="54" height="16" rx="5" fill="{MUSTARD}"/>
    <rect x="-17" y="-12" width="34" height="18" rx="9" fill="#FFF6EA" stroke-width="2.5"/>
  </g>
  <text x="200" y="378" text-anchor="middle" font-family="Fredoka SemiBold" font-size="9" fill="{INK}">MEL</text>
  <!-- tigela de coco ralado -->
  <g transform="translate(690 372)">
    <g fill="#FFFFFF" stroke="{INK}" stroke-width="2">{"".join(f'<rect x="{dx}" y="{dy}" width="8" height="3" rx="1.5" transform="rotate({a} {dx} {dy})"/>' for dx,dy,a in [(-30,-16,20),(-14,-22,-30),(4,-18,40),(18,-22,-10),(-22,-10,60),(10,-12,15),(26,-12,-45)])}</g>
    <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
      <path d="M-50 -10 Q-46 28 0 32 Q46 28 50 -10 Z" fill="{CHERRY}"/>
      <path d="M-50 -10 Q0 0 50 -10" fill="none"/>
    </g>
    <g fill="#FFFFFF"><circle cx="-26" cy="8" r="4"/><circle cx="0" cy="14" r="4"/><circle cx="26" cy="8" r="4"/></g>
  </g>
'''
svg = r.frame("Ahhh… nada!", "BOLINHAS DE BANANA E COCO", scene, accent=BROWN)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="2" text-anchor="middle" font-family="Pacifico" font-size="36"')
open(S + "/nada-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/nada-retro.png", output_width=1600)
print("ok")
