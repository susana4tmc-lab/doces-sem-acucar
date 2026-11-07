import importlib.util, sys, random
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
COFFEE = "#6B4A3A"
random.seed(11)

def jar(x, y, s=1.0):
    seeds = "".join(f'<ellipse cx="{random.uniform(-36,36):.1f}" cy="{random.uniform(-10,40):.1f}" rx="1.6" ry="1.1" fill="#3B2414"/>' for _ in range(40))
    return f'''<g transform="translate({x} {y}) scale({s})">
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-44 -60 L44 -60 L42 48 Q42 58 32 58 L-32 58 Q-42 58 -42 48 Z" fill="#E8F3F6"/>
  </g>
  <path d="M-40 -14 L40 -14 L39 48 Q39 55 31 55 L-31 55 Q-39 55 -39 48 Z" fill="#C9A27E"/>
  <path d="M-42 -52 L42 -52 L40 -14 L-40 -14 Z" fill="#F6EEE2"/>
  <path d="M-40 -14 Q-20 -20 0 -14 Q20 -8 40 -14" stroke="#B48A64" stroke-width="2" fill="none"/>
  {seeds}
  
  <path d="M-42 -52 Q-30 -66 -10 -60 Q4 -70 22 -62 Q40 -64 42 -52 Q0 -44 -42 -52 Z" fill="#6E4027" stroke="{INK}" stroke-width="2.5"/>
  <g fill="#5A321D" opacity="0.7">{"".join(f'<circle cx="{random.uniform(-30,30):.1f}" cy="{random.uniform(-60,-52):.1f}" r="1.6"/>' for _ in range(10))}</g>
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-44 -60 L44 -60 L42 48 Q42 58 32 58 L-32 58 Q-42 58 -42 48 Z" fill="none"/>
    <ellipse cx="0" cy="-60" rx="44" ry="6" fill="none" stroke-width="3"/>
  </g>
  <path d="M-34 -30 Q-36 10 -32 44" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.8"/>
</g>'''

scene = f'''
  <ellipse cx="400" cy="408" rx="170" ry="18" fill="{INK}" opacity="0.18"/>
  {jar(330, 342)}
  {jar(462, 348, 0.92)}
  <!-- chávena de café -->
  <g transform="translate(650 368)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <ellipse cx="0" cy="40" rx="62" ry="13" fill="#FFFFFF"/>
    <path d="M38 -6 Q66 -6 62 14 Q58 30 34 26" fill="none" stroke-width="7"/>
    <path d="M38 -6 Q66 -6 62 14 Q58 30 34 26" fill="none" stroke="#FFFFFF" stroke-width="3"/>
    <path d="M-42 -18 Q-40 34 0 36 Q40 34 42 -18 Z" fill="{TEAL}"/>
    <ellipse cx="0" cy="-18" rx="42" ry="10" fill="#4A2A18"/>
    <ellipse cx="-6" cy="-19" rx="20" ry="4" fill="#8A5636" stroke="none"/>
    <g fill="#FFFFFF" stroke="none"><circle cx="-22" cy="8" r="4"/><circle cx="0" cy="14" r="4"/><circle cx="22" cy="8" r="4"/></g>
  </g>
  <g stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.85">
    <path d="M636 330 q-8 -12 0 -24 q8 -12 0 -24"/><path d="M660 334 q-8 -12 0 -24 q8 -12 0 -24"/>
  </g>
  <!-- frasco de mel -->
  <g transform="translate(150 372)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-30 -36 Q-34 28 -24 32 L24 32 Q34 28 30 -36 Z" fill="{ORANGE}"/>
    <rect x="-34" y="-54" width="68" height="20" rx="6" fill="{MUSTARD}"/>
    <rect x="-22" y="-14" width="44" height="22" rx="11" fill="#FFF6EA" stroke-width="2.5"/>
  </g>
  <text x="150" y="373" text-anchor="middle" font-family="Fredoka SemiBold" font-size="10" fill="{INK}">MEL</text>
  <!-- saco de chia -->
  <g transform="translate(70 380)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-30 -34 L30 -34 L34 30 L-34 30 Z" fill="#F2E6CF"/>
    <path d="M-30 -34 L-24 -44 L24 -44 L30 -34" fill="#E2D2B2"/>
    <rect x="-22" y="-14" width="44" height="22" rx="11" fill="{TEAL}" stroke-width="2.5"/>
  </g>
  <text x="70" y="381" text-anchor="middle" font-family="Fredoka SemiBold" font-size="10" fill="#FFFFFF">CHIA</text>
  <g fill="#3B2414">{"".join(f'<ellipse cx="{x}" cy="{y}" rx="1.8" ry="1.2"/>' for x,y in [(108,414),(116,420),(124,412),(112,428),(130,424),(102,422)])}</g>
'''
svg = r.frame("Tiramisu de chia", "IOGURTE, CAFÉ E CACAU · SEM AÇÚCAR", scene, accent=COFFEE)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="0" text-anchor="middle" font-family="Pacifico" font-size="31"')
open(S + "/tiramisu-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/tiramisu-retro.png", output_width=1600)
print("ok")
