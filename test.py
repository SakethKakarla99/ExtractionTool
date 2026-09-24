import json
from caloptima_extractor import extract_authorization_form
from pdf_extractor import PDFExtractor
from validator import validate_authorization_form
from anthem_extractor import  *


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

#print("\n--- ANTHEM FORM FIELDS ---")

#anthem_fields = inspect_anthem_form(
    #"documents/anthem_authorization_form.pdf"
#)

#for name, value in anthem_fields.items():
    #print(f"{name}: {value}")

print("\n--- ANTHEM Demographics ---")
anthem_member = extractor_anthem_member("documents/anthem_authorization_form.pdf")
print(anthem_member)

print("\n--- ANTHEM ORDERING PHYSICIAN ---")
extractor = PDFExtractor(
    "documents/anthem_authorization_form.pdf"
)
ordering_physician = extracting_ordering_physician(extractor)
print(ordering_physician)

# ANTHEM AGENCY INFORMATION

agency = extract_agency_information(
    extractor,
    "anthem_page_1.png"
)

print("\n--- ANTHEM AGENCY INFORMATION ---")
print(agency)

# BCBA PROVIDER INFORMATION

print("\n--- BCBA PROVIDER INFORMATION ---")
bcba = extract_bcba_information(extractor, "anthem_page_1.png")
print(bcba)

#print("\n--- TEST AGE OF FIRST ABA")
#extractor.print_text_coordinates(page_number = 2)

print("\n--- AGE FIRST ABA TREATMENT ---")
print("Age of Frist ABA Treatment: ", extract_age_first_aba_treatment(extractor))

print("\n--- DATE OF CURRENT REQUEST ---")
print("Start Date of Current Request:", extract_start_date_current_request(extractor))

print("\n--- TREATMENT PAGE WIDGETS ---")

print("\n--- ANTHEM TREATMENTS ---")
treatments = extract_treatments(extractor)
for treatment in treatments:
    print(treatment)

print("\n--- Provider Name ---")
provider_name, license_information = extract_anthem_provider_info(extractor)
print("Provider Name:", provider_name)
print("License Information:", license_information)

position =  extractor.find_text_position("Diagnosis")
print("\n--- Diagnosis Position ---")
print(position)

print("\n YUUURRR")

print("\n--- PHYSICIAN ADDRESS TEST ---")
print(extract_physician_address(extractor))


print("\n--- VALIDATION ---")

errors = validate_authorization_form(authorization_form)

if not errors:
    print("Authorization form is valid")
else:
    print("Authorization form has validation errors:")

    for error in errors:
        print("-", error)
