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

    

    


