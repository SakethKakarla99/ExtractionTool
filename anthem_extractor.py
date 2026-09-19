from pdf_extractor import PDFExtractor
from models import AnthemMember, OrderingPhysician, AgencyInformation


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
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 85,
        y1 = 490,
        x2 = 350,
        y2 = 510
    )

def extract_diagnosis_date(extractor):
    diagonsis_date = extractor.extract_text_from_region(
        page_number = 1,
        x1 = 410,
        y1 = 490,
        x2 = 590,
        y2 = 510
    )
    return extractor.normalize_date(diagonsis_date)

def extract_diagnosed_by(extractor):
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 150,
        y1 = 470,
        x2 = 590,
        y2 = 490
    )


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
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 115,
        y1 = 430,
        x2 = 590,
        y2 = 450
    )

def extract_provider_tid(extractor):
    text = extractor.extract_text_from_region(
        page_number=1,
        x1=95,
        y1=410,
        x2=350,
        y2=430
    )

    if not text:
        return None

    return text.split()[0]

def extract_physician_phone(extractor):
    text = extractor.extract_text_from_region(
        page_number=1,
        x1=95,
        y1=410,
        x2=350,
        y2=430
    )

    if not text:
        return None

    parts = text.split()

    if len(parts) < 2:
        return None

    return parts[1]

def extract_physician_address(extractor):
    return extractor.extract_text_from_region(
        page_number = 1,
        x1 = 80,
        y1 = 390,
        x2 = 590,
        y2 = 410
    )

def extracting_ordering_physician(extractor):
    return OrderingPhysician(
        physician_name= extract_physician_name(extractor),
        provider_tid = extract_provider_tid(extractor),
        phone = extract_physician_phone(extractor),
        address = extract_physician_address(extractor)
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
