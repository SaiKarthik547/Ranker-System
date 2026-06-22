import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class Cluster(BaseContract):
    cluster_id: ArtifactId = Field(default_factory=uuid.uuid4)
    cluster_name: str = Field(min_length=1)
    size: int = Field(ge=0)

class ClusterCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    clusters: tuple[Cluster, ...] = Field(default_factory=tuple)
