import uuid
from typing import Literal
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class RankingPolicy(BaseContract):
    sort_order: Literal["ASC", "DESC"] = "DESC"
    max_results: int = 100

class RankedCandidate(BaseContract):
    rank: int
    candidate_id: str
    job_id: str
    score_id: ArtifactId
    alignment_id: ArtifactId
    final_score: float
    factor_count: int
    evidence_count: int
    top_factors: tuple[str, ...]
    factor_contributions: tuple[float, ...]

class RankedCandidateCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    generation_policy: RankingPolicy
    ranked_candidates: tuple[RankedCandidate, ...] = Field(default_factory=tuple)
