# ExtractionTool

A Python-based document extraction tool designed to extract structured information from authorization forms.

## Current Features

The tool currently supports extraction from Behavioral Health Treatment Authorization Request PDF forms.

It extracts:

- Member information
  - First and last name
  - Sex
  - Age
  - Date of birth
  - CIN
  - ICD-10 diagnosis
  - Mailing address
  - Phone number

- Provider information
  - ABA provider
  - NPI
  - TIN
  - Medi-Cal ID
  - Address
  - Phone
  - Fax
  - Office contact

Extracted information is stored in Python `Member` and `Provider` objects.

## Technologies

- Python
- pypdf
- OpenCV

## Project Structure

- `authorization_extractor.py` - Extracts information from authorization PDF forms
- `models.py` - Contains the Member and Provider data models
- `checkbox_detector.py` - Utilities for detecting checked boxes
- `test.py` - Tests the authorization form extractor

## In Development

Future functionality will include:

- Provider signature extraction
- Requested procedure and HCPCS code extraction
- Support for additional authorization form formats
- Improved handling of scanned/non-fillable PDFs
