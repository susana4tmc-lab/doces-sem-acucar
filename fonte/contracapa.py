import importlib.util, sys, base64, io
from PIL import Image
S = sys.argv[1]
U = S + "/logos/"  # logótipos originais: Agrupamento, Associação de Pais, UCC Loures
spec = importlib.util.spec_from_file_location("retro", S + "/retro.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
INK, CREAM, MUSTARD, ORANGE, TEAL, CHERRY = r.INK, r.CREAM, r.MUSTARD, r.ORANGE, r.TEAL, r.CHERRY
W, H = 600, 820

logos = [("05513d23-image.png", 4), ("4f31b1e4-image.jpg", 2), ("43c42970-image.jpg", 0)]
uris = []
for f, crop in logos:
    im = Image.open(U + f).convert("RGB")
    im = im.crop((crop, crop, im.width - crop, im.height - crop))
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            rr, gg, bb = px[x, y]
            if min(rr, gg, bb) > 225: px[x, y] = (255, 255, 255)
            elif bb > 150 and bb > rr + 60 and bb > gg + 30 and f.startswith("05513"): px[x, y] = (255, 255, 255)
    im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
    im.save(S + "/logo-" + f.split("-")[0] + ".png")
    b = io.BytesIO(); im.save(b, "PNG")
    uris.append(("data:image/png;base64," + base64.b64encode(b.getvalue()).decode(), im.width / im.height))


def tile(cx, cy, w, h, uri, ratio):
    pad = 10
    iw, ih = w - 2 * pad, h - 2 * pad
    if iw / ih > ratio:
        iw = ih * ratio
    else:
        ih = iw / ratio
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="18" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
            f'<image x="{cx-iw/2:.1f}" y="{cy-ih/2:.1f}" width="{iw:.1f}" height="{ih:.1f}" href="{uri}" preserveAspectRatio="xMidYMid meet"/>')


def gingham(y, h):
    g = [f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="#FFF6EA"/>', f'<g fill="{CHERRY}" opacity="0.45">']
    g += [f'<rect x="{x}" y="{y}" width="20" height="{h}"/>' for x in range(0, W, 40)]
    g.append(f'</g><g fill="{CHERRY}" opacity="0.45">')
    g += [f'<rect x="0" y="{yy}" width="{W}" height="20"/>' for yy in range(y, y + h, 40)]
    g.append('</g>')
    return "\n".join(g)


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W*2}" height="{H*2}">
<defs><clipPath id="c"><rect x="16" y="16" width="{W-32}" height="{H-32}" rx="40"/></clipPath></defs>
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{TEAL}"/>
  {r.halftone(16, 16, W, 700, step=16, color="#FFFFFF", op=0.16)}
  {r.sunburst(300, 760, 470, n=28)}
  <circle cx="300" cy="760" r="200" fill="#F7D58E"/>
  {r.star(70, 90, 14, "#FFFFFF")}{r.star(530, 70, 11, "#FFFFFF")}{r.star(540, 140, 7, CREAM)}{r.star(60, 160, 7, CREAM)}

  <!-- cartão central -->
  <g transform="translate(300 330)">
    <rect x="-250" y="-250" width="500" height="470" rx="40" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>
    <rect x="-238" y="-238" width="476" height="446" rx="32" fill="none" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7 7"/>
    <text x="0" y="-180" text-anchor="middle" font-family="Pacifico" font-size="40" fill="{CHERRY}">Obrigado!</text>
    <text x="0" y="-140" text-anchor="middle" font-family="Fredoka SemiBold" font-size="15" letter-spacing="2.5" fill="{INK}">UM LIVRO FEITO EM PARCERIA</text>
    {tile(-115, -40, 190, 150, *uris[0])}
    {tile(115, -40, 190, 150, *uris[1])}
    {tile(0, 128, 240, 140, *uris[2])}
  </g>

  {gingham(700, 120)}
  <rect x="0" y="700" width="{W}" height="6" fill="{INK}" opacity="0.15"/>

  <!-- fita -->
  <g transform="translate(300 620)">
    <path d="M-230 -20 L-200 -20 L-200 24 L-230 24 L-216 2 Z" fill="#B23A2F" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M230 -20 L200 -20 L200 24 L230 24 L216 2 Z" fill="#B23A2F" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
    <rect x="-205" y="-26" width="410" height="44" rx="6" fill="{CHERRY}" stroke="{INK}" stroke-width="3.5"/>
    <text x="0" y="4" text-anchor="middle" font-family="Fredoka SemiBold" font-size="19" fill="#FFFFFF">a fruta adoça, com casca e tudo!</text>
  </g>

  <g transform="translate(300 752)">
    <rect x="-230" y="-28" width="460" height="56" rx="28" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>
    <text x="0" y="-3" text-anchor="middle" font-family="Fredoka SemiBold" font-size="15" letter-spacing="1.5" fill="{INK}">DIA DA ALIMENTAÇÃO · 16 DE OUTUBRO DE 2026</text>
    <text x="0" y="17" text-anchor="middle" font-family="Fredoka" font-size="13" fill="{INK}">Escola Básica João Villaret · Loures</text>
  </g>
</g>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="40" fill="none" stroke="{INK}" stroke-width="7"/>
</svg>'''
open(S + "/contracapa.svg", "w").write(svg)
r.cairosvg.svg2png(bytestring=svg.encode(), write_to=S + "/contracapa.png", output_width=1200)
print("ok")
