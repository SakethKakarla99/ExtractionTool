import pymupdf
import os


def pdf_page_to_image(pdf_path, page_number=1):
    pdf = pymupdf.open(pdf_path)

    page = pdf[page_number - 1]

    pix = page.get_pixmap(
        matrix=pymupdf.Matrix(2, 2)
    )

    pdf_name = os.path.splitext(
        os.path.basename(pdf_path)
    )[0]

    image_path = f"{pdf_name}_page_{page_number}.png"

    pix.save(image_path)

    pdf.close()

    return image_path