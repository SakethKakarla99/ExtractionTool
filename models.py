from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Member:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    sex: Optional[str] = None
    age: Optional[float] = None
    dob: Optional[str] = None
    cin: Optional[str] = None
    icd10_dx: Optional[str] = None
    mailing_address: Optional[str] = None
    phone: Optional[str] = None



@dataclass
class Provider:
    aba_provider: Optional[str] = None
    npi: Optional[str] = None
    tin: Optional[str] = None
    medi_cal_id: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    office_contact: Optional[str] = None
    signature_present: bool = False
    signature_name: Optional[str] = None
    signature_date: Optional[str] = None

@dataclass
class RequestedProcedure:
    code: Optional[str] = None
    description: Optional[str] = None
    units_duration: Optional[str] = None

@dataclass
class AuthorizationForm:
    member: Member
    provider: Provider
    procedures: list[RequestedProcedure]

    def to_dict(self):
        return asdict(self)
    

