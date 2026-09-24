from pdf_extractor import PDFExtractor
from models import *
import cv2 
from checkbox_detector import is_checked
import re

def inspect_anthem_form(pdf_path):
    extractor = PDFExtractor(pdf_path)

    return extractor.get_all_fields()

def extract_gender(extractor):
    widgets = extractor.get_widget_info()
    gender_widgets = []

    for widget in widgets:
        rect = widget['rect']

        if(
            widget['page'] == 1
            and rect
            and 500 < float(rect[0]) < 600
            and 500 < float(rect[1]) < 550
        ):
            gender_widgets.append(widget)

    gender_widgets.sort(
        key = lambda widget: float(widget['rect'][0])
    )

    if len(gender_widgets) < 2:
        return None

    male_widget = gender_widgets[0]
    female_widget = gender_widgets[1]

    if male_widget["appearance_state"] != "/Off":
        return "Male"
    if female_widget["appearance_state"] != "/Off":
        return "Female"

    return None

def extract_diagnosis(extractor):
    position = extractor.find_text_position("Diagnosis")

    if not position:
        return None
    page = position["page"]
    x = position["x"]
    y = position["y"]

    diagnosis =  extractor.extract_text_from_region(
        page_number = page,
        x1 = x + 50,
        y1 = y - 10,
        x2 = x + 320,
        y2 = y + 10
    )

    if not diagnosis:
        return None
    return diagnosis.lstrip(": ").strip()

def extract_diagnosis_date(extractor):
    position = extractor.find_text_position("Dx Date")

    if not position:
        return None

    page = position["page"]
    x = position["x"]
    y = position["y"]

    diagnosis_date = extractor.extract_text_from_region(
        page_number=page,
        x1=x + 40,
        y1=y - 10,
        x2=x + 230,
        y2=y + 10
    )

    return extractor.normalize_date(diagnosis_date)

def extract_diagnosed_by(extractor):
    position = extractor.find_text_position("Diagnosed by Whom")

    if not position:
        return None

    page = position["page"]
    x = position["x"]
    y = position["y"]

    diagnosed_by = extractor.extract_text_from_region(
        page_number=page,
        x1=x + 100,
        y1=y - 10,
        x2=x + 500,
        y2=y + 10
    )

    if not diagnosed_by:
        return None

    return diagnosed_by.lstrip(": ").strip()


def extractor_anthem_member(pdf_path):
    extractor = PDFExtractor(pdf_path)

    

    member = AnthemMember(
        name = extractor.get_field("Text1"),
        dob = extractor.normalize_date(extractor.get_field("Text2")),
        member_id = extractor.get_field("Text3"),
        age = int(extractor.get_field("Text4").split()[0])
            if extractor.get_field("Text4")
            else None,
        gender = extract_gender(extractor),
        diagnosis = extract_diagnosis(extractor),
        diagnosis_date = extract_diagnosis_date(extractor),
        diagnosed_by = extract_diagnosed_by(extractor)
        
    )

    return member

def extract_physician_name(extractor):
    position = extractor.find_text_position("Physician Name")

    if not position:
        return None

    page = position["page"]
    x = position["x"]
    y = position["y"]

    physician_name = extractor.extract_text_from_region(
        page_number=page,
        x1=x + 75,
        y1=y - 10,
        x2=x + 500,
        y2=y + 10
    )

    if not physician_name:
        return None

    return physician_name.lstrip(": ").strip()

def extract_provider_tid(extractor):
    position = extractor.find_text_position("Provider TID")

    if not position:
        return None

    page = position["page"]
    x = position["x"]
    y = position["y"]

    provider_tid = extractor.extract_text_from_region(
        page_number=page,
        x1=x + 55,
        y1=y - 10,
        x2=x + 300,
        y2=y + 10
    )

    if not provider_tid:
        return None

    provider_tid = provider_tid.lstrip(": ").strip()

    return provider_tid.split()[0]

def extract_physician_phone(extractor):
    section = extractor.find_text_position("ORDERING PHYSICIAN")

    if not section:
        return None

    position = extractor.find_text_position(
        "Phone",
        page_number=section["page"],
        after_y=section["y"]
    )

    if not position:
        return None

    row_text = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=0,
        y1=position["y"] - 10,
        x2=600,
        y2=position["y"] + 10
    )

    if not row_text:
        return None

    phone_match = re.search(
        r"\d{3}-\d{3}-\d{4}",
        row_text
    )

    if not phone_match:
        return None

    return phone_match.group()

