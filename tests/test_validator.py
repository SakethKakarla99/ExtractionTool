from caloptima_extractor import extract_authorization_form
from validator import validate_authorization_form
from pdf_extractor import PDFExtractor

def test_valid_authorization_form():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    errors = validate_authorization_form(authorization_form)

    assert errors == []

def test_invalid_npi_length():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.provider.npi = "12345"

    errors = validate_authorization_form(authorization_form)

    assert "Provider NPI must be 10 digits" in errors

def test_invalid_npi_characters():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.provider.npi = "123ABC7890"

    errors = validate_authorization_form(authorization_form)

    assert "Provider NPI must contain only numbers" in errors

def test_invalid_age():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.member.age = 150

    errors = validate_authorization_form(authorization_form)

    assert "Member age must be between 0 and 120" in errors

def test_invalid_dob():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.member.dob = "02/31/2015"

    errors = validate_authorization_form(authorization_form)

    assert "Member DOB must be a valid date in MM/DD/YYYY format" in errors

def test_missing_procedure_units_duration():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.procedures[0].units_duration = None

    errors = validate_authorization_form(authorization_form)

    assert "Units and duration are missing for procedure H0032-HO" in errors

def test_missing_procedure_code():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.procedures[0].code = None

    errors = validate_authorization_form(authorization_form)

    assert "Procedure HCPCS code is missing" in errors

def test_missing_member_cin():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.member.cin = None

    errors = validate_authorization_form(authorization_form)

    assert "Member CIN is missing" in errors


def test_missing_provider_npi():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.provider.npi = None

    errors = validate_authorization_form(authorization_form)

    assert "Provider NPI is missing" in errors


def test_no_procedures():
    authorization_form = extract_authorization_form(
        "documents/authorization_form.pdf"
    )

    authorization_form.procedures = []

    errors = validate_authorization_form(authorization_form)

    assert "No requested procedures were found" in errors

def test_normalize_two_digit_year():
    extractor = PDFExtractor("documents/authorization_form.pdf")

    result = extractor.normalize_date("10/15/16")

    assert result == "10/15/2016"

def test_normalize_single_digit_month_and_day():
    extractor = PDFExtractor("documents/authorization_form.pdf")

    result = extractor.normalize_date("8/6/2021")

    assert result == "08/06/2021"

def test_normalize_four_digit_year():
    extractor = PDFExtractor("documents/authorization_form.pdf")

    result = extractor.normalize_date("02/07/2005")

    assert result == "02/07/2005"