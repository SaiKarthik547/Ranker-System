import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class IntelligenceSummary(BaseContract):
    summary_id: ArtifactId = Field(default_factory=uuid.uuid4)
    summary_text: str = Field(min_length=1)

class IntelligenceReport(IntelligenceArtifact):
    report_id: ArtifactId = Field(default_factory=uuid.uuid4)
    summaries: tuple[IntelligenceSummary, ...] = Field(default_factory=tuple)
