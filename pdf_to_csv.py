import pdfplumber
import csv
import re
from pathlib import Path

def extract_transactions(pdf_path, csv_path):
    transactions = []
    previous_balance = None

    # Pattern with type 
    pattern_with_type = re.compile(
        r"^(\d{1,2}\s+[A-Za-z]{3})\s+([A-Z]{2,4})\s+(.+?)\s+(\d{1,3}(?:,\d{3})*\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})$"
    )
    # Pattern without type 
    pattern_no_type = re.compile(
        r"^(\d{1,2}\s+[A-Za-z]{3})\s+(.+?)\s+(\d{1,3}(?:,\d{3})*\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})$"
    )

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split('\n'):
                line = line.strip()

                # Skip irrelevant or header lines
                if (
                    not line
                    or line.startswith(("Date", "Balance", "Totals", "Statement"))
                    or "Opening balance" in line
                    or "Orig date" in line
                    or "Page" in line
                ):
                    continue

                match = pattern_with_type.match(line)
                if match:
                    date, type_, desc, amount_str, balance_str = match.groups()
                else:
                    match = pattern_no_type.match(line)
                    if not match:
                        continue
                    date, desc, amount_str, balance_str = match.groups()
                    type_ = ""

                # convert numeric values
                amount = float(amount_str.replace(",", ""))
                balance = float(balance_str.replace(",", ""))

                # Determine sign based on previous balance
                if previous_balance is not None:
                    amount = -abs(amount) if balance < previous_balance else abs(amount)
                else:
                    amount = abs(amount)

                # amount as currency with two decimals
                amount_formatted = f"${amount:,.2f}"

                transactions.append([date, type_, desc.strip(), amount_formatted])
                previous_balance = balance

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Type", "Description", "Amount"])
        writer.writerows(transactions)

    print(f"✅ CSV created successfully: {csv_path}")
    print(f"📊 {len(transactions)} transactions extracted.")


if __name__ == "__main__":
    pdf_input = Path("statement.pdf")
    csv_output = Path("statement.csv")
    extract_transactions(pdf_input, csv_output)
