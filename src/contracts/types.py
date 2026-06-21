"""
Reusable types for data contracts.
"""

import uuid
from typing import Annotated

from pydantic import Field

ArtifactId = uuid.UUID
PipelineRunId = uuid.UUID
EvidenceId = uuid.UUID
SemVer = str
ConfidenceSemVer = Annotated[str, Field(pattern=r"^\d+\.\d+\.\d+$")]
ConfidenceScore = Annotated[float, Field(ge=0.0, le=1.0)]

# Complex bounded types
PrimitiveValue = str | int | float | bool | None
ProfileMetricValue = float | int | str | tuple[tuple[str, float], ...]
