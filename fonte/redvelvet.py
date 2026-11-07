import importlib.util, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
ROSE = "#C24A6A"
RED, RED2, RED3 = "#A8253A", "#8E1D30", "#C23A4E"
CREAM = "#FFFBF2"

scene = f'''
  <ellipse cx="400" cy="406" rx="200" ry="20" fill="{INK}" opacity="0.18"/>
  <!-- prato de pé -->
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M370 404 L430 404 L420 384 L380 384 Z" fill="{TEAL}"/>
    <ellipse cx="400" cy="380" rx="170" ry="24" fill="{TEAL}"/>
    <ellipse cx="400" cy="376" rx="150" ry="18" fill="#7CC3C1" stroke-width="2"/>
  </g>
  <!-- bolo de duas camadas com fatia cortada -->
  <g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <!-- corpo exterior (cobertura branca nos lados) -->
    <path d="M272 272 L272 368 Q370 396 444 380 L444 288 Z" fill="{CREAM}"/>
    <!-- face cortada: camadas -->
    <path d="M444 288 L520 272 L520 368 L444 380 Z" fill="{RED}"/>
    <!-- topo -->
    <path d="M272 272 Q272 248 396 248 Q520 248 520 272 L444 288 Q420 294 396 294 Q272 294 272 272 Z" fill="{CREAM}"/>
  </g>
  <!-- camada de recheio branco no corte -->
  <path d="M444 326 L520 312 L520 330 L444 344 Z" fill="{CREAM}" stroke="{INK}" stroke-width="2"/>
  <path d="M444 296 L520 282" stroke="{CREAM}" stroke-width="8"/>
  <g fill="{RED2}" opacity="0.7">{"".join(f'<circle cx="{x}" cy="{y}" r="1.8"/>' for x,y in [(456,312),(476,302),(500,308),(462,360),(490,354),(510,346),(470,370)])}</g>
  <!-- migalhas vermelhas por cima -->
  <g fill="{RED3}" stroke="{INK}" stroke-width="1.5">{"".join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x,y in [(310,266),(332,272),(360,262),(388,270),(414,262),(440,268),(470,262),(352,276),(404,278),(486,270)])}</g>
  <!-- fatia servida -->
  <g transform="translate(570 344)" stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <ellipse cx="42" cy="54" rx="66" ry="14" fill="#FFFFFF"/>
    <path d="M0 6 L80 -4 L80 44 L0 52 Z" fill="{RED}"/>
    <path d="M0 6 L80 -4 L94 -10 L14 0 Z" fill="{CREAM}"/>
    <path d="M80 -4 L94 -10 L94 38 L80 44 Z" fill="{CREAM}"/>
  </g>
  <path d="M570 372 L650 362" stroke="{CREAM}" stroke-width="7"/>
  <path d="M570 368 L650 358 M570 377 L650 367" stroke="{INK}" stroke-width="1.5" opacity="0.5"/>
  <!-- beterrabas -->
  <g transform="translate(120 378)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-6 -30 Q-26 -60 -14 -66 Q-2 -56 -2 -32 Z" fill="#6FA34A"/>
    <path d="M2 -30 Q10 -64 26 -62 Q24 -44 6 -30 Z" fill="#7FB069"/>
    <path d="M0 -32 Q-34 -30 -36 2 Q-34 30 0 34 Q34 30 36 2 Q34 -30 0 -32 Z" fill="#7A1F3D"/>
    <path d="M0 34 Q2 46 8 52" fill="none"/>
    <path d="M-20 -10 Q-24 4 -18 16" stroke="#B0476A" stroke-width="4" fill="none" stroke-linecap="round"/>
  </g>
  <g transform="translate(200 404) scale(0.7)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M0 -32 Q-34 -30 -36 2 Q-34 30 0 34 Q34 30 36 2 Q34 -30 0 -32 Z" fill="#7A1F3D"/>
    <path d="M0 -32 Q4 -46 12 -50" fill="none"/>
  </g>
  <!-- limão -->
  <g transform="translate(712 398)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
    <path d="M-34 0 Q-30 -26 0 -26 Q30 -26 34 0 Q30 26 0 26 Q-30 26 -34 0 Z" fill="#F4D03F"/>
    <path d="M-34 0 L-42 -4 M34 0 L42 4" />
    <path d="M-14 -14 Q-20 -4 -16 6" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round"/>
  </g>
'''
svg = r.frame("Red Velvet", "DE BETERRABA E TÂMARAS · SEM AÇÚCAR", scene, accent=ROSE)
svg = svg.replace('<text x="0" y="6" text-anchor="middle" font-family="Pacifico" font-size="38"', '<text x="0" y="2" text-anchor="middle" font-family="Pacifico" font-size="35"')
open(S + "/redvelvet-retro.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/redvelvet-retro.png", output_width=1600)
print("ok")
