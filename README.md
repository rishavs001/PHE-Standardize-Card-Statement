# Credit Card Statement Standardization

## Overview
This project provides a Python script to standardize credit card statements from different banks into a unified format. The script processes CSV files, normalizes date formats, converts amounts to numerical values, and extracts relevant details such as currency and transaction location.

## Features
- Converts various date formats (DD-MM-YYYY, MM-DD-YYYY, DD-MM-YY) to a standard format (DD-MM-YYYY).
- Parses transaction amounts and distinguishes between debits and credits.
- Extracts currency codes for international transactions.
- Identifies transaction locations from descriptions.
- Automatically detects the correct column structure of input files.
- Sorts transactions chronologically.
- Outputs standardized CSV files with a consistent format.

## Assumptions
- The input CSV files may have varying column structures, but they will contain essential fields such as Date, Transaction Description, and Amount.
- Dates may be in different formats, but the script assumes they follow a recognizable pattern (DD-MM-YYYY, MM-DD-YYYY, or DD-MM-YY).
- Amounts may contain commas or currency indicators, which will be cleaned and converted to numerical values.
- Transactions marked with 'cr', 'Cr', or 'CR' are assumed to be credits, while others are debits.
- The last word in the transaction description is assumed to be the location for domestic transactions, while the second-to-last word is assumed to be the location for international transactions.
- The cardholder's name may appear as a standalone row in the CSV file, which will be detected and assigned accordingly.

## Installation
### Prerequisites
- Python 3.x

## Usage
1. Place the input CSV file in the project directory.
2. Run the script:
        index.py

3. Enter the input file name when prompted (e.g., `HDFC-Input-Case1.csv`).
4. The standardized output file will be generated with the corresponding name (e.g., `HDFC-Output-Case1.csv`).

## Input File Naming Convention
- Input files should follow the pattern: `BankName-Input-CaseX.csv` (e.g., `HDFC-Input-Case1.csv`).
- The script generates output files with the format: `BankName-Output-CaseX.csv`.

## Standardized Output Format
| Date       | Transaction Description | Debit | Credit | Currency | CardName | Transaction | Location |
|------------|-------------------------|-------|--------|----------|----------|-------------|----------|
| 12-01-2024 | Amazon Purchase         | 500   | 0      | INR      | HDFC     | Domestic    | amazon   |
| 15-02-2024 | PayPal Transfer         | 0     | 200    | USD      | ICICI    | International | paypal  |

## Error Handling
- Skips empty or malformed rows.
- Detects incorrect date formats and logs errors.
- Handles encoding issues and suggests re-saving CSV files in UTF-8 format.

## Contributing
Feel free to contribute by submitting issues or pull requests.


