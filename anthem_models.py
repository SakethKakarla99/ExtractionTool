from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class AnthemMember:
    name: Optional[str] = None
    dob: Optional[str] = None
    member_id: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    diagnosis: Optional[str] = None
    diagnosis_date: Optional[str] = None
    diagnosed_by: Optional[str] = None


@dataclass
class OrderingPhysician:
    physician_name: Optional[str] = None
    provider_tid: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None


@dataclass
class AgencyInformation:
    agency_name: Optional[str] = None
    tid: Optional[str] = None
    npi: Optional[str] = None
    in_network: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    address: Optional[str] = None
    contact_person_phone: Optional[str] = None


@dataclass
class BCBAInformation:
    provider_name: Optional[str] = None
    tid: Optional[str] = None
    npi: Optional[str] = None
    in_network: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


@dataclass
class AnthemTreatment:
    description: str = ""
    units: str = ""
    cpt_code: str = ""
    timeframe: str = ""


@dataclass
class AnthemProviderSignature:
    provider_name: str = ""
    license_information: str = ""
    signature_present: bool = False
    signature_name: str = ""
    signature_date: str = ""

@dataclass
class AnthemAuthorizationForm:
    member: AnthemMember
    ordering_physician: OrderingPhysician
    agency: AgencyInformation
    bcba: BCBAInformation
    age_first_aba_treatment: Optional[int] = None
    start_date_current_request: Optional[str] = None
    treatments: list[AnthemTreatment] = None
    provider_name: Optional[str] = None
    license_information: Optional[str] = None
    provider_date: Optional[str] = None

    def to_dict(self):
        return asdict(self)