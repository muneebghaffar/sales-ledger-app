from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JSON_FILE = "public/data/sales_data.json"

def load_sales_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sales data: {str(e)}")

@app.get("/api/sales-data")
async def get_sales_data(
    customer: Optional[List[str]] = None,
    currency: Optional[List[str]] = None,
    location: Optional[List[str]] = None,
    date: Optional[int] = None,
    fromDate: Optional[str] = None,
    toDate: Optional[str] = None
):
    data = load_sales_data()

    if not (customer or currency or location or date or fromDate or toDate):
        return data

    from_date = None
    to_date = None
    if fromDate:
        try:
            from_date = datetime.strptime(fromDate, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid fromDate format. Use YYYY-MM-DD.")
    if toDate:
        try:
            to_date = datetime.strptime(toDate, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid toDate format. Use YYYY-MM-DD.")

    filtered_data = data.copy()
    filtered_periods = {}

    target_fiscal_years = []
    if date:
        target_fiscal_years = [f"F{date + 1}"]
    else:
        target_fiscal_years = list(data["periods"].keys())

    for fiscal_year in target_fiscal_years:
        if fiscal_year not in data["periods"]:
            continue

        fiscal_periods = data["periods"][fiscal_year]
        filtered_fiscal_periods = {}

        for month, products in fiscal_periods.items():
            filtered_products = {}

            month_date = datetime.strptime(month + '-01', '%Y-%m-%d')
            if from_date and month_date < from_date:
                continue
            if to_date and month_date > to_date:
                continue

            for product, transactions in products.items():
                filtered_transactions = transactions

                if customer:
                    filtered_transactions = [
                        tx for tx in filtered_transactions
                        if tx.get("Company") in customer
                    ]
                if currency:
                    filtered_transactions = [
                        tx for tx in filtered_transactions
                        if tx.get("Original Currency") in currency
                    ]
                if location:
                    filtered_transactions = [
                        tx for tx in filtered_transactions
                        if tx.get("Location") in location
                    ]
                if from_date or to_date:
                    filtered_transactions = [
                        tx for tx in filtered_transactions
                        if (not from_date or datetime.strptime(tx["Date"], '%Y-%m-%d') >= from_date) and
                           (not to_date or datetime.strptime(tx["Date"], '%Y-%m-%d') <= to_date)
                    ]

                if filtered_transactions:
                    filtered_products[product] = filtered_transactions

            if filtered_products:
                filtered_fiscal_periods[month] = filtered_products

        if filtered_fiscal_periods:
            filtered_periods[fiscal_year] = filtered_fiscal_periods

    filtered_data["periods"] = filtered_periods

    all_transactions = []
    for fiscal_year, periods in filtered_periods.items():
        for month, products in periods.items():
            for product, transactions in products.items():
                all_transactions.extend(transactions)

    filtered_data["meta"] = {
        "customers": list(set(tx.get("Company") for tx in all_transactions if tx.get("Company"))),
        "currencies": list(set(tx.get("Original Currency") for tx in all_transactions if tx.get("Original Currency"))),
        "locations": list(set(tx.get("Location") for tx in all_transactions if tx.get("Location")))
    }

    return filtered_data