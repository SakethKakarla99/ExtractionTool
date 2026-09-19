from models import Member, Provider, RequestedProcedure, AuthorizationForm
from pdf_extractor import PDFExtractor
from datetime import datetime
import re



def extract_authorization_form(pdf_path):

    extractor = PDFExtractor(pdf_path)

    # Member Information

    full_name = extractor.get_field("Member Name (Last, First)")

    first_name = None
    last_name = None

    if full_name and "," in full_name:
        last_name, first_name = full_name.split(",",1)

        last_name = last_name.strip()
        first_name = first_name.strip()

    sex = extractor.get_field("Sex")

    if sex:
        sex =  sex.replace("/", "")

    age = extractor.get_field("Age")

    if age:
        age = float(age)

    member = Member(
        first_name = first_name,
        last_name = last_name,
        sex = sex,
        age = age,
        dob = extractor.normalize_date(extractor.get_field("DOB")),
        cin = extractor.get_field("Client Index CIN"),
        icd10_dx = extractor.get_field("ICD10 Diagnosis"),
        mailing_address = extractor.get_field("Mailing Address"),
        phone = extractor.get_field("Phone")
    )

    signature_present = False
    signature_name = None
    signature_date = None

    signature_data = extractor.get_raw_field("Provider Signature")

    if isinstance(signature_data, dict):
        signature_present = True
        signature_name = signature_data.get("/Name")
        signature_date = extractor.parse_pdf_date(
            signature_data.get("/M")
        )
    # Provider Information

    provider = Provider(
        aba_provider = extractor.get_field("ABA Provider"),
        npi = extractor.get_field("Provider NPI"),
        tin = extractor.get_field("Provider TIN"),
        medi_cal_id = extractor.get_field("Provider MediCal ID"),
        address = extractor.get_field("Provider Address"),
        phone = extractor.get_field("Provider Phone"),
        fax = extractor.get_field("Provider Fax"),
        office_contact = extractor.get_field("Provider Office Contact"),
        signature_present = signature_present,
        signature_name = signature_name,
        signature_date = signature_date
    )

    procedure_definitions = [
    ("H0031", "Mental health assessment by non-physician", "Units and Duration for H0031"),
    ("H0032-HN", "Mental health service plan development by non-physician (Non-BCBA)", "Units and Duration for H0032HN"),
    ("H0032-HO", "Mental health service plan development by non-physician (BCBA)", "Units and Duration for H0032HO"),
    ("H2014", "Skills training and development", "Units and Duration for H2014"),
    ("H2019", "Therapeutic behavioral services", "Units and Duration for H2019"),
    ("S5108", "Home care training to home care client", "Units and Duration for S5108"),
    ("S5110", "Home care training, family", "Units and Duration for S5110"),]

    procedures = []

    for code, description, field_name in procedure_definitions:
        units_duration = extractor.get_field(field_name)

        if units_duration:
            procedures.append(
                RequestedProcedure(
                    code = code,
                    description = description,
                    units_duration = units_duration
                )
            )

    other_description = extractor.get_field("Other BHT procedure")
    other_code  = extractor.get_field("Other HCPCS Code")
    other_units_duration = extractor.get_field("Units and Duration for Other")

    if other_description or other_code or other_units_duration:
        procedures.append(
            RequestedProcedure(
                code = other_code,
                description = other_description,
                units_duration = other_units_duration
            )
        )


    authorization_form = AuthorizationForm(
        member = member,
        provider = provider,
        procedures = procedures
    )

    return authorization_form


        


