from dataclasses import dataclass
from typing import Optional

@dataclass
class Member:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    sex: Optional[str] = None
    age: Optional[int] = None
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
    signature_path: Optional[str] = None