import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SALES_LEDGER_PATH = os.getenv("SALES_LEDGER_PATH", "data-sets/Sales Ledger.xlsx")
    JSON_OUTPUT_PATH = os.getenv("JSON_OUTPUT_PATH", "public/data/sales_data.json")

config = Config()