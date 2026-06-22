import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class TopGraphEntity(BaseContract):
    entity_id: str
    entity_type: str
    label: str
    degree: int = 0
    normalized_degree: float = 0.0
    relationship_count: int = 0
    connected_candidate_count: int = 0

class EntityCentralityCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    top_entities: tuple[TopGraphEntity, ...] = Field(default_factory=tuple)
