"""Impõe um PDF A5 em folhas A4 deitadas, na ordem de livrinho (frente e verso, dobrar ao meio)."""
import sys
from pypdf import PdfReader, PdfWriter, Transformation, PageObject

src, out = sys.argv[1], sys.argv[2]
r = PdfReader(src)
pages = list(r.pages)
n = len(pages)
assert n % 4 == 0, n
w = float(pages[0].mediabox.width)
h = float(pages[0].mediabox.height)

wr = PdfWriter()
for i in range(n // 4):
    for left, right in ((n - 2 * i, 2 * i + 1), (2 * i + 2, n - 2 * i - 1)):
        sheet = PageObject.create_blank_page(width=2 * w, height=h)
        sheet.merge_transformed_page(pages[left - 1], Transformation().translate(0, 0))
        sheet.merge_transformed_page(pages[right - 1], Transformation().translate(w, 0))
        wr.add_page(sheet)
with open(out, "wb") as f:
    wr.write(f)
print(n // 4, "folhas,", n // 2, "faces")
