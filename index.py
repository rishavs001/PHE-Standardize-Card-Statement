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
    return None  # Return None for unrecognized date formats

def parse_amount(amount_str):
    """Convert amount strings to float after removing commas and handling 'cr' suffix."""
    if not amount_str or amount_str.strip() == '':
        return 0.0, False  # Default to debit
    amount_str = amount_str.replace(',', '').strip()
    
    is_credit = amount_str.endswith(" cr") or amount_str.endswith("Cr") or amount_str.endswith("CR")
    amount = float(amount_str.replace(" cr", "").replace("Cr", "").replace("CR", "")) if is_credit else float(amount_str)

    return amount, is_credit  # Returns amount and whether it's credit

def extract_currency(description, transaction_type):
    """Extract currency code for international transactions."""
    # if transaction_type == "International":
    #     match = re.search(r'\b[A-Z]{3}\b', description)  # Look for a three-letter currency code
    #     return match.group() if match else "NA"  # Default to NA if no match
    # return "INR"  # Default for domestic transactions
    words = description.split()
    if words:
        return re.sub(r'[^a-zA-Z]', '', words[-1]) if transaction_type == "International" else "INR"
    # return "unknown"

def extract_location(description, transaction_type):
    """Extract location (assumed as the last word in the description)."""
    words = description.split()
    if words:
        return re.sub(r'[^a-zA-Z]', '', words[-1]).lower() if transaction_type == "Domestic" else re.sub(r'[^a-zA-Z]', '', words[-2]).lower()
    return "unknown"

def standardize_statement(inputFile, outputFile):
    """Processes a bank statement CSV file and outputs a standardized format."""
    rows = []  # To store all processed rows for sorting
    with open(inputFile, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        writer = csv.writer(open(outputFile, 'w', newline='', encoding='utf-8'))
        writer.writerow(['Date', 'Transaction Description', 'Debit', 'Credit', 'Currency', 'CardName', 'Transaction', 'Location'])

        current_card_name = None
        transaction_type = "Domestic"
        date_col = desc_col = debit_col = credit_col = amount_col = None
        header_processed = False

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue  # Skip empty rows

            """ Detect Transaction Type (Check all cells in the row) """
            for cell in row:
                cell = cell.strip()
                if "Domestic" in cell:
                    transaction_type = "Domestic"
                    break
                elif "International" in cell:
                    transaction_type = "International"
                    break

            """ Detect Column Positions (First Non-Empty Row) """
            if not header_processed:
                for i, cell in enumerate(row):
                    if 'Date' in cell:
                        date_col = i
                    elif 'Transaction Description' in cell or 'Transaction Details' in cell:
                        desc_col = i
                    elif 'Debit' in cell:
                        debit_col = i
                    elif 'Credit' in cell:
                        credit_col = i
                    elif 'Amount' in cell:
                        amount_col = i
                if date_col is not None and desc_col is not None:
                    header_processed = True
                continue  # Skip header row

            """ Detect Cardholder Name (Row with one populated cell) """
            non_empty_cells = [cell.strip() for cell in row if cell.strip()]
            if len(non_empty_cells) == 1:  # If only one non-empty cell exists, it's likely a cardholder name
                current_card_name = non_empty_cells[0]
                continue  # Move to the next row after updating cardholder name

            """ Process Transaction Rows """
            if len(row) >= 3:
                date_str = row[date_col].strip()
                description = row[desc_col].strip()
                description_modified = " ".join(description.split()[:-1]) if transaction_type.lower() == "international" else description

                if not date_str or not description:
                    continue  # Skip rows with missing date or description

                parsed_date = parse_date(date_str)
                if not parsed_date:
                    continue  # Skip invalid dates

                """ Detect Format Type """
                if len(row) >= 3 and amount_col is not None:  # Format 1: Date, Description, Amount
                    amount, is_credit = parse_amount(row[amount_col].strip())
                    debit = 0 if is_credit else amount
                    credit = amount if is_credit else 0
                elif len(row) >= 4 and amount_col is None:  # Format 2: Date, Description, Debit, Credit
                    debit = parse_amount(row[debit_col].strip())[0] if row[debit_col].strip() else 0
                    credit = parse_amount(row[credit_col].strip())[0] if row[credit_col].strip() else 0
                else:
                    continue  # Skip malformed rows

                """ Extract Currency and Location """
                currency = extract_currency(description, transaction_type)
                location = extract_location(description, transaction_type)

                rows.append([parsed_date, description_modified, debit, credit, currency, current_card_name, transaction_type, location])
    
    """ Sort rows by Date (asc) and Transaction Description (desc) """
    # rows.sort(key=lambda x: (datetime.strptime(x[0], '%d-%m-%Y'), x[1].lower()), reverse=False)
    rows.sort(key=lambda x: (datetime.strptime(x[0], '%d-%m-%Y'), -ord(x[1][0].lower())), reverse=False)


    """ Write sorted rows to the output file """
    with open(outputFile, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Date', 'Transaction Description', 'Debit', 'Credit', 'Currency', 'CardName', 'Transaction', 'Location'])
        writer.writerows(rows)  # Write all sorted rows

    print(f"✅ Output file generated: {outputFile}")



if __name__ == "__main__":
    inputFile = input("Enter the input CSV file name (e.g., HDFC-Input-Case1.csv): ").strip()
    
    if not inputFile.endswith('.csv'):
        inputFile += '.csv'

    # *Generate Output File Name Dynamically*
    if "Input" in inputFile:
        outputFile = inputFile.replace("Input", "Output")
    else:
        outputFile = inputFile.replace(".csv", "-Output.csv")

    # *Check if the input file exists before proceeding*
    if not os.path.exists(inputFile):
        print(f"❌ Error: The file '{inputFile}' was not found. Please check the file name and try again.")
    else:
        try:
            standardize_statement(inputFile, outputFile)
            print(f"✅ Processing complete. The output file is saved as: {outputFile}")
        except UnicodeDecodeError:
            print(f"❌ Error: Encoding issue detected in '{inputFile}'. Try opening it in Excel and re-saving as UTF-8 CSV.")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")


    """ Input CSV File Example """
    # HDFC-Input-Case1.csv
    # ICICI-Input-Case2.csv
    # Axis-Input-Case3.csv
    # IDFC-Input-Case4.csv