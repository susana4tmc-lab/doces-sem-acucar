import importlib.util, sys, random
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
GREEN = "#2E7D5B"
random.seed(3)

def ball(x, y, rad=16, fill="#8A5530", coat=None):
    specks = "".join(f'<circle cx="{x+random.uniform(-rad*0.6, rad*0.6):.1f}" cy="{y+random.uniform(-rad*0.6, rad*0.6):.1f}" r="1.6" fill="{coat or "#5A321D"}"/>' for _ in range(6))
    return (f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{x-rad*0.55} {y-rad*0.3} q{rad*0.3} {-rad*0.4} {rad*0.7} {-rad*0.45}" stroke="#B07A44" stroke-width="2.5" fill="none" stroke-linecap="round"/>' + specks)

balls = ""
pos = [(330, 340), (366, 342), (402, 344), (438, 342), (474, 340),
       (348, 316), (384, 318), (420, 318), (456, 316),
       (366, 292), (402, 294), (438, 292),
       (384, 268), (420, 268)]
fills = ["#8A5530", "#7A4630", "#9C6338"]
for i, (x, y) in enumerate(pos):
    coat = "#FFFFFF" if i % 4 == 1 else None
    f = "#F2E7D3" if i % 4 == 1 else fills[i % 3]
    balls += ball(x, y, 17, f, coat)

def jar(x, y, label, fill, content):
    return f'''<g transform="translate({x} {y})">
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-34 -40 Q-38 34 -28 38 L28 38 Q38 34 34 -40 Z" fill="#FFFDF5"/>
  </g>
  {content}
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-34 -40 Q-38 34 -28 38 L28 38 Q38 34 34 -40 Z" fill="none"/>
    <rect x="-38" y="-58" width="76" height="20" rx="6" fill="{fill}"/>
    <rect x="-31" y="-14" width="62" height="24" rx="12" fill="#FFF6EA" stroke-width="2.5"/>
  </g>
  <text x="0" y="3" text-anchor="middle" font-family="Fredoka SemiBold" font-size="8.5" fill="{INK}">{label}</text>
</g>'''

peanut = '<path d="M-30 -20 L30 -20 L28 34 L-28 34 Z" fill="#C98B52" opacity="0.9"/>'
dates = "".join(f'<g transform="translate({dx} {dy}) rotate({a})"><ellipse rx="12" ry="6" fill="#6B3A1E" stroke="{INK}" stroke-width="2.5"/></g>' for dx, dy, a in [(-14, 22, 20), (10, 26, -15), (-4, 8, 5), (16, 6, 40), (-18, -6, -30)])

scene = f'''
  <ellipse cx="402" cy="404" rx="170" ry="18" fill="{INK}" opacity="0.18"/>
  <g stroke="{INK}" stroke-width="3.5">
    <ellipse cx="402" cy="372" rx="150" ry="30" fill="{CHERRY}"/>
    <ellipse cx="402" cy="366" rx="128" ry="22" fill="#FFF6EA" stroke-width="2"/>
  </g>
  {balls}
  {jar(150, 370, "AMENDOIM", MUSTARD, peanut)}
  {jar(660, 370, "TÂMARAS", TEAL, dates)}
  <!-- amêndoas e cajus soltos -->
  {"".join(f'<g transform="translate({x} {y}) rotate({a})" stroke="{INK}" stroke-width="2.5"><path d="M0 -10 Q9 -2 0 12 Q-9 -2 0 -10 Z" fill="#C98B52"/></g>' for x, y, a in [(60, 412, 30), (88, 420, -20), (240, 420, 10)])}
  {"".join(f'<g transform="translate({x} {y}) rotate({a})" stroke="{INK}" stroke-width="2.5"><path d="M-10 -4 Q-12 10 2 12 Q12 10 10 2 Q4 4 2 -2 Q0 -8 -10 -4 Z" fill="#E8C98C"/></g>' for x, y, a in [(560, 418, 10), (590, 424, -30), (740, 420, 40)])}
'''
svg = r.frame("Bolinhas", "ENERGÉTICAS · SEM AÇÚCAR", scene, accent=GREEN)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="2" text-anchor="middle" font-family="Pacifico" font-size="36"')
open(S + "/bolinhas-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/bolinhas-retro.png", output_width=1600)
print("ok")
