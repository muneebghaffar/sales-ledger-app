import json
import pandas as pd
import os
from datetime import datetime
from app.core.config import config

def load_sales_data():
    file_path = config.JSON_OUTPUT_PATH
    print(f"Attempting to load sales_data.json from: {file_path}")
    if not os.path.exists(file_path):
        print(f"Error: File does not exist at {file_path}")
        raise FileNotFoundError(f"Sales data JSON file not found at {file_path}")
    if os.path.getsize(file_path) == 0:
        print(f"Error: File is empty at {file_path}")
        raise ValueError(f"Sales data JSON file is empty at {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"File content (first 100 chars): {content[:100]}")
            data = json.loads(content)
            print("Successfully loaded sales_data.json")
            return data
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in sales_data.json: {str(e)}")
        raise ValueError(f"Invalid JSON in sales_data.json: {str(e)}") from e
    except Exception as e:
        print(f"Error loading sales_data.json: {str(e)}")
        raise

def filter_sales_data(filters: dict):
    data = load_sales_data()
    period_data = data["periods"]
    filtered_data = {}
    for period, months in period_data.items():
        filtered_data[period] = {}
        for month, products in months.items():
            filtered_data[period][month] = {}
            for product, transactions in products.items():
                filtered_transactions = [
                    tx for tx in transactions
                    if all(
                        (not filters.get("customer") or tx["Customer"] in filters["customer"]) and
                        (not filters.get("currency") or tx["Currency"] in filters["currency"]) and
                        (not filters.get("location") or tx["Location"] in filters["location"]) and
                        (not filters.get("date") or pd.to_datetime(tx["Date"]).year == filters["date"])
                    )
                ]
                if filtered_transactions:
                    filtered_data[period][month][product] = filtered_transactions
    return {
        **data,
        "periods": filtered_data
    }