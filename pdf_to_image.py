import fitz

pdf = fitz.open("documents/anthem_authorization_form.pdf")

page = pdf[0]

pix = page.get_pixmap(matrix = fitz.Matrix(2,2))

pix.save("anthem_page_1.png")

pdf.close()

print("Saved anthem_page_1.png")