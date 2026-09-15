import json
from authorization_extractor import extract_authorization_form
from pdf_extractor import PDFExtractor
from validator import validate_authorization_form


extractor = PDFExtractor("documents/authorization_form_3.pdf")

print("Has form fields:", extractor.has_form_fields())

print("\n--- PDF TEXT ---")
print(extractor.get_text())

authorization_form = extract_authorization_form("documents/authorization_form_3.pdf")

print("\n--- MEMBER ---")
print(authorization_form.member)

print("\n--- PROVIDER ---")
print(authorization_form.provider)

print("\n--- PROCEDURES ---")

for procedure in authorization_form.procedures:
    print(procedure)

print("\n--- DICTIONARY ---")
print(authorization_form.to_dict())

print("\n--- JSON ---")
print(
    json.dumps(
        authorization_form.to_dict(),
        indent = 4
    )
)

print("\n--- VALIDATION ---")

errors = validate_authorization_form(authorization_form)

if not errors:
    print("Authorization form is valid")
else:
    print("Authorization form has validation errors:")

    for error in errors:
        print("-", error)
