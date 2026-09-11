from pathlib import Path
from collections import Counter
import re

from pypdf import PdfReader
from docx import Document


def extract_text(file_path):
    path = Path(file_path)


