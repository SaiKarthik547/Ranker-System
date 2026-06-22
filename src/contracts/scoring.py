import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId
from src.contracts.confidence import Confidence

class ScoringFactor(BaseContract):
    factor_id: ArtifactId = Field(default_factory=uuid.uuid4)
    factor_name: str
    raw_strength: float
    normalized_strength: float
    contribution: float
    confidence: Confidence

class CandidateJobScore(IntelligenceArtifact):
    score_id: ArtifactId = Field(default_factory=uuid.uuid4)
    alignment_id: ArtifactId
    candidate_id: str
    job_id: str
    factors: tuple[ScoringFactor, ...] = Field(default_factory=tuple)
    final_score: float

class ScoringCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    scores: tuple[CandidateJobScore, ...] = Field(default_factory=tuple)
