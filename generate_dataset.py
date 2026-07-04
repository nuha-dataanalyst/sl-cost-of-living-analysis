import pandas as pd
import numpy as np
import os

np.random.seed(42)

years = list(range(2019, 2025))
months = list(range(1, 13))
regions = ['Colombo', 'Kandy', 'Galle', 'Jaffna']
categories = ['Food', 'Transport', 'Housing', 'Healthcare', 'Education', 'Utilities']

# Base prices per category per region (LKR)
base_prices = {
    'Colombo':    {'Food': 25000, 'Transport': 8000,  'Housing': 45000, 'Healthcare': 12000, 'Education': 15000, 'Utilities': 6000},
    'Kandy':      {'Food': 22000, 'Transport': 7000,  'Housing': 32000, 'Healthcare': 10000, 'Education': 12000, 'Utilities': 5000},
    'Galle':      {'Food': 21000, 'Transport': 6500,  'Housing': 28000, 'Healthcare': 9000,  'Education': 11000, 'Utilities': 4800},
    'Jaffna':     {'Food': 20000, 'Transport': 6000,  'Housing': 25000, 'Healthcare': 8500,  'Education': 10000, 'Utilities': 4500},
}

# Inflation multipliers by year (2022 crisis visible)
inflation = {
    2019: 1.00,
    2020: 1.06,
    2021: 1.12,
    2022: 1.45,  # economic crisis spike
    2023: 1.68,
    2024: 1.75,
}

records = []

for region in regions:
    for year in years:
        for month in months:
            for category in categories:
                base = base_prices[region][category]
                inf = inflation[year]
                seasonal = 1 + 0.03 * np.sin(2 * np.pi * month / 12)
                noise = np.random.uniform(0.97, 1.03)
                price = round(base * inf * seasonal * noise, 2)
                records.append({
                    'Year': year,
                    'Month': month,
                    'Region': region,
                    'Category': category,
                    'Monthly_Cost_LKR': price
                })

df = pd.DataFrame(records)
os.makedirs('data', exist_ok=True)
df.to_csv('data/sl_cost_of_living.csv', index=False)
print(f"Dataset created: {len(df)} rows")
print(df.head(10))