import pdfplumber
import pandas as pd
import numpy as np
import re
import warnings

warnings.filterwarnings("ignore")

def parse(file_path, output="transaction.csv"):
    all_data = []
    date_pattern = r'^\d{2}-[A-Z]{3}'  # e.g. 01-APR

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # Skip empty or non-date lines
                if not re.match(date_pattern, line):
                    continue

                parts = line.split()
                try:
                    date = parts[0]
                    # Handle CR (credit) transactions
                    if parts[-1] == 'CR':
                        flag = 'CR'
                        amount_str = parts[-2]
                        description = " ".join(parts[2:-2])
                    else:
                        flag = 'DR'
                        amount_str = parts[-1]
                        description = " ".join(parts[2:-1])

                    # Clean and convert amount
                    amount = float(amount_str.replace(".", "").replace(",", "."))

                    if flag == "CR":
                        amount *= -1

                    all_data.append([date, description, amount, flag])
                except Exception:
                    continue  # Skip malformed lines

    # Build DataFrame
    df = pd.DataFrame(all_data, columns=['date', 'description', 'amount', 'flag'])

    # Filter out payment lines or noise
    df = df[df['description'].str.len() > 4]
    df = df[~df['description'].str.contains("PEMBAYARAN - MBCA", na=False)]

    df.to_csv(output, index=False)
    print(f"✅ Data extracted and saved to: {output}")
    return df

if __name__ == "__main__":
    file_path = input("Masukkan path ke PDF CC BCA anda:\n")
    parse(file_path)