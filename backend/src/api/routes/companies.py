"""Company intelligence API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import List

from src.models.company import Company, CompanyProfile
from src.core.logging_config import logger

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

# Hardcoded company list
COMPANIES = [
    {"name": "Microsoft", "ticker": "MSFT", "cik": "0000789019", "domain": "microsoft.com"},
    {"name": "Apple", "ticker": "AAPL", "cik": "0000320193", "domain": "apple.com"},
    {"name": "NVIDIA", "ticker": "NVDA", "cik": "0001045810", "domain": "nvidia.com"},
    {"name": "Alphabet", "ticker": "GOOGL", "cik": "0001652044", "domain": "google.com"},
    {"name": "Amazon", "ticker": "AMZN", "cik": "0001018724", "domain": "amazon.com"},
    {"name": "Meta", "ticker": "META", "cik": "0001326801", "domain": "meta.com"},
    {"name": "Tesla", "ticker": "TSLA", "cik": "0001318605", "domain": "tesla.com"},
    {"name": "Salesforce", "ticker": "CRM", "cik": "0001108524", "domain": "salesforce.com"},
    {"name": "Adobe", "ticker": "ADBE", "cik": "0000796343", "domain": "adobe.com"},
    {"name": "Netflix", "ticker": "NFLX", "cik": "0001065280", "domain": "netflix.com"}
]


@router.get("", response_model=dict)
async def list_companies():
    """List all available companies"""
    companies = [Company(**c) for c in COMPANIES]
    return {"companies": companies}


@router.get("/{ticker}", response_model=CompanyProfile)
async def get_company(ticker: str):
    """Get full intelligence profile for a company"""
    logger.info(f"Fetching company profile for {ticker}")

    # TODO: Implement real company retrieval from cache/database
    raise HTTPException(
        status_code=425,
        detail=f"Profile for {ticker} not ready. Run the pipeline first."
    )


@router.get("/{ticker}/insights")
async def get_company_insights(ticker: str):
    """Get only AI insights (without enrichment)"""
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{ticker}/enrichment")
async def get_company_enrichment(ticker: str):
    """Get only live enrichment data"""
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented yet")
