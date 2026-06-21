"""
Confidence contract.
"""

from pydantic import Field

from src.contracts.base import BaseContract
from src.contracts.enums import ConfidenceLevel
from src.contracts.types import ConfidenceScore


class Confidence(BaseContract):
    """Derived confidence information."""

    confidence_score: ConfidenceScore
    confidence_level: ConfidenceLevel
    confidence_method: str
    confidence_factors: tuple[tuple[str, float], ...] = Field(default_factory=tuple)
    confidence_explanation: str
