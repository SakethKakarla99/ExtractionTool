import cv2
from pypdf import PdfReader
from models import Member, Provider
from checkbox_detector import is_checked


def extract_authorization_form(pdf_path):

    reader = PdfReader(pdf_path)

    fields = reader.get_fields()

    if not fields:
        raise ValueError("No form fields found in PDF")

    def get_value(field_name):
        for name, field in fields.items():
            normalized_name = " ".join(name.split())
            normalized_search = " ".join(field_name.split())
        
            if normalized_name == normalized_search:

                value = field.get("/V")

                if value is None or value == "":
                    return None
                return str(value).strip()
        return None

     # Member Information

    full_name = get_value("Member Name (Last, First)")

    first_name = None
    last_name = None

    if full_name and "," in full_name:
        last_name, first_name = full_name.split(",",1)

        last_name = last_name.strip()
        first_name = first_name.strip()

    sex = get_value("Sex")

    if sex:
        sex =  sex.replace("/", "")

    age = get_value("Age")

    if age:
        age = int(age)

    member = Member(
        first_name = first_name,
        last_name = last_name,
        sex = sex,
        age = age,
        dob = get_value("DOB"),
        cin = get_value("Client Index CIN"),
        icd10_dx = get_value("ICD10 Diagnosis"),
        mailing_address = get_value("Mailing Address"),
        phone = get_value("Phone")
    )

    # Provider Information

    provider = Provider(
        aba_provider = get_value("ABA Provider"),
        npi = get_value("Provider NPI"),
        tin = get_value("Provider TIN"),
        medi_cal_id = get_value("Provider MediCal ID"),
        address = get_value("Provider Address"),
        phone = get_value("Provider Phone"),
        fax = get_value("Provider Fax"),
        office_contact = get_value("Provider Office Contact")
    )

    return member, provider


        


