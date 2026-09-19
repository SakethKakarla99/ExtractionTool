from pdf_extractor import PDFExtractor
from models import AnthemMember


def inspect_anthem_form(pdf_path):
    extractor = PDFExtractor(pdf_path)

    return extractor.get_all_fields()

def extractor_anthem_member(pdf_path):
    extractor = PDFExtractor(pdf_path)

    

    member = AnthemMember(
        name = extractor.get_field("Text1"),
        dob = extractor.normalize_date(extractor.get_field("Text2")),
        member_id = extractor.get_field("Text3"),
        age = int(extractor.get_field("Text4").split()[0])
            if extractor.get_field("Text4")
            else None,
        gender = extractor.get_field("Radio Button5")
        
    )

    return member

