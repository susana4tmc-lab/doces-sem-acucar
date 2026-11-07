import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
PURPLE = "#6C4F8C"

def pancake(y, rx=88):
    return f'''<g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M{-rx} {y} Q{-rx} {y+16} 0 {y+18} Q{rx} {y+16} {rx} {y} Z" fill="#D9933E"/>
  <ellipse cx="0" cy="{y}" rx="{rx}" ry="16" fill="#E9B05A"/>
</g>
<ellipse cx="-20" cy="{y-3}" rx="40" ry="7" fill="#F2C878" opacity="0.8"/>'''

stack = "".join(pancake(y) for y in (350, 334, 318, 302, 286))
slices = "".join(f'<g transform="translate({x} {y})" stroke="{INK}" stroke-width="2.5"><ellipse rx="15" ry="6" fill="#FBEAB2"/><circle r="2.2" fill="#D9B85A" stroke="none"/></g>' for x, y in [(-34, 282), (0, 278), (34, 284), (-14, 290), (18, 292)])
berries = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#3E4E9C" stroke="{INK}" stroke-width="2.5"/>' for x, y in [(-6, 268), (14, 270), (4, 262)])

scene = f'''
  <ellipse cx="400" cy="402" rx="190" ry="20" fill="{INK}" opacity="0.18"/>
  <g transform="translate(400 0)">
    <g stroke="{INK}" stroke-width="3.5"><ellipse cx="0" cy="372" rx="150" ry="28" fill="#FFFFFF"/><ellipse cx="0" cy="370" rx="118" ry="20" fill="#F1F7F6" stroke-width="2"/></g>
    {stack}
    {slices}{berries}
  </g>
  <!-- frigideira -->
  <g transform="translate(640 380)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <rect x="58" y="-10" width="90" height="16" rx="8" fill="{CHERRY}" transform="rotate(-10 58 -2)"/>
    <ellipse cx="0" cy="0" rx="70" ry="22" fill="#3B3B40"/>
    <ellipse cx="0" cy="-2" rx="58" ry="16" fill="#55555C" stroke-width="2"/>
    <ellipse cx="-4" cy="-4" rx="28" ry="8" fill="#E9B05A" stroke-width="2.5"/>
  </g>
  {r.banana(30, 300, -10)}
  <!-- ovo e copo de bebida vegetal -->
  <g transform="translate(180 360)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-24 -50 L24 -50 L20 36 L-20 36 Z" fill="#FFFDF5"/>
    <path d="M-22 -20 L22 -20 L20 36 L-20 36 Z" fill="#F3E7D2" stroke-width="0"/>
    <path d="M-24 -50 L24 -50 L20 36 L-20 36 Z" fill="none"/>
    <path d="M-16 -40 L-14 24" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  </g>
  <ellipse cx="236" cy="384" rx="18" ry="23" fill="#F3DCC0" stroke="{INK}" stroke-width="3"/>
'''
svg = r.frame("Panquecas", "DE BANANA E AVEIA · SEM AÇÚCAR", scene, accent=PURPLE)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="0" text-anchor="middle" font-family="Pacifico" font-size="34"')
open(S + "/panquecas-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/panquecas-retro.png", output_width=1600)
print("ok")
