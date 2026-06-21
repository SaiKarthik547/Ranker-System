"""
Artifact Metadata contract.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pydantic import Field

from src.contracts.base import BaseContract
from src.contracts.enums import ArtifactType
from src.contracts.types import ArtifactId, PipelineRunId, SemVer

if TYPE_CHECKING:
    from src.contracts.confidence import Confidence


class ArtifactMetadata(BaseContract):
    """Metadata tracking for all artifacts."""

    artifact_id: ArtifactId = Field(default_factory=uuid.uuid4)
    artifact_type: ArtifactType
    artifact_version: SemVer = "1.0.0"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    producer_module: str
    pipeline_run_id: PipelineRunId
    schema_version: SemVer = "1.0.0"
    confidence: Confidence | None = None
    evidence_count: int = Field(default=0, ge=0)
    tags: tuple[str, ...] = Field(default_factory=tuple)
