# ExtractionTool

A Python-based PDF extraction tool designed to extract structured information from healthcare authorization and treatment-plan PDF documents.

The project currently supports CalOptima Behavioral Health Treatment Authorization Request Forms (BHT-ARF) and is actively adding support for Anthem Treatment Plan Request Forms for Autism Spectrum Disorders.

The project uses a general PDF extraction layer that can be extended to support additional PDF document types.

## Current Features

### General PDF Extraction

- Read fillable PDF form fields
- Extract embedded PDF text
- Extract text from specific PDF coordinate regions
- Inspect PDF widget information and appearance states
- Normalize PDF field names
- Handle empty and missing fields
- Normalize multiple date formats
- Convert extracted data into structured Python dataclasses
- Support document-specific extractors built on a shared PDF extraction layer

### CalOptima BHT Authorization Forms

- Extract member information
- Extract provider information
- Detect and extract digital signature metadata
- Convert PDF signature dates into readable dates
- Extract requested procedures and HCPCS codes
- Extract units and duration for requested procedures
- Extract custom "Other" procedures
- Support integer and decimal member ages
- Convert extracted authorization forms into Python dictionaries and JSON
- Validate extracted authorization form data
- Automated validation testing with pytest

### Anthem ASD Treatment Plan Forms

Current Anthem extraction support includes:

#### Member Demographics

- Member name
- Date of birth
- Member ID
- Age
- Gender
- Diagnosis
- Diagnosis date
- Diagnosing provider

Gender is extracted using PDF radio-button widget appearance states.

Diagnosis information is extracted using coordinate-based PDF text extraction rather than hard-coded diagnosis values.

#### Ordering Physician

- Physician name
- Provider TID
- Phone number
- Address

#### Agency Information

Current extraction includes:

- Agency name
- TID
- NPI

Additional Anthem fields are currently being implemented.

## Architecture

The project separates general PDF functionality from document-specific extraction logic.

```text
PDF Document
     │
     ▼
PDFExtractor
     │
     ├── Form field extraction
     ├── Embedded text extraction
     ├── Coordinate-based text extraction
     ├── PDF widget inspection
     └── Date normalization
     │
     ▼
Document-Specific Extractor
     │
     ├── caloptima_extractor.py
     └── anthem_extractor.py
     │
     ▼
Structured Data Models
     │
     ▼
Validation
     │
     ▼
Dictionary / JSON
```

This architecture allows new document types to reuse the same low-level PDF functionality while keeping document-specific field mappings and extraction rules separate.

## Structured Data Models

### CalOptima

CalOptima authorization forms are organized into an `AuthorizationForm` model:

```text
AuthorizationForm
├── Member
├── Provider
└── RequestedProcedure[]
```

The model can be converted into a Python dictionary:

```python
authorization_form.to_dict()
```

### Anthem

Anthem extraction currently uses structured models including:

```text
AnthemMember

OrderingPhysician

AgencyInformation
```

These models allow extracted sections of the Anthem treatment-plan form to be represented as structured Python objects as development continues.

The structured format is intended to support future database and API integrations.

## Coordinate-Based Text Extraction

Some PDFs contain visible information that is not stored as standard fillable form fields.

For these cases, `PDFExtractor` supports extracting embedded text from a specified region of a PDF page.

This is currently used for Anthem fields such as:

- Diagnosis
- Diagnosis date
- Diagnosing provider
- Ordering physician information
- Agency information

The document-specific extractor defines where a field is located, while the generic `PDFExtractor` handles retrieving text from that region.

This keeps document-layout knowledge out of the general PDF extraction layer.

## PDF Widget Extraction

Some form controls cannot be reliably interpreted using only their high-level field value.

The extractor can inspect individual PDF widgets, including:

- Page number
- Field name
- Field type
- Field value
- Appearance state
- Widget coordinates

This is currently used to determine the selected gender radio button on Anthem forms.

## Date Normalization

The general PDF extraction layer normalizes several common date formats into:

```text
MM/DD/YYYY
```

Examples:

```text
10/15/16   → 10/15/2016
8/6/2021   → 08/06/2021
02/07/2005 → 02/07/2005
06-08-2018 → 06/08/2018
6-8-18     → 06/08/2018
```

This allows dates from different document formats to be represented consistently before validation or database storage.

## Validation

The project includes a validation layer in `validator.py`.

Current CalOptima validation includes:

- Required member first and last name
- Required member CIN
- CIN alphanumeric validation
- Member age range validation
- Member DOB validation
- Required ABA provider
- Provider NPI validation
- Required requested procedures
- Required HCPCS codes
- Required units and duration

Validation occurs after extraction so malformed or incomplete data can be detected before it is passed to another system.

## Automated Testing

Validation and general extraction utilities are tested using `pytest`.

Tests currently cover scenarios including:

- Valid authorization forms
- Invalid NPI length
- Non-numeric NPI values
- Invalid member age
- Invalid DOB
- Missing procedure units/duration
- Missing HCPCS codes
- Missing member CIN
- Missing provider NPI
- Missing requested procedures
- Two-digit year normalization
- Single-digit month and day normalization
- Four-digit year normalization

Run all automated tests with:

```bash
py -m pytest
```

## PDF Compatibility Testing

The extractor is tested against multiple versions of authorization and treatment-plan forms rather than relying on a single sample document.

Testing multiple PDFs has identified differences such as:

- Integer and decimal age values
- Different date formats
- Different procedure unit formats
- Different provider information
- Different digital signatures
- Alphanumeric CIN values
- Radio-button behavior
- Information stored as form fields versus embedded PDF text

This testing is used to identify assumptions in the extraction logic and make the extractor more robust across document variations.

## Future Development

Planned improvements include:

- Complete Anthem Agency Information extraction
- Extract Anthem BCBA/rendering provider information
- Extract Anthem assessment and treatment information
- Extract Anthem CPT codes, requested units, and treatment durations
- Add automated tests for Anthem extraction
- Test Anthem extraction across multiple form samples
- Visual/handwritten signature detection
- Support for additional PDF document types
- Automatic document-type detection and routing
- OCR support for scanned and flattened PDFs
- Improved visual checkbox detection
- More robust field validation
- Additional automated extraction tests
- Supabase database integration
- Database storage for extracted document data
- DOCX document support
