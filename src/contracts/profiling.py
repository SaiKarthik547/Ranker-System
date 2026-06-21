"""
Profiling contracts.
"""

import uuid

from pydantic import Field, model_validator

from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.enums import MetricType
from src.contracts.types import ArtifactId, ProfileMetricValue


class ProfileMetric(BaseContract):
    """Immutable representation of a single statistical metric."""

    metric_id: ArtifactId = Field(default_factory=uuid.uuid4)
    field_path: str = Field(min_length=1)
    metric_type: MetricType
    metric_value: ProfileMetricValue
    calculation_method: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_metric_context(self) -> "ProfileMetric":
        """Enforce strict contextual bounds based on metric_type."""
        if self.metric_type == MetricType.NULLABILITY:
            if not isinstance(self.metric_value, float) or not (
                0.0 <= self.metric_value <= 1.0
            ):
                raise ValueError("NULLABILITY must be a float between 0.0 and 1.0")

        elif self.metric_type == MetricType.CARDINALITY:
            if not isinstance(self.metric_value, int) or self.metric_value < 0:
                raise ValueError("CARDINALITY must be an int >= 0")

        return self


class ProfileReport(IntelligenceArtifact):
    """Aggregation of all statistical findings across the entire dataset."""

    report_id: ArtifactId = Field(default_factory=uuid.uuid4)
    field_metrics: tuple[ProfileMetric, ...] = Field(min_length=1)
    summary: str | None = None
