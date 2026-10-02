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

    # Remove the "Address :" label
    address = re.sub(
        r"^Address\s*:\s*",
        "",
        address,
        flags=re.IGNORECASE
    )

    # Extract state and ZIP from the end
    state_zip_match = re.search(
        r"\b([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$",
        address
    )

    if not state_zip_match:
        return address, None, None, None

    state = state_zip_match.group(1)
    zip_code = state_zip_match.group(2)

    # Remove state and ZIP
    remaining_address = address[:state_zip_match.start()].strip()

    # Separate street and city
    street, city = split_street_city(remaining_address)

    return street, city, state, zip_code

def extracting_ordering_physician(extractor):
    street, city, state, zip_code = extract_physician_address(extractor)
    return OrderingPhysician(
        physician_name= extract_physician_name(extractor),
        provider_tid = extract_provider_tid(extractor),
        phone = extract_physician_phone(extractor),
        street = street,
        city = city,
        state = state,
        zip_code = zip_code
    )

def extract_agency_name(extractor):
    section = extractor.find_text_position("AGENCY INFORMATION")

    if not section:
        return None

    position = extractor.find_text_position(
        "Agency Name",
        page_number=section["page"],
        after_y=section["y"]
    )

    if not position:
        return None

    agency_name = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=position["x"] + 65,
        y1=position["y"] - 10,
        x2=position["x"] + 500,
        y2=position["y"] + 10
    )

    if not agency_name:
        return None

    return agency_name.lstrip(": ").strip()

def extract_agency_tid(extractor):
    section = extractor.find_text_position("AGENCY INFORMATION")

    if not section:
        return None

    position = extractor.find_text_position(
        "TID",
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

    tid_match = re.search(r"\b\d{9}\b", row_text)

    if not tid_match:
        return None

    return tid_match.group()

def extract_agency_npi(extractor):
    section = extractor.find_text_position("AGENCY INFORMATION")

    if not section:
        return None

    position = extractor.find_text_position(
        "NPI",
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

    numbers = re.findall(r"\d+", row_text)

    for number in numbers:
        if len(number) == 10:
            return number

    return None

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
    section = extractor.find_text_position("AGENCY INFORMATION")

    if not section:
        return None

    position = extractor.find_text_position(
        "Fax",
        page_number=section["page"],
        after_y=section["y"]
    )

    if not position:
        return None

    row_text = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=position["x"],
        y1=position["y"] - 10,
        x2=600,
        y2=position["y"] + 10
    )

    if not row_text:
        return None

    fax_match = re.search(
        r"\d{3}[-.\s]\d{3}[-.\s]\d{4}",
        row_text
    )

    if not fax_match:
        return None

    return fax_match.group()

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
        contact_person_phone = extract_agency_contact_person_phone(extractor)

    )

def extract_bcba_provider_name(extractor):
    section = extractor.find_text_position(
        "BCBA OR RENDERING PROVIDER INFORMATION"
    )

    if not section:
        return None

    position = extractor.find_text_position(
        "Provider Name",
        page_number=section["page"],
        after_y=section["y"]
    )

    if not position:
        return None

    provider_name = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=position["x"] + 75,
        y1=position["y"] - 10,
        x2=position["x"] + 500,
        y2=position["y"] + 10
    )

    if not provider_name:
        return None

    return provider_name.lstrip(": ").strip()

