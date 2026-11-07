import importlib.util, sys, random
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
DEEP = "#556B2F"
random.seed(5)

def bean(x, y, a, s=1.0):
    return (f'<g transform="translate({x} {y}) rotate({a}) scale({s})">'
            f'<path d="M-9 -2 Q-10 -9 -2 -9 Q4 -9 6 -5 Q10 -6 10 0 Q10 8 0 8 Q-9 8 -9 -2 Z" fill="#2A2320" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M-4 -5 q3 -2 6 0" stroke="#FFFFFF" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.8"/></g>')

scene = f'''
  <ellipse cx="400" cy="404" rx="200" ry="20" fill="{INK}" opacity="0.18"/>
  <g stroke="{INK}" stroke-width="3.5">
    <ellipse cx="400" cy="380" rx="185" ry="30" fill="#FFFFFF"/>
    <ellipse cx="400" cy="376" rx="158" ry="22" fill="#F1F7F6" stroke-width="2"/>
  </g>
  <!-- bolo redondo com fatia cortada -->
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M262 300 L262 360 Q380 392 498 360 L498 300 Z" fill="#4A2A18"/>
    <path d="M420 316 L498 300 L498 360 L420 376 Z" fill="#6B3A22"/>
    <path d="M262 300 Q262 276 380 276 Q498 276 498 300 L420 316 Q400 322 380 322 Q262 322 262 300 Z" fill="#5A321D"/>
  </g>
  <g fill="#3A1E11">{"".join(f'<circle cx="{x}" cy="{y}" r="2.2"/>' for x,y in [(434,330),(452,346),(470,322),(486,340),(444,360),(478,356)])}</g>
  <!-- polvilhado de cacau e frutos vermelhos -->
  <g fill="#7A4630">{"".join(f'<circle cx="{random.uniform(280,470):.0f}" cy="{random.uniform(284,312):.0f}" r="1.6"/>' for _ in range(26))}</g>
  {"".join(f'<circle cx="{x}" cy="{y}" r="8" fill="{CHERRY}" stroke="{INK}" stroke-width="2.5"/><path d="M{x-2} {y-7} l2 -5" stroke="#4E7A2E" stroke-width="2.5"/>' for x,y in [(340,292),(362,286),(388,294)])}
  <!-- fatia servida -->
  <g transform="translate(560 346)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <ellipse cx="40" cy="50" rx="66" ry="14" fill="#FFFFFF"/>
    <path d="M0 10 L80 0 L80 38 L0 48 Z" fill="#6B3A22"/>
    <path d="M0 10 L80 0 L95 -6 L15 4 Z" fill="#5A321D"/>
    <path d="M80 0 L95 -6 L95 32 L80 38 Z" fill="#4A2A18"/>
  </g>
  <!-- taça de feijão preto -->
  <g transform="translate(130 392)">
    {"".join(bean(dx, dy, a) for dx,dy,a in [(-26,-16,20),(-8,-22,-30),(10,-18,40),(26,-14,-10),(-16,-8,60),(4,-10,10),(20,-6,-50),(-30,-6,0)])}
    <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
      <path d="M-50 -8 Q-46 30 0 34 Q46 30 50 -8 Z" fill="{MUSTARD}"/>
      <path d="M-50 -8 Q0 2 50 -8" fill="none"/>
    </g>
    <g fill="#FFFFFF"><circle cx="-26" cy="10" r="4"/><circle cx="0" cy="16" r="4"/><circle cx="26" cy="10" r="4"/></g>
  </g>
  {"".join(bean(x, y, a, 0.9) for x,y,a in [(206,424,30),(222,416,-20),(70,424,10)])}
  <!-- frasco de xarope de tâmara -->
  <g transform="translate(700 366)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-22 -40 L-22 -54 L22 -54 L22 -40 Q36 -30 36 -10 L36 30 Q36 38 28 38 L-28 38 Q-36 38 -36 30 L-36 -10 Q-36 -30 -22 -40 Z" fill="#7A3B1E"/>
    <rect x="-26" y="-66" width="52" height="14" rx="5" fill="{CHERRY}"/>
    <rect x="-30" y="-8" width="60" height="26" rx="13" fill="#FFF6EA" stroke-width="2.5"/>
  </g>
  <text x="700" y="368" text-anchor="middle" font-family="Fredoka SemiBold" font-size="9" fill="{INK}">TÂMARA</text>
'''
svg = r.frame("Bolo de chocolate", "E FEIJÃO PRETO · SEM FARINHA", scene, accent=DEEP)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="0" text-anchor="middle" font-family="Pacifico" font-size="31"')
open(S + "/feijao-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/feijao-retro.png", output_width=1600)
print("ok")
