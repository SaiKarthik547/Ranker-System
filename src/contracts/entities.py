import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class Entity(BaseContract):
    entity_id: ArtifactId = Field(default_factory=uuid.uuid4)
    entity_name: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    mentions: int = Field(ge=0, default=1)
    source_record_id: str | None = None
    source_field_path: str | None = None

class EntityCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    entities: tuple[Entity, ...] = Field(default_factory=tuple)
