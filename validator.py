from models import AuthorizationForm
from datetime import datetime

def validate_authorization_form(form: AuthorizationForm):
    errors = []

    # Member Validation

    if not form.member.first_name:
        errors.append("Member first name is missing")

    if not form.member.last_name:
        errors.append("Member last name is missing")

    if not form.member.cin:
        errors.append("Member CIN is missing")
    elif not form.member.cin.isalnum():
        errors.append("Member CIN must contain only letters and numbers")

    if form.member.age is None:
        errors.append("Member age is missing")
    elif form.member.age < 0 or form.member.age > 120:
        errors.append("Member age must be between 0 and 120")

    if not form.member.dob:
        errors.append("Member DOB is missing")
    else:
        try:
            datetime.strptime(form.member.dob, "%m/%d/%Y")
        except ValueError:
            errors.append("Member DOB must be a valid date in MM/DD/YYYY format")



    # Provider Validation

    if not form.provider.aba_provider:
        errors.append("ABA provider is missing")

    if not form.provider.npi:
        errors.append("Provider NPI is missing")
    elif not form.provider.npi.isdigit():
        errors.append("Provider NPI must contain only numbers")
    elif len(form.provider.npi) != 10:
        errors.append("Provider NPI must be 10 digits")

    # Procedure validation

    if not form.procedures:
        errors.append("No requested procedures were found")

    for procedure in form.procedures:
        if not procedure.code:
            errors.append("Procedure HCPCS code is missing")
        if not procedure.units_duration:
            errors.append(
                f"Units and duration are missing for procedure {procedure.code}"
            )

    return errors