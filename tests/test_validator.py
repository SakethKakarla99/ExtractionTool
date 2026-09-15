from authorization_extractor import extract_authorization_form
from validator import validate_authorization_form

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