def extract_bcba_tid(extractor):
    section = extractor.find_text_position(
        "BCBA OR RENDERING PROVIDER INFORMATION"
    )

    if not section:
        return None

    position = extractor.find_text_position(
        "TID",
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

    numbers = re.findall(r"\d+", row_text)

    for number in numbers:
        if len(number) == 9:
            return number

    return None



def extract_bcba_npi(extractor):
    section = extractor.find_text_position(
        "BCBA OR RENDERING PROVIDER INFORMATION"
    )

    if not section:
        return None

    position = extractor.find_text_position(
        "NPI",
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

    numbers = re.findall(r"\d+", row_text)

    for number in numbers:
        if len(number) == 10:
            return number

    return None

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
    section = extractor.find_text_position(
        "BCBA OR RENDERING PROVIDER INFORMATION"
    )

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

    phone_numbers = re.findall(
        r"\d{3}-\d{3}-\d{4}",
        row_text
    )

    if not phone_numbers:
        return None

    return phone_numbers[0]

def extract_bcba_fax(extractor):
    section = extractor.find_text_position(
        "BCBA OR RENDERING PROVIDER INFORMATION"
    )

    if not section:
        return None

    position = extractor.find_text_position(
        "Fax",
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

    phone_numbers = re.findall(
        r"\d{3}-\d{3}-\d{4}",
        row_text
    )

    if len(phone_numbers) < 2:
        return None

    return phone_numbers[1]

def extract_bcba_email(extractor):
    section = extractor.find_text_position(
        "BCBA OR RENDERING PROVIDER INFORMATION"
    )

    if not section:
        return "N/A"

    position = extractor.find_text_position(
        "Email",
        page_number=section["page"],
        after_y=section["y"]
    )

    if not position:
        return "N/A"

    row_text = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=0,
        y1=position["y"] - 10,
        x2=600,
        y2=position["y"] + 10
    )

    if not row_text:
        return "N/A"

    email_match = re.search(
        r"[\w.-]+@[\w.-]+\.\w+",
        row_text
    )

    if not email_match:
        return "N/A"

    return email_match.group()

def extract_bcba_address(extractor):
    section = extractor.find_text_position(
        "BCBA OR RENDERING PROVIDER INFORMATION"
    )

    if not section:
        return None

    position = extractor.find_text_position(
        "Address",
        page_number=section["page"],
        after_y=section["y"]
    )

    if not position:
        return None

    address = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=0,
        y1=position["y"] - 10,
        x2=600,
        y2=position["y"] + 10
    )

    if not address:
        return None

    address = re.sub(
        r"^Address\s*:\s*",
        "",
        address,
        flags=re.IGNORECASE
    )

    return address.strip()

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



def extract_treatments(extractor):
    treatments = []

    # Find the table headings dynamically
    description_heading = extractor.find_text_position(
        "Adaptive Behavior Treatment",
        page_number=2
    )

    units_heading = extractor.find_text_position(
        "Units",
        page_number=2
    )

    cpt_heading = extractor.find_text_position(
        "CPT",
        page_number=2
    )

    timeframe_heading = extractor.find_text_position(
        "Timeframe",
        page_number=2
    )

    # Make sure all required headings were found
    if not all([
        description_heading,
        units_heading,
        cpt_heading,
        timeframe_heading
    ]):
        return treatments

    # Find treatment descriptions dynamically.
    # Each description gives us the Y position of its row.
    treatment_rows = extractor.get_text_items_from_region(
        page_number=2,
        x1=description_heading["x"],
        y1=300,
        x2=units_heading["x"],
        y2=description_heading["y"] - 1
    )

    widgets = extractor.get_widget_info()

    # Find widgets located in the Units column
    unit_widgets = []

    for widget in widgets:
        rect = widget["rect"]

        if widget["page"] != 2 or not rect:
            continue

        x = float(rect[0])

        if 420 < x < 480:
            unit_widgets.append(widget)

    # Find widgets located in the Timeframe column
    timeframe_widgets = []

    for widget in widgets:
        rect = widget["rect"]

        if widget["page"] != 2 or not rect:
            continue

        x = float(rect[0])

        if 500 < x < 600:
            timeframe_widgets.append(widget)

    # Dynamic boundary between CPT and Timeframe columns
    cpt_end_x = (
        cpt_heading["x"] + timeframe_heading["x"]
    ) / 2

    # Build each treatment row
    for row in treatment_rows:
        description = row["text"]
        row_y = row["y"]

        # -------------------------
        # Units
        # -------------------------
        units = ""

        for widget in unit_widgets:
            rect = widget["rect"]

            widget_bottom = float(rect[1])
            widget_top = float(rect[3])

            if widget_bottom <= row_y <= widget_top:
                units = (widget["value"] or "").strip()
                break

        # -------------------------
        # CPT Code
        # -------------------------
        cpt_code = extractor.extract_text_from_region(
            page_number=2,
            x1=cpt_heading["x"] - 10,
            y1=row_y - 5,
            x2=cpt_end_x,
            y2=row_y + 5
        ) or ""

        cpt_code = cpt_code.strip()

        # -------------------------
        # Timeframe
        # -------------------------
        timeframe = ""

        # First check for a PDF widget
        for widget in timeframe_widgets:
            rect = widget["rect"]

            widget_bottom = float(rect[1])
            widget_top = float(rect[3])

            if widget_bottom <= row_y <= widget_top:
                timeframe = (widget["value"] or "").strip()
                break

        # If there is no widget value, check embedded text
        if not timeframe:
            timeframe_bottom = extractor.extract_text_from_region(
                page_number=2,
                x1=timeframe_heading["x"] - 15,
                y1=row_y - 6,
                x2=600,
                y2=row_y + 6
            ) or ""

            timeframe_top = extractor.extract_text_from_region(
                page_number=2,
                x1=timeframe_heading["x"] - 15,
                y1=row_y + 6,
                x2=600,
                y2=row_y + 16
            ) or ""

            timeframe = " ".join(
                part.strip()
                for part in [
                    timeframe_top,
                    timeframe_bottom
                ]
                if part.strip()
            )

        # -------------------------
        # Create treatment object
        # -------------------------
        treatment = AnthemTreatment(
            description=description,
            units=units,
            cpt_code=cpt_code,
            timeframe=timeframe
        )

        treatments.append(treatment)

    return treatments

def extract_anthem_provider_info(extractor):
    position = extractor.find_text_position(
        "Provider Name",
        page_number=2
    )

    if not position:
        return "", ""

    text = extractor.extract_text_from_region(
        page_number=position["page"],
        x1=position["x"],
        y1=position["y"] + 10,
        x2=400,
        y2=position["y"] + 30
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

def split_street_city(address):
    if not address:
        return None, None

    unit_pattern = re.search(
        r"\b(?:Ste\.?|Suite|Apt\.?|Apartment|Unit|#)\s*[A-Za-z0-9-]+",
        address,
        re.IGNORECASE
    )

    if unit_pattern:
        street_end = unit_pattern.end()

        street = address[:street_end].strip()
        city = address[street_end:].strip()

        return street, city

    return address, None

def extract_anthem_provider_date(extractor):
    date_position = extractor.find_text_position(
        "Date",
        page_number=2
    )

    if not date_position:
        return None

    widgets = extractor.get_widget_info()

    for widget in widgets:
        rect = widget["rect"]

        if widget["page"] != 2 or not rect:
            continue

        widget_x = float(rect[0])
        widget_bottom = float(rect[1])
        widget_top = float(rect[3])

        # Find the widget directly above the Date label
        if (
            widget_x >= date_position["x"] - 10
            and widget_bottom > date_position["y"]
            and widget_top < date_position["y"] + 50
        ):
            value = widget["value"]

            if value:
                return extractor.normalize_date(str(value).strip())

    return None


