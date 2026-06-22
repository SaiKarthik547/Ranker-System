import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class SemanticConcept(BaseContract):
    concept_id: ArtifactId = Field(default_factory=uuid.uuid4)
    field_path: str = Field(min_length=1)
    concept_name: str = Field(min_length=1)
    concept_type: str = Field(min_length=1)

class SemanticCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    concepts: tuple[SemanticConcept, ...] = Field(default_factory=tuple)
