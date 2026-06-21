"""
Base contract definitions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from src.contracts.confidence import Confidence
    from src.contracts.evidence import Evidence
    from src.contracts.metadata import ArtifactMetadata


class BaseContract(BaseModel):
    """
    Root contract for all intelligence models.
    Enforces strict typing and immutability.
    """

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
        arbitrary_types_allowed=False,
    )


class BaseArtifact(BaseContract):
    """
    A generated intelligence artifact that tracks its own metadata.
    """

    metadata: ArtifactMetadata


class IntelligenceArtifact(BaseArtifact):
    """
    A higher-order artifact backed by confidence and evidence.
    """

    confidence: Confidence
    evidence: list[Evidence]
