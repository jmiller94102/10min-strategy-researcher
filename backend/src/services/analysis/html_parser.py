"""Quick HTML parsing for 10-K filings"""
import re
from bs4 import BeautifulSoup

from src.core.logging_config import logger


class TenKHTMLParser:
    """Fast HTML parser for 10-K filings"""

    def parse_10k(self, html_content: str) -> dict:
        """
        Extract clean text from 10-K HTML

        Args:
            html_content: Raw HTML from SEC

        Returns:
            Dict with extracted text sections
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style tags
        for script in soup(["script", "style"]):
            script.decompose()

        # Get all text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Extract AI-related content (simple keyword matching)
        ai_keywords = [
            'artificial intelligence', 'machine learning', 'AI', 'ML',
            'neural network', 'deep learning', 'generative AI', 'GenAI',
            'large language model', 'LLM', 'natural language processing', 'NLP',
            'computer vision', 'reinforcement learning', 'GPT', 'transformer'
        ]

        # Split into sentences
        sentences = re.split(r'[.!?]+', text)

        # Find AI-related sentences
        ai_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 50:  # Too short
                continue

            sentence_lower = sentence.lower()
            if any(keyword.lower() in sentence_lower for keyword in ai_keywords):
                ai_sentences.append(sentence)

        # Limit to 100 most relevant sentences (roughly 50K chars)
        ai_text = '. '.join(ai_sentences[:100])

        logger.info(
            f"Extracted {len(ai_sentences)} AI-related sentences "
            f"from {len(text):,} total chars"
        )

        return {
            "full_text": text[:500000],  # First 500K chars
            "ai_text": ai_text,
            "ai_sentence_count": len(ai_sentences)
        }
