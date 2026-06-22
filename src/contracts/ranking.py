import uuid
from typing import Literal
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class RankingPolicy(BaseContract):
    sort_order: Literal["ASC", "DESC"] = "DESC"
    max_results: int = 100

class EvidenceObject(BaseContract):
    evidence_type: str
    source_artifact: str
    value: str
    contribution: float

class FactorContribution(BaseContract):
    factor: str
    contribution: float

class RankedCandidate(BaseContract):
    rank: int
    candidate_id: str
    job_id: str
    score_id: ArtifactId
    alignment_id: ArtifactId
    final_score: float
    factor_count: int
    top_factors: tuple[FactorContribution, ...]
    evidence: tuple[EvidenceObject, ...]

class RankedCandidateCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    generation_policy: RankingPolicy
    ranked_candidates: tuple[RankedCandidate, ...] = Field(default_factory=tuple)
