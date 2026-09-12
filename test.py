from authorization_extractor import extract_authorization_form
from pdf_extractor import PDFExtractor

extractor = PDFExtractor("documents/authorization_form.pdf")

print("Has form fields:", extractor.has_form_fields())

print("\n--- PDF TEXT ---")
print(extractor.get_text())

member, provider, procedures = extract_authorization_form("documents/authorization_form.pdf")

print("\n--- MEMBER ---")
print(member)

print("\n--- PROVIDER ---")
print(provider)

print("\n--- PROCEDURES ---")

for procedure in procedures:
    print(procedure)
