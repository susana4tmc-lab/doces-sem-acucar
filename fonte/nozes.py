import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
OLIVE = "#7A8B3C"

def walnut(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
  <ellipse cx="0" cy="0" rx="18" ry="15" fill="#C89A5E"/>
  <path d="M0 -15 Q-3 0 0 15" fill="none" stroke-width="2.5"/>
  <path d="M-10 -6 q4 3 0 6 M8 -7 q-4 3 0 6 M-9 5 q4 2 1 6" fill="none" stroke-width="2"/>
</g>'''

def chunk(x, y, rot):
    return f'''<g transform="translate({x} {y}) rotate({rot})" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
  <path d="M0 0 L22 -4 L26 14 L4 18 Z" fill="#3A1E11"/>
  <path d="M0 0 L22 -4 L28 -10 L6 -6 Z" fill="#5A321D"/>
</g>'''

scene = f'''
  <ellipse cx="390" cy="404" rx="210" ry="22" fill="{INK}" opacity="0.18"/>
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M200 396 L580 396 L612 360 L232 360 Z" fill="{MUSTARD}"/>
    <path d="M200 396 L580 396 L580 406 L200 406 Z" fill="#C88A2A"/>
    <path d="M580 396 L612 360 L612 370 L580 406 Z" fill="#B07A22"/>
  </g>
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M250 300 L250 368 L490 368 L490 300 Z" fill="#A0693A"/>
    <path d="M490 300 L540 286 L540 354 L490 368 Z" fill="#E2C18A"/>
    <path d="M250 300 Q250 262 330 258 L470 254 Q540 252 540 286 L490 300 Q370 316 250 300 Z" fill="#8A5530"/>
  </g>
  <!-- pedaços de chocolate e nozes no miolo -->
  <g fill="#3A1E11">{"".join(f'<rect x="{x}" y="{y}" width="7" height="6" rx="1"/>' for x,y in [(498,306),(518,322),(504,340),(526,300),(512,352),(530,336)])}</g>
  <g fill="#C89A5E">{"".join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x,y in [(508,318),(524,346),(500,330)])}</g>
  <!-- cobertura de nozes e chocolate no topo -->
  {walnut(310, 276, 0.8)}{walnut(400, 272, 0.8)}{walnut(470, 268, 0.75)}
  {chunk(345, 268, -10)}{chunk(430, 262, 12)}
  <!-- fatia servida -->
  <g transform="translate(598 334)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <ellipse cx="38" cy="58" rx="62" ry="14" fill="#FFFFFF"/>
    <path d="M0 0 L60 0 L60 52 L0 52 Z" fill="#E2C18A"/>
    <path d="M0 0 Q4 -16 30 -18 Q56 -16 60 0 Z" fill="#8A5530"/>
    <path d="M60 0 L74 -6 L74 46 L60 52 Z" fill="#A0693A"/>
  </g>
  <g fill="#3A1E11">{"".join(f'<rect x="{598+x}" y="{334+y}" width="7" height="6" rx="1"/>' for x,y in [(12,14),(38,26),(20,38)])}</g>
  {r.banana(44, 296, -10)}
  <!-- frasco de mel -->
  <g transform="translate(150 362)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-32 -40 Q-36 30 -26 34 L26 34 Q36 30 32 -40 Z" fill="{ORANGE}"/>
    <rect x="-36" y="-58" width="72" height="20" rx="6" fill="{CHERRY}"/>
    <path d="M-36 -48 L36 -48" stroke-dasharray="6 6" stroke="#FFFFFF" stroke-width="3"/>
    <rect x="-22" y="-20" width="44" height="26" rx="13" fill="#FFF6EA" stroke-width="2.5"/>
    <path d="M-20 -30 Q-28 -10 -22 20" stroke="#F4A65A" stroke-width="5" fill="none" stroke-linecap="round"/>
  </g>
  <text x="150" y="360" text-anchor="middle" font-family="Fredoka SemiBold" font-size="12" fill="{INK}">MEL</text>
  <!-- nozes soltas -->
  {walnut(80, 418)}{walnut(116, 428, 0.9)}
  {chunk(700, 392, -20)}{chunk(736, 398, 10)}
  {walnut(724, 372, 0.95)}
'''
svg = r.frame("Bolo de banana", "COM MEL, NOZES E CACAU", scene, accent=OLIVE)
open(S + "/bolo-nozes-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/bolo-nozes-retro.png", output_width=1600)
print("ok")
