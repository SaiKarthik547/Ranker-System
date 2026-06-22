import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class Anomaly(BaseContract):
    anomaly_id: ArtifactId = Field(default_factory=uuid.uuid4)
    description: str = Field(min_length=1)
    severity: str = Field(min_length=1)

class AnomalyCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    anomalies: tuple[Anomaly, ...] = Field(default_factory=tuple)
