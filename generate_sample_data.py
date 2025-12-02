# generate_sample_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
n_customers = 500
customer_ids = [f"C{1000+i}" for i in range(n_customers)]

records = []
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 11, 30)

for cid in customer_ids:
    # each customer has between 1 and 30 invoices
    invoices = np.random.poisson(3) + 1
    for _ in range(invoices):
        inv_date = start_date + (end_date - start_date) * np.random.random()
        qty = np.random.randint(1, 6)
        unit_price = round(np.random.uniform(5, 500), 2)
        total_price = round(qty * unit_price, 2)
        invoice_no = f"INV{random.randint(10000,99999)}"
        records.append({
            "CustomerID": cid,
            "InvoiceNo": invoice_no,
            "InvoiceDate": inv_date.strftime("%Y-%m-%d"),
            "Quantity": qty,
            "UnitPrice": unit_price,
            "TotalPrice": total_price,
            "Country": random.choice(["India","USA","UK","Germany","France"])
        })

df = pd.DataFrame(records)
df.to_csv("ecommerce_data.csv", index=False)
print("Saved ecommerce_data.csv with", len(df), "rows")