def extract_physician_address(extractor):
    section = extractor.find_text_position("ORDERING PHYSICIAN")

    if not section:
        return None, None, None, None

    position = extractor.find_text_position(
        "Address",
        page_number=section["page"],
        after_y=section["y"]
    )

    if not position:
        return None, None, None, None

    address = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=0,
        y1=position["y"] - 10,
        x2=600,
        y2=position["y"] + 10
    )

    if not address:
        return None, None, None, None

    address = address.strip()

    # Remove the "Address :" label from the extracted row
    address = re.sub(
        r"^Address\s*:\s*",
        "",
        address,
        flags=re.IGNORECASE
    )

    # Extract state and ZIP from the end of the address
    state_zip_match = re.search(
        r"\b([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$",
        address
    )

    if not state_zip_match:
        return address, None, None, None

    state = state_zip_match.group(1)
    zip_code = state_zip_match.group(2)

    # Everything before state/ZIP still contains street + city
    remaining_address = address[:state_zip_match.start()].strip()

    print("Remaining Address:", remaining_address)
    print("State:", state)
    print("ZIP:", zip_code)

    return remaining_address, None, state, zip_code

def extracting_ordering_physician(extractor):
    return OrderingPhysician(
        physician_name= extract_physician_name(extractor),
        provider_tid = extract_provider_tid(extractor),
        phone = extract_physician_phone(extractor),
        # address = extract_physician_address(extractor)
    )

def extract_agency_name(extractor):
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 105,
        y1 = 345,
        x2 = 590,
        y2 = 365
    )

def extract_agency_tid(extractor):
    text = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 55,
        y1 = 330,
        x2 = 200,
        y2 = 340
    )
    if not text:
        return None
    return text.split()[0]

def extract_agency_npi(extractor):
    text = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 50,
        y1 = 330,
        x2 = 200,
        y2 = 340
    )
    if not text:
        return None
    parts = text.split()

    if len(parts) <2:
        return None

    return parts[1]

def extract_agency_in_network(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return None

    yes_checked = is_checked(
        image,
        (1049, 903, 1069, 923),
        threshold = 0.10
    )

    no_checked = is_checked(
        image,
        (1125,904,1145,924),
        threshold = 0.10
    )

    if yes_checked and not no_checked:
        return "Yes"

    if no_checked and not yes_checked:
        return "No"

    return None

def extract_agency_phone(extractor):
    return extractor.get_field("Text6")

def extract_agency_fax(extractor):
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 385,
        y1 = 305,
        x2 = 590,
        y2 = 320
    )

def extract_agency_address(extractor):
    street = extractor.get_field("Text7")
    city = extractor.get_field("Text8")
    state = extractor.get_field("Text9")
    zip_code = extractor.get_field("Text10")

    address_parts = [
        part for part in [street, city, state, zip_code]
        if part
    ]

    return ", ".join(address_parts)

def extract_agency_contact_person_phone(extractor):
    return extractor.get_field("Text11")

def extract_agency_information(extractor, image_path):
    return AgencyInformation(
        agency_name= extract_agency_name(extractor),
        tid = extract_agency_tid(extractor),
        npi = extract_agency_npi(extractor),
        in_network = extract_agency_in_network(image_path),
        phone = extract_agency_phone(extractor),
        fax = extract_agency_fax(extractor),
        address = extract_agency_address(extractor),
        contact_person_phone= extract_agency_contact_person_phone(extractor)

    )

def extract_bcba_provider_name(extractor):
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 110,
        y1 = 220,
        x2 = 590,
        y2 = 240
    )

def extract_bcba_tid(extractor):
    text = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 50,
        y1 = 200,
        x2 = 350,
        y2 = 215
    )
    if not text:
        return None

    parts = text.split()
    numbers = [part for part in parts if part.isdigit()]

    if not numbers:
        return None
    return numbers[0]

def extract_bcba_npi(extractor):
    text = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 50,
        y1 = 200,
        x2 = 350,
        y2 = 215
    )
    if not text:
        return None

    parts = text.split()
    numbers = [part for part in parts if part.isdigit()]

    if len(numbers) < 2:
        return None
    return numbers[1]

def extract_bcba_in_network(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return None

    yes_checked = is_checked(
        image,
        (1048,1153,1068,1173),
        threshold = 0.10
    )

    no_checked = is_checked(
        image,
        (1125,1153,1145,1173),
        threshold = 0.10
    )

    if yes_checked and not no_checked:
        return "Yes"

    if no_checked and not yes_checked:
        return "No"

    return None

def extract_bcba_phone(extractor):
    text = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 65,
        y1 = 180,
        x2 = 590,
        y2 = 195

    )
    if not text:
        return None

    phone_numbers = re.findall(
        r"\d{3}-\d{3}-\d{4}",
        text
    )
    if not phone_numbers:
        return None
    return phone_numbers[0]

