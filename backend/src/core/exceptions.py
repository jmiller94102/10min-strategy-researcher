"""Custom exceptions"""


class PipelineException(Exception):
    """Base exception for pipeline errors"""
    pass


class InvalidTickerError(PipelineException):
    """Unknown company ticker"""
    def __init__(self, ticker: str):
        self.ticker = ticker
        super().__init__(f"Ticker '{ticker}' not found")


class DaytonaUnavailableError(PipelineException):
    """Daytona service unavailable"""
    pass


class LLMAPIError(PipelineException):
    """LLM API error"""
    pass


class RateLimitExceededError(PipelineException):
    """Rate limit exceeded"""
    pass


class SECNavigationError(PipelineException):
    """SEC EDGAR navigation error"""
    pass


class ParsingError(PipelineException):
    """10-K parsing error"""
    pass
