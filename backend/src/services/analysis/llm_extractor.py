"""LLM-powered insight extraction from 10-K filings"""
import json
from typing import Optional
from openai import AsyncAzureOpenAI

from src.core.config import settings
from src.core.logging_config import logger


class AIInsightExtractor:
    """Extract AI insights using Azure OpenAI"""

    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
        self.deployment = settings.azure_openai_chat_deployment

    async def extract_insights(self, ai_text: str, company_name: str) -> dict:
        """
        Extract AI insights from 10-K text

        Args:
            ai_text: AI-related text from 10-K
            company_name: Company name

        Returns:
            Dict with investments, products, risks
        """
        logger.info(f"Extracting AI insights for {company_name} from {len(ai_text):,} chars")

        # Limit input to avoid token limits (GPT-4 context: 128K tokens ~= 400K chars)
        ai_text_limited = ai_text[:100000]  # ~25K tokens

        prompt = f"""You are an expert financial analyst. Analyze this 10-K filing excerpt from {company_name} and extract AI-related information.

Text to analyze:
{ai_text_limited}

Extract the following and return ONLY valid JSON:

{{
  "investments": {{
    "total_amount": "estimated total $ amount or 'not disclosed'",
    "details": [
      {{
        "amount": "specific $ amount if mentioned",
        "purpose": "what the investment is for",
        "quote": "direct quote from text"
      }}
    ]
  }},
  "products": [
    {{
      "name": "product/service name",
      "description": "what it does",
      "quote": "direct quote"
    }}
  ],
  "risks": [
    {{
      "risk": "risk description",
      "quote": "direct quote"
    }}
  ]
}}

Return ONLY the JSON, no other text."""

        try:
            response = await self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": "You are a financial analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )

            result_text = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            result = json.loads(result_text)

            logger.info(
                f"Extracted {len(result.get('investments', {}).get('details', []))} investments, "
                f"{len(result.get('products', []))} products, "
                f"{len(result.get('risks', []))} risks"
            )

            return result

        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            # Return empty structure on failure
            return {
                "investments": {"total_amount": "not disclosed", "details": []},
                "products": [],
                "risks": []
            }
