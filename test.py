import json
from caloptima_extractor import extract_authorization_form
from pdf_extractor import PDFExtractor
from validator import validate_authorization_form
from anthem_extractor import inspect_anthem_form, extractor_anthem_member, extracting_ordering_physician, extract_agency_name, extract_agency_tid, extract_agency_npi


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

print("\n--- ANTHEM FORM FIELDS ---")

anthem_fields = inspect_anthem_form(
    "documents/anthem_authorization_form.pdf"
)

for name, value in anthem_fields.items():
    print(f"{name}: {value}")

print("\n--- ANTHEM Demographics ---")
anthem_member = extractor_anthem_member("documents/anthem_authorization_form.pdf")
print(anthem_member)

print("\n--- ANTHEM ORDERING PHYSICIAN ---")
extractor = PDFExtractor(
    "documents/anthem_authorization_form.pdf"
)
ordering_physician = extracting_ordering_physician(extractor)
print(ordering_physician)

print("\n--- ANTHEM AGENCY INFORMATION ---")
agency_name = extract_agency_name(extractor)
print(agency_name)

agency_tid = extract_agency_tid(extractor)
print(agency_tid)

agency_npi = extract_agency_npi(extractor)
print(agency_npi)

print("\n--- VALIDATION ---")

errors = validate_authorization_form(authorization_form)

if not errors:
    print("Authorization form is valid")
else:
    print("Authorization form has validation errors:")

    for error in errors:
        print("-", error)
