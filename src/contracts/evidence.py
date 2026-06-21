"""
Evidence contract.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pydantic import Field

from src.contracts.base import BaseContract
from src.contracts.types import ArtifactId, EvidenceId, PrimitiveValue

if TYPE_CHECKING:
    from src.contracts.confidence import Confidence


class Evidence(BaseContract):
    """Unit of evidence supporting an intelligence artifact."""

    evidence_id: EvidenceId = Field(default_factory=uuid.uuid4)
    evidence_type: str
    source_artifact: ArtifactId
    source_location: str | None = None
    source_value: PrimitiveValue = None
    reasoning: str
    confidence: Confidence | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
