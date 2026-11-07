import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
NAVY = "#2F5D7C"

def glass(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <ellipse cx="0" cy="92" rx="38" ry="9" fill="#FFFFFF"/>
  <path d="M-6 60 L-6 88 L6 88 L6 60 Z" fill="#E8F3F6"/>
  <path d="M-58 -10 Q-56 58 0 62 Q56 58 58 -10 Z" fill="#E8F3F6"/>
  <path d="M-52 4 Q-48 52 0 55 Q48 52 52 4 Z" fill="#5A321D" stroke-width="2.5"/>
  <ellipse cx="0" cy="-10" rx="58" ry="14" fill="#F4FAFB"/>
  <path d="M-48 -4 Q-30 -26 -6 -16 Q10 -34 30 -18 Q50 -20 48 -4 Q0 8 -48 -4 Z" fill="#6E4027"/>
  <path d="M-26 -14 q8 -6 16 0 M8 -18 q8 -6 16 2" stroke="#8A5636" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <g fill="#C89A5E" stroke-width="2"><circle cx="-14" cy="-20" r="5"/><circle cx="6" cy="-26" r="4.5"/><circle cx="22" cy="-16" r="4"/><circle cx="-2" cy="-12" r="3.5"/></g>
  <path d="M-44 10 Q-42 34 -30 46" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.8"/>
</g>'''

def avocado_half(x, y, rot, s=1.0):
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M0 -50 Q-22 -48 -26 -14 Q-40 10 -36 30 Q-28 56 0 56 Q28 56 36 30 Q40 10 26 -14 Q22 -48 0 -50 Z" fill="#3E5A23"/>
  <path d="M0 -42 Q-16 -40 -19 -12 Q-31 10 -28 28 Q-22 47 0 47 Q22 47 28 28 Q31 10 19 -12 Q16 -40 0 -42 Z" fill="#C9DE7C" stroke-width="2.5"/>
  <path d="M0 -30 Q-10 -28 -12 -8 Q-20 8 -18 22 Q-14 36 0 36 Q14 36 18 22 Q20 8 12 -8 Q10 -28 0 -30 Z" fill="#E6EFA6" stroke="none"/>
  <circle cx="0" cy="20" r="15" fill="#8A5530"/>
  <path d="M-6 12 q4 -4 8 -2" stroke="#B07A44" stroke-width="2.5" fill="none" stroke-linecap="round"/>
</g>'''

def avocado_whole(x, y, rot):
    return f'''<g transform="translate({x} {y}) rotate({rot})" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <path d="M0 -46 Q-20 -44 -24 -12 Q-36 10 -32 28 Q-26 52 0 52 Q26 52 32 28 Q36 10 24 -12 Q20 -44 0 -46 Z" fill="#3E5A23"/>
  <path d="M-14 -20 Q-18 0 -22 14" stroke="#5C7A33" stroke-width="4" fill="none" stroke-linecap="round"/>
  <g fill="#2E4419" stroke="none"><circle cx="10" cy="-10" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="2" cy="30" r="2"/><circle cx="-10" cy="22" r="2"/></g>
</g>'''

scene = f'''
  <ellipse cx="400" cy="408" rx="160" ry="18" fill="{INK}" opacity="0.18"/>
  {avocado_whole(500, 352, 25)}
  {glass(310, 312)}
  {glass(440, 318, 0.9)}
  {avocado_half(590, 360, 15, 0.95)}
  {r.banana(44, 296, -10)}
  <!-- lata de cacau -->
  <g transform="translate(160 372)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <rect x="-36" y="-56" width="72" height="88" rx="6" fill="{CHERRY}"/>
    <ellipse cx="0" cy="-56" rx="36" ry="9" fill="#B23A2F"/>
    <rect x="-28" y="-30" width="56" height="34" rx="6" fill="#FFF6EA" stroke-width="2.5"/>
    <path d="M-36 20 L36 20" stroke-width="2.5"/>
  </g>
  <text x="160" y="356" text-anchor="middle" font-family="Fredoka SemiBold" font-size="12" fill="{INK}">CACAU</text>
  <text x="160" y="368" text-anchor="middle" font-family="Fredoka" font-size="8" fill="{INK}">100%</text>
  <!-- colher -->
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <path d="M660 420 L740 394" stroke-width="7" stroke-linecap="round"/>
    <path d="M660 420 L740 394" stroke="#D9DDE0" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="652" cy="423" rx="16" ry="10" fill="#D9DDE0" transform="rotate(-18 652 423)"/>
  </g>
  <g transform="translate(720 360)">{"".join(f'<g transform="translate({x} {y})" stroke="{INK}" stroke-width="2.5"><ellipse rx="10" ry="8" fill="#C89A5E"/><path d="M0 -8 Q-2 0 0 8" fill="none" stroke-width="2"/></g>' for x,y in [(0,0),(-22,12),(14,18)])}</g>
'''
svg = r.frame("Mousse", "DE CHOCOLATE SAUDÁVEL", scene, accent=NAVY)
open(S + "/mousse-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/mousse-retro.png", output_width=1600)
print("ok")
