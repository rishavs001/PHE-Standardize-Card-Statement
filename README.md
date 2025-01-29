# Credit Card Statement Standardization

## Overview

This Python script standardizes credit card statements from various banks into a unified format. It handles different CSV formats, normalizes transaction data, and provides detailed transaction analysis including currency detection and location extraction. The script is particularly useful for financial data analysis and reconciliation purposes.

## Features

- Date Format Standardization

  - Converts multiple formats (DD-MM-YYYY, MM-DD-YYYY, DD-MM-YY) to DD-MM-YYYY
  - Validates date entries and skips invalid formats
  - Maintains chronological ordering in output

- Amount Processing

  - Handles both combined and split (debit/credit) amount columns
  - Automatically detects credit indicators ('cr', 'Cr', 'CR')
  - Removes commas and special characters from amounts
  - Rounds all amounts to 2 decimal places

- Transaction Classification

  - Distinguishes between domestic and international transactions
  - Extracts currency codes for international transactions (defaults to USD if not specified)
  - Identifies and preserves cardholder information
  - Extracts location data from transaction descriptions

- Smart Column Detection

  - Automatically identifies column structure in input files
  - Supports various CSV layouts from different banks
  - Handles missing or differently named columns

## Assumptions
- The input CSV files may have varying column structures, but they will contain essential fields such as Date, Transaction Description, and Amount.
- Dates may be in different formats, but the script assumes they follow a recognizable pattern (DD-MM-YYYY, MM-DD-YYYY, or DD-MM-YY).
- Amounts may contain commas or currency indicators, which will be cleaned and converted to numerical values.
- Transactions marked with 'cr', 'Cr', or 'CR' are assumed to be credits, while others are debits.
- The last word in the transaction description is assumed to be the location for domestic transactions, while the second-to-last word is assumed to be the location for international transactions.
- The cardholder's name may appear as a standalone row in the CSV file, which will be detected and assigned accordingly.

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses standard library only)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rishavs001/PHE-Standardize-Card-Statement.git
cd credit-card-standardizer
```

2. Verify Python installation:

```bash
python --version
```

## Usage

1. Place your input CSV file in the script directory
2. Run the script:

```bash
python index.py
```

3. When prompted, enter the input filename (e.g., `HDFC-Input-Case1.csv`)
4. The standardized output file will be generated automatically

### File Naming Conventions

- Input files: `BankName-Input-CaseX.csv` (e.g., `HDFC-Input-Case1.csv`)
- Output files: `BankName-Output-CaseX.csv` (e.g., `HDFC-Output-Case1.csv`)
- The script automatically handles files with or without the .csv extension

### Input File Requirements

The script accepts CSV files containing:

- Transaction dates in any standard format
- Transaction descriptions
- Amount information (either as single column or separate debit/credit columns)
- Optional cardholder information

### Output Format Specification

The standardized output CSV contains the following columns:

| Column Name             | Description           | Format                 |
| ----------------------- | --------------------- | ---------------------- |
| Date                    | Transaction date      | DD-MM-YYYY             |
| Transaction Description | Cleaned description   | Text                   |
| Debit                   | Debit amount          | Numeric (2 decimals)   |
| Credit                  | Credit amount         | Numeric (2 decimals)   |
| Currency                | Transaction currency  | 3-letter code          |
| CardName                | Cardholder identifier | Text                   |
| Transaction             | Transaction type      | Domestic/International |
| Location                | Extracted location    | Lowercase text         |

## Processing Logic

### Date Processing

- Attempts multiple format interpretations
- Validates date logic (valid month/day combinations)
- Skips rows with unparseable dates

### Amount Processing

- Removes all non-numeric characters except decimal points
- Identifies credits through suffix detection
- Splits amounts into appropriate debit/credit columns
- Maintains original precision up to 2 decimal places

### Location Extraction

- Domestic transactions: Uses last word from description
- International transactions: Uses penultimate word
- Cleans location text (removes special characters, converts to lowercase)

### Currency Detection

- Domestic: Defaults to INR
- International:
  - Extracts 3-letter currency code from description
  - Falls back to USD if no valid code found

## Error Handling

### Input Validation

- Verifies file existence and readability
- Checks for minimum required columns
- Validates data format in each column

### Runtime Error Management

- Handles encoding issues with helpful messages
- Skips malformed rows while continuing processing
- Provides detailed error messages for troubleshooting

### Common Error Solutions

- UTF-8 encoding issues: Suggests re-saving CSV in correct format
- Missing columns: Indicates required column names
- Invalid dates: Reports specific problematic entries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Inspired by the need for standardized financial data analysis
- Developed with input from financial analysts and data scientists

## Support

For issues and feature requests, please use the GitHub Issues tracker.
