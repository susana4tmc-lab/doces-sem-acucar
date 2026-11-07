import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
SKY = "#4F9FC4"

def muffin(x, y, s=1.0, cup=CHERRY):
    stripes = "".join(f'<path d="M{-30+i*10} 0 L{-24+i*8} 34" stroke="{INK}" stroke-width="1.5" opacity="0.45"/>' for i in range(7))
    return f'''<g transform="translate({x} {y}) scale({s})">
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-34 0 L34 0 L26 36 L-26 36 Z" fill="{cup}"/>
  </g>
  {stripes}
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-40 2 Q-46 -20 -26 -32 Q-10 -46 8 -40 Q30 -44 40 -24 Q48 -6 40 2 Z" fill="#C98A45"/>
  </g>
  <g fill="#8A5530"><circle cx="-18" cy="-18" r="2"/><circle cx="4" cy="-28" r="2"/><circle cx="22" cy="-14" r="2"/><circle cx="-4" cy="-10" r="2"/><circle cx="14" cy="-30" r="1.6"/></g>
  <g stroke="{INK}" stroke-width="2.5" stroke-linejoin="round">
    <path d="M-12 -30 L4 -34 L6 -24 L-10 -20 Z" fill="#F6E7B8"/>
    <path d="M10 -22 L24 -26 L26 -16 L12 -12 Z" fill="#F6E7B8"/>
  </g>
  <path d="M-12 -30 L4 -34" stroke="{CHERRY}" stroke-width="2.5"/>
  <path d="M10 -22 L24 -26" stroke="{CHERRY}" stroke-width="2.5"/>
</g>'''

def apple(tx, ty, s=1.0, half=False):
    if half:
        return f'''<g transform="translate({tx} {ty}) scale({s})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M0 -26 Q-34 -40 -40 -4 Q-40 32 -10 36 Q0 32 10 36 Q40 32 40 -4 Q34 -40 0 -26 Z" fill="#FFF3D6"/>
  <path d="M0 -26 Q-34 -40 -40 -4 Q-40 32 -10 36 Q0 32 10 36 Q40 32 40 -4 Q34 -40 0 -26 Z" fill="none" stroke="{CHERRY}" stroke-width="5"/>
  <g fill="#3B2414" stroke="none"><ellipse cx="-7" cy="4" rx="3" ry="5"/><ellipse cx="7" cy="4" rx="3" ry="5"/></g>
  <path d="M0 -26 Q2 -40 8 -46" fill="none"/>
</g>'''
    return f'''<g transform="translate({tx} {ty}) scale({s})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M0 -26 Q-34 -40 -40 -4 Q-40 32 -10 36 Q0 32 10 36 Q40 32 40 -4 Q34 -40 0 -26 Z" fill="{CHERRY}"/>
  <path d="M0 -26 Q2 -40 8 -46" fill="none"/>
  <path d="M6 -38 Q22 -54 34 -42 Q20 -30 6 -38 Z" fill="#7FB069" stroke-width="3"/>
  <path d="M-24 -10 Q-26 2 -20 12" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round"/>
</g>'''

scene = f'''
  <ellipse cx="400" cy="404" rx="190" ry="20" fill="{INK}" opacity="0.18"/>
  <g stroke="{INK}" stroke-width="3.5">
    <ellipse cx="400" cy="380" rx="185" ry="30" fill="#FFFFFF"/>
    <ellipse cx="400" cy="376" rx="160" ry="22" fill="#F1F7F6" stroke-width="2"/>
  </g>
  {muffin(330, 330, 1.0, TEAL)}{muffin(470, 330, 1.0, MUSTARD)}
  {muffin(400, 352, 1.1, CHERRY)}
  {apple(130, 372)}{apple(205, 392, 0.8, half=True)}
  <!-- frasco de aveia -->
  <g transform="translate(670 360)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-40 -56 Q-46 40 -34 44 L34 44 Q46 40 40 -56 Z" fill="#FFFDF5"/>
    <path d="M-38 -20 Q-40 40 -32 42 L32 42 Q40 40 38 -20 Z" fill="#EAD9B5" stroke="none"/>
    <path d="M-40 -56 Q-46 40 -34 44 L34 44 Q46 40 40 -56 Z" fill="none"/>
    <rect x="-44" y="-74" width="88" height="20" rx="6" fill="{TEAL}"/>
  </g>
  <g fill="#C9B07E">{"".join(f'<ellipse cx="{670+dx}" cy="{360+dy}" rx="4" ry="2.4" transform="rotate({a} {670+dx} {360+dy})"/>' for dx,dy,a in [(-20,-6,20),(-6,4,-30),(10,-10,40),(22,6,0),(-14,18,60),(4,24,-10),(18,30,30),(-24,32,-40),(0,-14,10),(14,16,70)])}</g>
  <rect x="644" y="352" width="52" height="22" rx="11" fill="#FFF6EA" stroke="{INK}" stroke-width="2.5"/>
  <text x="670" y="367" text-anchor="middle" font-family="Fredoka SemiBold" font-size="10" fill="{INK}">AVEIA</text>
'''
svg = r.frame("Muffins", "DE AVEIA E MAÇÃ · SEM AÇÚCAR", scene, accent=SKY)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="0" text-anchor="middle" font-family="Pacifico" font-size="34"')
open(S + "/muffins-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/muffins-retro.png", output_width=1600)
print("ok")
