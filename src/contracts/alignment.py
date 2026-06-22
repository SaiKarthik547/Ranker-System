import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

class AlignmentEvidence(BaseContract):
    evidence_id: ArtifactId = Field(default_factory=uuid.uuid4)
    candidate_id: str
    job_id: str
    evidence_type: str
    evidence_text: str
    confidence: float = 1.0
    entity_centrality: float | None = None

class AlignmentSignal(BaseContract):
    signal_id: ArtifactId = Field(default_factory=uuid.uuid4)
    candidate_id: str
    job_id: str
    signal_name: str
    signal_value: str

class CandidateJobAlignment(BaseContract):
    alignment_id: ArtifactId = Field(default_factory=uuid.uuid4)
    candidate_id: str
    job_id: str
    alignment_signals: tuple[AlignmentSignal, ...] = Field(default_factory=tuple)
    alignment_evidence: tuple[AlignmentEvidence, ...] = Field(default_factory=tuple)
    alignment_summary: str = "Alignment processed successfully"

class AlignmentCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    alignments: tuple[CandidateJobAlignment, ...] = Field(default_factory=tuple)
