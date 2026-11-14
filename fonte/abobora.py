import importlib.util, sys, random
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
ACC = "#C8642A"
PUMP = "#F08A2E"
random.seed(7)

# frasco de doce com tampa de pano aos quadrados e fita
def jar(x, y):
    checks = "".join(
        f'<rect x="{x-58+i*14}" y="{y-150+j*10}" width="7" height="5" fill="{CHERRY}" opacity="0.85"/>'
        for i in range(9) for j in range(2))
    return f'''
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M{x-52} {y-118} Q{x-62} {y-60} {x-56} {y-6} Q{x-54} {y+6} {x-40} {y+6} L{x+40} {y+6} Q{x+54} {y+6} {x+56} {y-6} Q{x+62} {y-60} {x+52} {y-118} Z" fill="{PUMP}"/>
    <path d="M{x-38} {y-104} Q{x-44} {y-60} {x-40} {y-20}" stroke="#FFD9A8" stroke-width="7" fill="none" opacity="0.8"/>
    <rect x="{x-56}" y="{y-134}" width="112" height="18" rx="5" fill="#E8C98C"/>
    <path d="M{x-62} {y-128} L{x-70} {y-104} Q{x} {y-112} {x+70} {y-104} L{x+62} {y-128} Q{x} {y-160} {x-62} {y-128} Z" fill="#FFF6EA"/>
  </g>
  <g clip-path="url(#cloth)">{checks}</g>
  <clipPath id="cloth"><path d="M{x-62} {y-128} L{x-70} {y-104} Q{x} {y-112} {x+70} {y-104} L{x+62} {y-128} Q{x} {y-160} {x-62} {y-128} Z"/></clipPath>
  <path d="M{x-62} {y-128} L{x-70} {y-104} Q{x} {y-112} {x+70} {y-104} L{x+62} {y-128} Q{x} {y-160} {x-62} {y-128} Z" fill="none" stroke="{INK}" stroke-width="3.5"/>
  <path d="M{x-56} {y-118} Q{x} {y-124} {x+56} {y-118}" stroke="{CHERRY}" stroke-width="5" fill="none"/>
  <g stroke="{INK}" stroke-width="2.5"><rect x="{x-34}" y="{y-70}" width="68" height="34" rx="14" fill="#FFF6EA"/></g>
  <text x="{x}" y="{y-49}" text-anchor="middle" font-family="Fredoka SemiBold" font-size="12" fill="{INK}">ABÓBORA</text>
'''

scene = f'''
  <ellipse cx="400" cy="410" rx="250" ry="18" fill="{INK}" opacity="0.18"/>
  <!-- abóbora-menina cortada ao meio (pescoço comprido) -->
  <g transform="translate(205 352) rotate(-8)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-120 10 Q-126 -38 -84 -44 Q-40 -46 -10 -30 Q30 -58 70 -50 Q112 -40 110 6 Q108 50 64 52 Q24 54 -6 40 Q-40 54 -84 50 Q-118 46 -120 10 Z" fill="#E8C98C"/>
    <path d="M-106 10 Q-110 -26 -80 -30 Q-44 -32 -12 -18 Q28 -42 66 -36 Q96 -28 94 6 Q92 38 60 38 Q22 40 -8 26 Q-42 40 -80 36 Q-104 32 -106 10 Z" fill="{PUMP}" stroke-width="2.5"/>
    <ellipse cx="44" cy="2" rx="30" ry="18" fill="#F6B25A" stroke-width="2.5"/>
    {"".join(f'<ellipse cx="{44+random.uniform(-18,18):.0f}" cy="{random.uniform(-8,12):.0f}" rx="4" ry="2.5" fill="#FFF1D6" stroke-width="1.5"/>' for _ in range(7))}
    <path d="M-120 8 L-138 2 Q-142 10 -136 16 L-120 14" fill="#7A8B3C"/>
  </g>
  <!-- cubos de abóbora -->
  {"".join(f'<g transform="translate({x} {y}) rotate({a})"><rect x="-11" y="-11" width="22" height="22" rx="3" fill="{PUMP}" stroke="{INK}" stroke-width="2.5"/><path d="M-11 -11 L-5 -16 L16 -16 L11 -11 Z" fill="#F6B25A" stroke="{INK}" stroke-width="2"/></g>' for x,y,a in [(330,404,0),(356,412,8),(312,420,-6)])}
  {jar(440, 404)}
  <!-- maçã -->
  <g transform="translate(560 372)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M0 -26 Q-34 -40 -40 -4 Q-42 34 -12 38 Q0 32 12 38 Q42 34 40 -4 Q34 -40 0 -26 Z" fill="{CHERRY}"/>
    <path d="M0 -26 Q2 -40 8 -48" fill="none"/>
    <path d="M6 -40 Q24 -54 34 -40 Q20 -32 6 -40 Z" fill="#4FA36A" stroke-width="2.5"/>
    <path d="M-24 -12 Q-28 4 -22 18" stroke="#FFFFFF" stroke-width="5" fill="none" opacity="0.6"/>
  </g>
  <!-- meia laranja -->
  <g transform="translate(650 392)" stroke="{INK}" stroke-width="3.5">
    <circle r="36" fill="{ORANGE}"/>
    <circle r="28" fill="#FFC56B" stroke-width="2"/>
    {"".join(f'<path d="M0 0 L{28*__import__("math").cos(i*0.785):.1f} {28*__import__("math").sin(i*0.785):.1f}" stroke="{ORANGE}" stroke-width="2.5"/>' for i in range(8))}
    <circle r="4" fill="#FFF1D6" stroke-width="1.5"/>
  </g>
  <!-- paus de canela -->
  <g transform="translate(690 340) rotate(-18)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <rect x="-46" y="-7" width="92" height="14" rx="7" fill="#9E5A2E"/>
    <rect x="-40" y="5" width="86" height="14" rx="7" fill="#B8703C"/>
    <path d="M-46 0 q4 -6 8 0" fill="none" stroke-width="2"/>
  </g>
'''
svg = r.frame("Doce de abóbora", "MAÇÃ, LARANJA E CANELA · SEM AÇÚCAR", scene, accent=ACC)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="0" text-anchor="middle" font-family="Pacifico" font-size="32"')
open(S + "/abobora-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/abobora-retro.png", output_width=1600)
print("ok")
