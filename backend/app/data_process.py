import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
SALES_LEDGER = "data-sets/Sales Ledger.xlsx"
JSON_OUTPUT = "public/data/sales_data.json"

def process_sales_data():
    print("Starting process_sales_data")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Checking for Sales Ledger at: {SALES_LEDGER}")
    
    if not os.path.exists(SALES_LEDGER):
        print(f"Error: {SALES_LEDGER} does not exist")
        raise FileNotFoundError(f"{SALES_LEDGER} not found")
    
    try:
        print("Reading Sales Ledger.xlsx")
        df = pd.read_excel(SALES_LEDGER)
        print(f"Read {len(df)} rows from Sales Ledger.xlsx")
        print(f"Columns in Excel: {df.columns.tolist()}")
        
        if df.empty:
            print("Warning: Excel file is empty, generating minimal JSON")
            processed_data = {
                "company_name": "Fangtooth Technologies Inc.",
                "currency": "CAD",
                "denomination": "$",
                "periods": {},
                "meta": {
                    "customers": [],
                    "currencies": [],
                    "locations": []
                },
                "product_colors": {
                    "Hats": "#104861",
                    "T-Shirts": "#DDDDDD"
                }
            }
        else:
            df['Date'] = pd.to_datetime(df['Date'])
            
            customers = df['Company'].unique().tolist() if 'Company' in df else []
            currencies = df['Original Currency'].unique().tolist() if 'Original Currency' in df else []
            locations = df['Location'].unique().tolist() if 'Location' in df else []
            print(f"Customers: {customers}")
            print(f"Currencies: {currencies}")
            print(f"Locations: {locations}")
            
            periods = {}
            for year in df['Date'].dt.year.unique():
                fiscal_year = f"F{year + 1}"
                periods[fiscal_year] = {}
                year_data = df[df['Date'].dt.year == year]
                for month in year_data['Date'].dt.strftime('%Y-%m').unique():
                    periods[fiscal_year][month] = {}
                    month_data = year_data[year_data['Date'].dt.strftime('%Y-%m') == month]
                    for product in month_data['Purchase'].unique():
                        product_data = month_data[month_data['Purchase'] == product]
                        transactions = product_data.to_dict('records')
                        for tx in transactions:
                            tx['Date'] = tx['Date'].strftime('%Y-%m-%d')
                        periods[fiscal_year][month][product] = transactions
            
            print(f"Processed periods (sample): {json.dumps(periods, indent=2)[:200]}...")
            
            processed_data = {
                "company_name": "Fangtooth Technologies Inc.",
                "currency": "CAD",
                "denomination": "$",
                "periods": periods,
                "meta": {
                    "customers": customers,
                    "currencies": currencies,
                    "locations": locations
                },
                "product_colors": {
                    "Hats": "#104861",
                    "T-Shirts": "#DDDDDD"
                }
            }
        
        print(f"Writing to {JSON_OUTPUT}")
        Path(JSON_OUTPUT).parent.mkdir(parents=True, exist_ok=True)
        with open(JSON_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=4)
        print(f"Successfully wrote to {JSON_OUTPUT}")
        print(f"File size: {os.path.getsize(JSON_OUTPUT)} bytes")
    
    except Exception as e:
        print(f"Error processing sales data: {str(e)}")
        raise

if __name__ == "__main__":
    print("Running data_process.py as main")
    process_sales_data()