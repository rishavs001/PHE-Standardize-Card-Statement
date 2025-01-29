import csv
import re
from datetime import datetime
import os

def parse_date(date_str):
    """Convert various date formats to standardized format (DD-MM-YYYY)."""
    for fmt in ('%d-%m-%Y', '%m-%d-%Y', '%d-%m-%y'):
        try:
            return datetime.strptime(date_str, fmt).strftime('%d-%m-%Y')
        except ValueError:
            continue
    return None  

def parse_amount(amount_str):
    """Convert amount strings to float after removing commas and handling 'cr' suffix."""
    if not amount_str or amount_str.strip() == '':
        return 0.0, False  # Default to debit
    amount_str = amount_str.replace(',', '').strip()
    
    is_credit = amount_str.lower().endswith(" cr")
    amount_str_clean = re.sub(r'\s*cr$', '', amount_str, flags=re.IGNORECASE)
    amount = float(amount_str_clean)

    return amount, is_credit  

def extract_currency(description, transaction_type):
    """Extract currency code for international transactions."""
    if transaction_type == "International":
        words = description.split()
        if words:
            last_word = words[-1].upper()
            if len(last_word) == 3 and last_word.isalpha():
                return last_word
            match = re.search(r'([A-Z]{3})$', description.upper())
            if match:
                return match.group()
        return "NA"  # Default to NA if not found
    return "INR"  # Default for domestic transactions

def extract_location(description, transaction_type):
    """Extract location (penultimate word for international, last word for domestic)."""
    words = description.split()
    if transaction_type == "International":
        if len(words) >= 2:
            return re.sub(r'[^a-zA-Z]', '', words[-2]).lower()
        elif words:
            return re.sub(r'[^a-zA-Z]', '', words[-1]).lower()
    else:
        if words:
            return re.sub(r'[^a-zA-Z]', '', words[-1]).lower()
    return "unknown"

def standardize_statement(inputFile, outputFile):
    """Processes a bank statement CSV file and outputs a standardized format."""
    rows = []  
    with open(inputFile, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        current_card_name = None
        transaction_type = "Domestic"
        date_col = desc_col = debit_col = credit_col = amount_col = None
        header_processed = False

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue  

            # Detect Transaction Type
            for cell in row:
                cell_lower = cell.strip().lower()
                if 'domestic' in cell_lower:
                    transaction_type = "Domestic"
                    break
                elif 'international' in cell_lower:
                    transaction_type = "International"
                    break

            # Detect Column Positions
            if not header_processed:
                for i, cell in enumerate(row):
                    cell_lower = cell.strip().lower()
                    if 'date' in cell_lower:
                        date_col = i
                    elif 'transaction description' in cell_lower or 'transaction details' in cell_lower:
                        desc_col = i
                    elif 'debit' in cell_lower:
                        debit_col = i
                    elif 'credit' in cell_lower:
                        credit_col = i
                    elif 'amount' in cell_lower:
                        amount_col = i
                if date_col is not None and desc_col is not None:
                    header_processed = True
                continue  

            # Detect Cardholder Name
            non_empty_cells = [cell.strip() for cell in row if cell.strip()]
            if len(non_empty_cells) == 1:
                current_card_name = non_empty_cells[0]
                continue

            # Process Transaction Rows
            if len(row) >= max(filter(None, [date_col, desc_col, amount_col, debit_col, credit_col])) + 1:
                date_str = row[date_col].strip() if date_col < len(row) else ''
                description = row[desc_col].strip() if desc_col < len(row) else ''

                if not date_str or not description:
                    continue  

                parsed_date = parse_date(date_str)
                if not parsed_date:
                    continue  

                # Handle Amount/Debit/Credit
                debit = 0.0
                credit = 0.0
                if amount_col is not None and amount_col < len(row):
                    amount_str = row[amount_col].strip()
                    amount, is_credit = parse_amount(amount_str)
                    debit = 0.0 if is_credit else amount
                    credit = amount if is_credit else 0.0
                elif debit_col is not None and credit_col is not None:
                    debit_str = row[debit_col].strip() if debit_col < len(row) else ''
                    credit_str = row[credit_col].strip() if credit_col < len(row) else ''
                    debit = float(debit_str.replace(',', '')) if debit_str else 0.0
                    credit = float(credit_str.replace(',', '')) if credit_str else 0.0

                # Modify description for international transactions
                if transaction_type == "International":
                    words = description.split()
                    if words and (len(words[-1]) == 3 and words[-1].isalpha()):
                        description_modified = ' '.join(words[:-1])
                    else:
                        description_modified = description
                else:
                    description_modified = description

                # Extract currency and location
                currency = extract_currency(description, transaction_type)
                location = extract_location(description, transaction_type)

                rows.append([
                    parsed_date,
                    description_modified.strip(),
                    round(debit, 2),
                    round(credit, 2),
                    currency,
                    current_card_name,
                    transaction_type,
                    location
                ])
    
    # Sort rows by Date (asc) and Transaction Description (desc)
    rows.sort(key=lambda x: (
        datetime.strptime(x[0], '%d-%m-%Y'),
        tuple([-ord(c) for c in x[1].lower()])  
    ))

    # Write sorted rows to the output file
    with open(outputFile, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Date', 'Transaction Description', 'Debit', 'Credit', 'Currency', 'CardName', 'Transaction', 'Location'])
        for row in rows:
            writer.writerow(row)

    print(f"✅ Output file generated: {outputFile}")

if __name__ == "__main__":
    inputFile = input("Enter the input CSV file name (e.g., HDFC-Input-Case1.csv): ").strip()
    
    if not inputFile.endswith('.csv'):
        inputFile += '.csv'

    # Generate Output File Name Dynamically
    if "Input" in inputFile:
        outputFile = inputFile.replace("Input", "Output")
    else:
        outputFile = inputFile.replace(".csv", "-Output.csv")

    # Check if the input file exists before proceeding
    if not os.path.exists(inputFile):
        print(f" Error: The file '{inputFile}' was not found. Please check the file name and try again.")
    else:
        try:
            standardize_statement(inputFile, outputFile)
            print(f" Processing complete. The output file is saved as: {outputFile}")
        except UnicodeDecodeError:
            print(f" Error: Encoding issue detected in '{inputFile}'. Try opening it in Excel and re-saving as UTF-8 CSV.")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")

""" Input CSV File Example """
    # HDFC-Input-Case1.csv
    # ICICI-Input-Case2.csv
    # Axis-Input-Case3.csv
    # IDFC-Input-Case4.csv