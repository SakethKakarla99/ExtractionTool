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
- Extract custom "Other" procedures
- Support integer and decimal member ages
- Convert extracted data into structured Python dataclasses
- Convert extracted authorization forms into Python dictionaries and JSON
- Validate extracted authorization form data
- Automated validation testing with pytest

## Structured Data Models

Extracted authorization forms are organized into a single `AuthorizationForm` model:

```text
AuthorizationForm
├── Member
├── Provider
└── RequestedProcedure[]
```

This allows an entire extracted document to be handled as one structured object instead of returning separate values.

The model can also be converted into a Python dictionary:

```python
authorization_form.to_dict()
```

This structured format is intended to support future database and API integrations.

## Validation

The project includes a validation layer in `validator.py`.

Current validation includes:

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

Validation rules are tested using `pytest`.

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

Run all automated tests with:

```bash
py -m pytest
```

## PDF Compatibility Testing

The extractor is being tested against multiple versions of real BHT authorization forms rather than relying on a single sample document.

Testing multiple PDFs has already identified differences such as:

- Integer and decimal age values
- Different date formats
- Different procedure unit formats
- Different provider information
- Different digital signatures
- Alphanumeric CIN values

This testing is used to identify assumptions in the extraction logic and make the extractor more robust across document variations.

## Date Normalization

A general date-normalization utility is being developed to standardize dates before validation or database storage.

The intended normalization includes:

```text
10/15/16   → 10/15/2016
8/6/2021   → 08/06/2021
02/07/2005 → 02/07/2005
```

Automated testing for date normalization is planned.

## Future Development

Planned improvements include:

- Complete and test date normalization
- Visual/handwritten signature detection
- Support for additional PDF document types
- Automatic document-type detection and routing
- OCR support for scanned and flattened PDFs
- Improved visual checkbox detection
- More robust field validation
- Additional automated extraction tests
- Supabase database integration
- Database-ready data mapping
- Support for storing extracted authorization records
