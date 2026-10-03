from pdf_extractor import PDFExtractor
from anthem_extractor import *


pdf_path = "documents/anthem_authorization_form_2.pdf"



extractor = PDFExtractor(pdf_path)


print("\n--- ANTHEM DEMOGRAPHICS ---")
member = extractor_anthem_member(pdf_path)
print(member)


print("\n--- ANTHEM ORDERING PHYSICIAN ---")
ordering_physician = extracting_ordering_physician(extractor)
print(ordering_physician)

print("\n--- ANTHEM AGENCY INFORMATION ---")
agency = extract_agency_information(extractor)
print(agency)


print("\n--- ANTHEM BCBA INFORMATION ---")
bcba = extract_bcba_information(extractor)
print(bcba)


print("\n--- ANTHEM ASSESSMENT & TREATMENT ---")

print(
    "Age of First ABA Treatment:",
    extract_age_first_aba_treatment(extractor)
)

print(
    "Start Date of Current Request:",
    extract_start_date_current_request(extractor)
)

for treatment in extract_treatments(extractor):
    print(treatment)



print("\n--- ANTHEM PROVIDER INFORMATION ---")

provider_name, license_information = extract_anthem_provider_info(extractor)

print("Provider Name:", provider_name)
print("License Information:", license_information)

print("\n--- ANTHEM PROVIDER DATE ---")

provider_date = extract_anthem_provider_date(extractor)

print("Provider Date:", provider_date)

print("\n--- COMPLETE ANTHEM FORM ---")

form = extract_anthem_form(pdf_path)

print(form)