import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class Pattern(BaseContract):
    pattern_id: ArtifactId = Field(default_factory=uuid.uuid4)
    pattern_name: str = Field(min_length=1)
    pattern_description: str = Field(min_length=1)
    frequency: int = Field(ge=0)

class PatternCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    patterns: tuple[Pattern, ...] = Field(default_factory=tuple)
