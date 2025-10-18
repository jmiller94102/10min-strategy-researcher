"""LLM-powered insight extraction from 10-K filings"""
import json
from typing import Optional
from datetime import datetime
from openai import AsyncAzureOpenAI
from galileo import galileo_context

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
        
        # Initialize Galileo if API key is configured
        self.galileo_enabled = bool(settings.galileo_api_key)
        if self.galileo_enabled:
            try:
                galileo_context.init(
                    project=settings.galileo_project,
                    log_stream=settings.galileo_log_stream
                )
                self.galileo_logger = galileo_context.get_logger_instance()
                logger.info("Galileo observability enabled for LLM extraction")
            except Exception as e:
                logger.warning(f"Failed to initialize Galileo: {e}")
                self.galileo_enabled = False

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
            # Start Galileo session and trace if enabled
            if self.galileo_enabled:
                self.galileo_logger.start_session()
                self.galileo_logger.start_trace(
                    name=f"Extract AI Insights - {company_name}",
                    input=f"Analyzing {len(ai_text_limited):,} chars from {company_name} 10-K"
                )
            
            # Capture start time for duration tracking
            start_time_ns = datetime.now().timestamp() * 1_000_000_000
            
            messages = [
                {"role": "system", "content": "You are a financial analyst. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=0.1,
                max_tokens=4000
            )

            result_text = response.choices[0].message.content.strip()
            
            # Log to Galileo if enabled
            if self.galileo_enabled:
                duration_ns = (datetime.now().timestamp() * 1_000_000_000) - start_time_ns
                self.galileo_logger.add_llm_span(
                    input=messages,
                    output=result_text,
                    model=self.deployment,
                    num_input_tokens=response.usage.prompt_tokens if response.usage else 0,
                    num_output_tokens=response.usage.completion_tokens if response.usage else 0,
                    total_tokens=response.usage.total_tokens if response.usage else 0,
                    duration_ns=int(duration_ns)
                )

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
            
            # Conclude Galileo trace if enabled
            if self.galileo_enabled:
                self.galileo_logger.conclude(
                    output=f"Extracted {len(result.get('investments', {}).get('details', []))} investments, "
                           f"{len(result.get('products', []))} products, {len(result.get('risks', []))} risks"
                )
                self.galileo_logger.flush()

            return result

        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            
            # Log error to Galileo if enabled
            if self.galileo_enabled:
                try:
                    self.galileo_logger.conclude(output=f"Error: {str(e)}")
                    self.galileo_logger.flush()
                except:
                    pass
            
            # Return empty structure on failure
            return {
                "investments": {"total_amount": "not disclosed", "details": []},
                "products": [],
                "risks": []
            }
