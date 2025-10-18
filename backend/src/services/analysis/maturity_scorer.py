"""AI maturity scoring algorithm"""
from src.core.logging_config import logger


class AIMaturityScorer:
    """Calculate AI maturity score for companies"""

    def calculate_score(self, insights: dict, enrichment: dict = None) -> dict:
        """
        Calculate AI maturity score (0-100)

        Args:
            insights: AI insights from LLM extraction
            enrichment: Optional enrichment data (jobs, tech stack)

        Returns:
            Dict with score, tier, and breakdown
        """
        score = 0
        breakdown = {}

        # Investment score (0-30 points)
        investment_score = self._score_investments(insights.get("investments", {}))
        score += investment_score
        breakdown["investments"] = investment_score

        # Products score (0-25 points)
        products_score = self._score_products(insights.get("products", []))
        score += products_score
        breakdown["products"] = products_score

        # Risks score (0-15 points) - more risks = more mature (they're aware)
        risks_score = min(len(insights.get("risks", [])) * 3, 15)
        score += risks_score
        breakdown["risks"] = risks_score

        # Enrichment score (0-30 points)
        if enrichment:
            enrichment_score = self._score_enrichment(enrichment)
            score += enrichment_score
            breakdown["enrichment"] = enrichment_score

        # Determine tier
        if score >= 80:
            tier = "Leader"
        elif score >= 60:
            tier = "Advanced"
        elif score >= 40:
            tier = "Developing"
        else:
            tier = "Early"

        logger.info(f"AI Maturity Score: {score}/100 ({tier})")

        return {
            "score": score,
            "tier": tier,
            "breakdown": breakdown
        }

    def _score_investments(self, investments: dict) -> int:
        """Score based on AI investments (0-30)"""
        total = investments.get("total_amount", "")
        details = investments.get("details", [])

        if "billion" in total.lower():
            return 30
        elif "million" in total.lower() or len(details) >= 3:
            return 20
        elif len(details) >= 1:
            return 10
        else:
            return 0

    def _score_products(self, products: list) -> int:
        """Score based on AI products (0-25)"""
        count = len(products)

        if count >= 5:
            return 25
        elif count >= 3:
            return 20
        elif count >= 1:
            return 10
        else:
            return 0

    def _score_enrichment(self, enrichment: dict) -> int:
        """Score based on live enrichment data (0-30)"""
        score = 0

        # AI jobs
        ai_jobs = enrichment.get("ai_jobs", [])
        if len(ai_jobs) >= 20:
            score += 15
        elif len(ai_jobs) >= 10:
            score += 10
        elif len(ai_jobs) >= 5:
            score += 5

        # Tech stack
        tech_stack = enrichment.get("tech_stack", [])
        if len(tech_stack) >= 5:
            score += 15
        elif len(tech_stack) >= 3:
            score += 10
        elif len(tech_stack) >= 1:
            score += 5

        return score
