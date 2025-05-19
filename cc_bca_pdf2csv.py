import pdfplumber
import pandas as pd
import re
import warnings

warnings.filterwarnings("ignore")

def parse(file_path, output="transaction.csv"):
    rows = []
    current_txn = None
    date_pattern = r'^\d{2}-[A-Z]{3}'  # e.g. 01-APR
    fx_pattern = r'^\(USD .* X .*?\)'  # foreign exchange line

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()

                # If line is a foreign exchange breakdown, merge to description
                if re.match(fx_pattern, line):
                    if current_txn:
                        current_txn["description"] += f" {line}"
                    continue

                # If line matches a transaction (starts with date)
                if re.match(date_pattern, line):
                    parts = line.split()

                    try:
                        date = parts[0]
                        if parts[-1] == 'CR':
                            flag = 'CR'
                            amount_str = parts[-2]
                            description = " ".join(parts[2:-2])
                        else:
                            flag = 'DR'
                            amount_str = parts[-1]
                            description = " ".join(parts[2:-1])

                        amount = float(amount_str.replace(".", "").replace(",", "."))

                        current_txn = {
                            "date": date,
                            "description": description,
                            "debit": amount if flag == "DR" else 0,
                            "credit": amount if flag == "CR" else 0
                        }
                        rows.append(current_txn)

                    except Exception:
                        continue  # Skip malformed lines

    df = pd.DataFrame(rows)

    # Filter out invalid descriptions
    df = df[df['description'].str.len() > 4]
    df = df[~df['description'].str.contains("PEMBAYARAN - MBCA", na=False)]

    df.to_csv(output, index=False)
    print(f"✅ Data saved to {output}")
    return df

if __name__ == "__main__":
    file_path = input("Masukkan path ke PDF CC BCA anda:\n")
    parse(file_path)