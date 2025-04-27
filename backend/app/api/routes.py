from fastapi import APIRouter, Query
from typing import List, Optional
from app.services.data_service import load_sales_data, filter_sales_data

router = APIRouter()

@router.get("/sales-data")
async def get_sales_data(
    customer: Optional[List[str]] = Query(None),
    currency: Optional[List[str]] = Query(None),
    location: Optional[List[str]] = Query(None),
    date: Optional[int] = Query(None)
):
    filters = {
        "customer": customer,
        "currency": currency,
        "location": location,
        "date": date
    }
    if any(filters.values()):
        return filter_sales_data(filters)
    return load_sales_data()