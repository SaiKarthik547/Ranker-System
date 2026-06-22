import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class Relationship(BaseContract):
    relationship_id: ArtifactId = Field(default_factory=uuid.uuid4)
    source_entity: str = Field(min_length=1)
    target_entity: str = Field(min_length=1)
    relationship_type: str = Field(min_length=1)
    weight: float = Field(ge=0.0, le=1.0, default=1.0)

class RelationshipCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    relationships: tuple[Relationship, ...] = Field(default_factory=tuple)