def extract_bcba_fax(extractor):
    text = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 65,
        y1 = 180,
        x2 = 590,
        y2 = 195
    )
    if not text:
        return None

    phone_numbers = re.findall(
        r"\d{3}-\d{3}-\d{4}",
        text
    )
    if len(phone_numbers) < 2:
        return None
    return phone_numbers[1]

def extract_bcba_email(extractor):
    text = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 65,
        y1 = 180,
        x2 = 590,
        y2 = 195
    )
    if not text:
        return "N/A"

    email_match = re.search(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        text
    )

    if not email_match:
        return "N/A"

    return email_match.group()
def extract_bcba_address(extractor):
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 80,
        y1 = 155,
        x2 = 590,
        y2 = 175

    )

def extract_bcba_information(extractor, image_path):
    return BCBAInformation(
        provider_name = extract_bcba_provider_name(extractor),
        tid = extract_bcba_tid(extractor),
        npi = extract_bcba_npi(extractor),
        in_network = extract_agency_in_network(image_path),
        phone = extract_bcba_phone(extractor),
        fax = extract_bcba_fax(extractor),
        email = extract_bcba_email(extractor),
        address = extract_bcba_address(extractor)
    )
def extract_age_first_aba_treatment(extractor):
    value = extractor.get_field("Text5")

    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        return value

def extract_start_date_current_request(extractor):
    value = extractor.get_field("Text18")

    if not value:
        return None

    return extractor.normalize_date(value)

TREATMENT_ROWS = [
    {
        "y1": 525,
        "y2": 545,
        "units_field": "Text12",
        "timeframe_field": None
    },
    {
        "y1": 502,
        "y2": 522,
        "units_field": "Text13",
        "timeframe_field": None
    },
    {
        "y1": 479,
        "y2": 499,
        "units_field": None,
        "timeframe_field": None
    },
    {
        "y1": 456,
        "y2": 476,
        "units_field": "Text14",
        "timeframe_field": "Text19"
    },
    {
        "y1": 433,
        "y2": 453,
        "units_field": None,
        "timeframe_field": None
    },
    {
        "y1": 410,
        "y2": 430,
        "units_field": "Text15",
        "timeframe_field": "Text20"
    },
    {
        "y1": 387,
        "y2": 407,
        "units_field": "Text16",
        "timeframe_field": "Text21"
    },
    {
        "y1": 364,
        "y2": 384,
        "units_field": None,
        "timeframe_field": None
    },
    {
        "y1": 341,
        "y2": 361,
        "units_field": None,
        "timeframe_field": None
    },
    {
        "y1": 318,
        "y2": 338,
        "units_field": None,
        "timeframe_field": None
    }
]

def extract_treatment_row(
    extractor,
    y1,
    y2,
    units_field=None,
    timeframe_field=None
):
    description = extractor.extract_text_from_region(
        page_number=2,
        x1=30,
        y1=y1,
        x2=435,
        y2=y2
    )

    cpt_code = extractor.extract_text_from_region(
        page_number=2,
        x1=475,
        y1=y1,
        x2=510,
        y2=y2
    )

    units = extractor.get_field(units_field) if units_field else None

    if timeframe_field:
        timeframe = extractor.get_field(timeframe_field)
    else:
        timeframe = extractor.extract_text_from_region(
            page_number=2,
            x1=510,
            y1=y1,
            x2=590,
            y2=y2
        )

    return AnthemTreatment(
        description=description or "",
        units=units or "",
        cpt_code=cpt_code or "",
        timeframe=timeframe or ""
    )
def extract_treatments(extractor):
    treatments = []

    for row in TREATMENT_ROWS:
        treatment = extract_treatment_row(
            extractor,
            y1=row["y1"],
            y2=row["y2"],
            units_field=row["units_field"],
            timeframe_field=row["timeframe_field"]
        )

        treatments.append(treatment)

    return treatments

def extract_anthem_provider_info(extractor):
    text = extractor.extract_text_from_region(
        page_number=2,
        x1=110,
        y1=280,
        x2=400,
        y2=300
    )

    if not text:
        return "", ""

    credential_pattern = re.compile(
        r"\b(?:Ph\.?D\.?|Psy\.?D\.?|M\.?A\.?|M\.?S\.?|BCBA-D|BCBA|LMFT|LCSW)\b",
        re.IGNORECASE
    )

    match = credential_pattern.search(text)

    if not match:
        return text.strip(), ""

    provider_name = text[:match.start()].strip()
    license_information = text[match.start():].strip()

    return provider_name, license_information



