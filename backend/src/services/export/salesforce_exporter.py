"""Salesforce CRM CSV export"""
import csv
from datetime import datetime
from pathlib import Path
from typing import List

from src.core.logging_config import logger


class SalesforceCSVExporter:
    """Export company profiles to Salesforce-compatible CSV"""

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"SalesforceCSVExporter initialized (output: {output_dir})")

    def export_companies(self, profiles: List[dict]) -> str:
        """
        Export company profiles to CSV

        Args:
            profiles: List of company profile dicts

        Returns:
            Path to generated CSV file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"10k_ai_intelligence_{timestamp}.csv"
        filepath = self.output_dir / filename

        logger.info(f"Exporting {len(profiles)} companies to {filepath}")

        # CSV columns matching Salesforce account import
        fieldnames = [
            "Company Name",
            "Ticker",
            "Domain",
            "AI Maturity Score",
            "AI Maturity Tier",
            "Total AI Investment",
            "AI Products Count",
            "AI Risks Count",
            "AI Jobs Count",
            "Tech Stack",
            "Filing Date",
            "Fiscal Year",
            "Data Source",
            "Last Updated"
        ]

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for profile in profiles:
                company = profile.get("company", {})
                insights = profile.get("insights", {})
                enrichment = profile.get("enrichment", {})
                maturity = profile.get("maturity", {})

                # Extract data
                investments = insights.get("investments", {})
                products = insights.get("products", [])
                risks = insights.get("risks", [])
                ai_jobs = enrichment.get("ai_jobs", [])
                tech_stack = enrichment.get("tech_stack", [])

                row = {
                    "Company Name": company.get("name", ""),
                    "Ticker": company.get("ticker", ""),
                    "Domain": company.get("domain", ""),
                    "AI Maturity Score": maturity.get("score", 0),
                    "AI Maturity Tier": maturity.get("tier", "Early"),
                    "Total AI Investment": investments.get("total_amount", "not disclosed"),
                    "AI Products Count": len(products),
                    "AI Risks Count": len(risks),
                    "AI Jobs Count": len(ai_jobs),
                    "Tech Stack": ", ".join(tech_stack[:10]),  # Top 10
                    "Filing Date": profile.get("filing_date", ""),
                    "Fiscal Year": profile.get("fiscal_year", ""),
                    "Data Source": "SEC 10-K + Live Enrichment",
                    "Last Updated": datetime.now().isoformat()
                }

                writer.writerow(row)

        logger.info(f"✅ Exported {len(profiles)} companies to {filepath}")

        return str(filepath)

    def export_single_company(self, profile: dict) -> str:
        """Export single company profile"""
        return self.export_companies([profile])
