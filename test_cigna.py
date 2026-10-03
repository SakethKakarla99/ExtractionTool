from pdf_extractor import PDFExtractor


pdf_path = "documents/cigna_authorization_form.pdf"

extractor = PDFExtractor(pdf_path)

print("\n--- CIGNA PDF INFO ---")
print("Has form fields:", extractor.has_form_fields())
print("Has embedded text:", bool(extractor.get_text()))

print("\n--- CIGNA FORM FIELDS ---")

fields = extractor.get_all_fields()

for name, value in fields.items():
    print(f"{name}: {value}")

