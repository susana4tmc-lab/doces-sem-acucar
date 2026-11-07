import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
MAGENTA = "#B4527F"

def almond(x, y, rot, s=1.0):
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="{INK}" stroke-width="2.5"><path d="M0 -10 Q9 -2 0 12 Q-9 -2 0 -10 Z" fill="#C98B52"/><path d="M0 -5 L0 6" stroke="#A86A36" stroke-width="1.5"/></g>'

def walnut(x, y, s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="2.5"><ellipse rx="10" ry="8" fill="#D2A66A"/><path d="M0 -8 Q-2 0 0 8 M-6 -3 q3 2 0 4 M5 -3 q-3 2 0 4" fill="none" stroke-width="1.8"/></g>'

def raisin(x, y, s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="2.2"><path d="M-6 -4 Q0 -9 6 -4 Q8 4 2 7 Q-6 8 -7 2 Z" fill="#5B2A3E"/><path d="M-3 -2 q3 2 5 0" stroke="#7E4258" stroke-width="1.5" fill="none"/></g>'

def bonbon(x, y, top):
    return f'''<g transform="translate({x} {y})">
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <path d="M-20 0 Q-22 -14 -10 -16 L12 -16 Q22 -14 20 0 Q20 10 10 12 L-10 12 Q-20 10 -20 0 Z" fill="#4E2A19"/>
  </g>
  <path d="M-14 -8 Q0 -12 14 -8" stroke="#7A4630" stroke-width="3" fill="none" stroke-linecap="round"/>
  {top}
</g>'''

tops = [
  almond(-6,-6,30,0.8)+walnut(7,-4,0.7),
  raisin(-6,-4,0.9)+almond(7,-6,-20,0.8),
  walnut(0,-5,0.85)+raisin(10,-2,0.7),
  almond(-7,-4,10,0.8)+raisin(6,-6,0.8),
]
grid = ""
k = 0
for row, yy in enumerate((330, 360, 390)):
    for col in range(5):
        xx = 318 + col * 62 - (row * 14)
        grid += bonbon(xx, yy, tops[k % 4]); k += 1

def bowl(x, y, color, content):
    return f'''<g transform="translate({x} {y})">
  {content}
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-46 -10 Q-42 26 0 30 Q42 26 46 -10 Z" fill="{color}"/>
    <path d="M-46 -10 Q0 0 46 -10" fill="none"/>
  </g>
  <g fill="#FFFFFF"><circle cx="-24" cy="8" r="4"/><circle cx="0" cy="14" r="4"/><circle cx="24" cy="8" r="4"/></g>
</g>'''

scene = f'''
  <ellipse cx="420" cy="420" rx="210" ry="18" fill="{INK}" opacity="0.18"/>
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M222 412 L612 412 L648 300 L258 300 Z" fill="#B9C3C8"/>
    <path d="M222 412 L612 412 L612 422 L222 422 Z" fill="#8E9AA0"/>
    <path d="M612 412 L648 300 L648 310 L612 422 Z" fill="#7D888E"/>
    <path d="M238 404 L600 404 L630 310 L268 310 Z" fill="#FFF8EC" stroke-width="2"/>
  </g>
  {grid}
  {bowl(120, 330, TEAL, walnut(-18,-14)+walnut(2,-18)+walnut(20,-12)+walnut(-6,-8))}
  {bowl(110, 410, MUSTARD, almond(-20,-12,20)+almond(-4,-18,-15)+almond(14,-12,40)+almond(26,-8,-30)+almond(4,-8,0))}
  {bowl(712, 390, ORANGE, raisin(-18,-12)+raisin(-4,-16)+raisin(12,-14)+raisin(24,-8)+raisin(2,-6)+raisin(-14,-4))}
  <!-- tablete de chocolate -->
  <g transform="translate(700 318) rotate(-12)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <rect x="-40" y="-26" width="80" height="52" rx="4" fill="#4E2A19"/>
    <path d="M-40 -26 L-40 26 L-10 26 L-10 -26 Z" fill="{CHERRY}"/>
    <path d="M14 -26 L14 26 M-10 0 L40 0" stroke="#3A1E11" stroke-width="2.5"/>
  </g>
  <text x="672" y="328" transform="rotate(-102 672 328)" text-anchor="middle" font-family="Fredoka SemiBold" font-size="10" fill="#FFFFFF">70%</text>
'''
svg = r.frame("Afogados", "FRUTOS SECOS NO CHOCOLATE", scene, accent=MAGENTA)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="0" text-anchor="middle" font-family="Pacifico" font-size="33"')
open(S + "/afogados-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/afogados-retro.png", output_width=1600)
print("ok")
