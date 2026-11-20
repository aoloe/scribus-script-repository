# Create a foldable fanzine

The 8 pages should be on the same side of the A4 landscape sheet.
In the top half there should be the pages 7, 6, 4, 4 rotate by 180°.
In the lower half the pages 1, 8, 2, 3 


```
from pypdf import PdfReader, PdfWriter, PageObject, Transformation

reader = PdfReader("input.pdf")
writer = PdfWriter()

# A4 landscape dimensions in PDF points
A4_WIDTH = 841.89
A4_HEIGHT = 595.28

# A7 dimensions
A7_WIDTH = 209.76
A7_HEIGHT = 297.64

# Create output sheet
sheet = PageObject.create_blank_page(
    width=A4_WIDTH,
    height=A4_HEIGHT
)

# Page arrangement, left to right, top to bottom
layout = [
    (7, False), (6, False), (5, False), (4, True),
    (1, False), (8, False), (2, False), (3, False),
]

for i, (page_num, rotate_180) in enumerate(layout):
    page = reader.pages[page_num - 1]

    col = i % 4
    row = i // 4

    x = col * A7_WIDTH
    y = A7_HEIGHT if row == 0 else 0

    if rotate_180:
        transform = (
            Transformation()
            .rotate(180)
            .translate(
                tx=x + A7_WIDTH,
                ty=y + A7_HEIGHT
            )
        )
    else:
        transform = Transformation().translate(
            tx=x,
            ty=y
        )

    sheet.merge_transformed_page(page, transform)

writer.add_page(sheet)

with open("fanzine.pdf", "wb") as f:
    writer.write(f)
```
