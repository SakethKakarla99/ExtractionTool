# ExtractionTool

A Python-based PDF extraction tool designed to extract structured information from PDF documents.

The project currently supports a Behavioral Health Treatment Authorization Request Form (BHT-ARF), while using a general PDF extraction layer that can be extended to support additional PDF document types.

## Current Features

- Read fillable PDF form fields
- Extract embedded PDF text
- Normalize PDF field names
- Handle empty and missing fields
- Extract member information
- Extract provider information
- Detect and extract digital signature metadata
- Convert PDF signature dates into readable dates
- Extract requested procedures and HCPCS codes
- Extract units and duration for requested procedures
- Return extracted information as structured Python dataclasses

## Project Architecture

The project separates general PDF reading from document-specific extraction logic.

```text
PDF
 |
 v
PDFExtractor
 |
 |-- Form Fields
 |-- Embedded Text
 |-- Raw PDF Fields
 |-- PDF Date Parsing
 |
 v
Document-Specific Extractor
 |
 |-- Member
 |-- Provider
 |-- Requested Procedures
 |
 v
Structured Python Models
```

### `pdf_extractor.py`

Contains the general-purpose `PDFExtractor` class.

This layer is not specific to the Behavioral Health Authorization form. It provides reusable functionality for working with PDFs, including:

- Opening PDFs with `pypdf`
- Detecting whether a PDF contains form fields
- Retrieving individual form fields
- Retrieving raw PDF field values
- Normalizing field names
- Extracting all form fields
- Extracting embedded text from PDF pages
- Parsing PDF-formatted dates

### `authorization_extractor.py`

Contains the extraction logic specifically for Behavioral Health Treatment Authorization Request Forms.

It uses `PDFExtractor` to retrieve the underlying PDF data and then maps that information into structured models.

Currently extracts:

- Member information
- Provider information
- Provider digital signature information
- Requested procedures
- HCPCS codes
- Units and duration

### `models.py`

Contains Python dataclasses used to represent extracted information.

Current models include:

```text
Member
Provider
RequestedProcedure
```

### `checkbox_detector.py`

Contains OpenCV-based checkbox detection functionality.

This can be used as a visual fallback for documents where checkbox information cannot be retrieved directly from PDF form fields.

### `coordinate_finder.py`

Development utility for locating coordinates within rendered PDF pages or images.

### `test.py`

Used to test the extraction pipeline against sample PDF documents.

## Example Extracted Data

The authorization extractor can return structured objects such as:

```python
Member(
    first_name="Jhon",
    last_name="Doe",
    sex="Male",
    age=6,
    dob="01/21/2015",
    cin="12345678A",
    icd10_dx="F84.0"
)
```

Provider information can also include digital signature metadata:

```python
Provider(
    aba_provider="Example Provider",
    npi="1234567890",
    signature_present=True,
    signature_name="Example Name",
    signature_date="02/08/2023 12:40 PM"
)
```

Requested procedures are returned individually:

```python
RequestedProcedure(
    code="H0032-HO",
    description="Mental health service plan development by non-physician (BCBA)",
    units_duration="78/6 months"
)
```

Only procedures containing a requested units/duration value are currently added to the procedure list.

## PDF Extraction Strategy

PDF documents can store information in several different ways.

The project is being designed to support multiple extraction strategies:

```text
PDF
 |
 |-- Fillable Form
 |     -> AcroForm field extraction
 |
 |-- Text-Based PDF
 |     -> Embedded text extraction
 |
 |-- Scanned / Image PDF
       -> OCR / computer vision fallback
```

Currently, fillable PDF fields and embedded text extraction are supported.

OCR and broader scanned-document support are planned for future development.

## Technologies

- Python
- pypdf
- OpenCV
- Python dataclasses
- Regular expressions

## Installation

Clone the repository:

```bash
git clone https://github.com/SakethKakarla99/ExtractionTool.git
```

Move into the project directory:

```bash
cd ExtractionTool
```

Install the required packages:

```bash
pip install pypdf opencv-python
```

## Running the Project

Place a test PDF inside the `documents` directory.

Then run:

```bash
py test.py
```

The test script displays:

- Whether form fields were detected
- Embedded PDF text
- Extracted member information
- Extracted provider information
- Digital signature information
- Requested procedures

## Future Development

Planned improvements include:

- Support for additional PDF document types
- Automatic document-type detection and routing
- OCR support for scanned PDFs
- Improved visual checkbox detection
- Extraction of custom/"Other" procedures
- More robust PDF date and timezone handling
- Additional structured data models
- Validation of extracted information
- Exporting extracted data to formats such as JSON
- Automated testing across multiple PDF formats

The long-term goal is to create a reusable PDF extraction pipeline where general PDF-reading functionality is shared across multiple document-specific parsers.
