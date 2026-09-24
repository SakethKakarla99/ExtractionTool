from pypdf import PdfReader
from datetime import datetime
import re

class PDFExtractor:
    def __init__(self,pdf_path):
        self.pdf_path = pdf_path
        self.reader = PdfReader(pdf_path)
        self.fields = self.reader.get_fields() or {}

    def _normalize_name(self,name):
        return " ".join(name.split())

    def get_raw_field(self, field_name):
        normalized_search = self._normalize_name(field_name)

        for name, field in self.fields.items():
            normalized_name = self._normalize_name(name)

            if normalized_name == normalized_search:
                return field.get("/V")

        return None

    def get_field(self,field_name):
        value = self.get_raw_field(field_name)

        if value is None or value == "":
            return None

        return str(value).strip()


    def get_all_fields(self):
        extracted_fields = {}

        for name, field in self.fields.items():
            value =  field.get("/V")

            if value is None or value == "":
                extracted_fields[name] = None
            else:
                extracted_fields[name] = str(value).strip()

        return extracted_fields

    def has_form_fields(self):
        return bool(self.fields)

    def get_text(self):
        text = ""

        for page in self.reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    def parse_pdf_date(self,pdf_date):
        if not pdf_date:
            return None

        match = re.match(
            r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})",
            pdf_date
        )

        if not match:
            return pdf_date

        year, month, day, hour, minute, second = map(
            int, match.groups()
        )

        date = datetime(
            year,
            month,
            day,
            hour,
            minute,
            second
        )
        return date.strftime("%m/%d/%Y %I:%M %p")
    
    def normalize_date(self, date_string):
        if not date_string:
            return None

        date_formats = [
            "%m/%d/%Y",
            "%m/%d/%y",
            "%m-%d-%Y",
            "%m-%d-%y"
        ]

        for date_format in date_formats:
            try:
                date = datetime.strptime(date_string.strip(), date_format)
                return date.strftime("%m/%d/%Y")
            except ValueError:
                continue

        return date_string
    def get_widget_info(self):
        widgets = []

        for page_number, page in enumerate(self.reader.pages):
            annotations = page.get("/Annots", [])

            for annotation in annotations:
                annotation_object = annotation.get_object()

                if annotation_object.get("/Subtype") == "/Widget":
                    widgets.append({
                        "page": page_number +1,
                        "field_name": annotation_object.get("/T"),
                        "field_type": annotation_object.get("/FT"),
                        "value": annotation_object.get("/V"),
                        "appearance_state": annotation_object.get("/AS"),
                        "rect": annotation_object.get("/Rect")
                    })
        return widgets
    def print_text_coordinates(self, page_number=1):
        page = self.reader.pages[page_number - 1]

        def visitor(text, cm, tm, font_dict, font_size):
            if text.strip():
                x = tm[4]
                y = tm[5]

                print(
                    f"Text: {text.strip()!r} | "
                    f"x={x:.2f}, y={y:.2f}"
                )

        page.extract_text(visitor_text=visitor)

    def extract_text_from_region(self,page_number, x1,y1,x2,y2):
        page = self.reader.pages[page_number -1]

        extracted_text = []

        def visitor(text,cm,tm,font_dict, font_size):
            if not text or not text.strip():
                return
            x = tm[4]
            y = tm[5]

            if x1 <= x <= x2 and y1 <= y <=y2:
                extracted_text.append(text.strip())
        page.extract_text(visitor_text = visitor)
        if not extracted_text:
            return None
        return " ".join(extracted_text)
    
    def find_text_position(self, search_text, page_number=None, after_y = None):
        pages = self.reader.pages

        if page_number is not None:
            pages = [self.reader.pages[page_number - 1]]

        for index, page in enumerate(pages):
            found_positions = []

            def visitor(text, cm, tm, font_dict, font_size):
                if not text:
                    return

                if search_text.lower() in text.strip().lower():
                    x = tm[4]
                    y = tm[5]

                    if after_y is not None and y >= after_y:
                        return

                    found_positions.append({
                        "page": page_number if page_number is not None else index + 1,
                        "x" : x,
                        "y" : y

                    })

            page.extract_text(visitor_text=visitor)

            if found_positions:
                if after_y is not None:
                    return max(found_positions, key = lambda item: item["y"])

                return found_positions[0]
        return None

    


