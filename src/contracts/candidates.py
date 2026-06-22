import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId
from src.contracts.enums import CandidateSignalType, SignalCategory

class CandidateSignal(BaseContract):
    """Immutable representation of a generated candidate signal."""
    signal_id: ArtifactId = Field(default_factory=uuid.uuid4)
    signal_name: CandidateSignalType
    signal_type: SignalCategory
    rationale: tuple[str, ...] = Field(default_factory=tuple)

class CandidateProfile(IntelligenceArtifact):
    """Candidate profile encapsulating structured intelligence and descriptive summaries."""
    candidate_id: str = Field(min_length=1)
    
    # Structured Intelligence
    skills: tuple[str, ...] = Field(default_factory=tuple)
    companies: tuple[str, ...] = Field(default_factory=tuple)
    roles: tuple[str, ...] = Field(default_factory=tuple)
    certifications: tuple[str, ...] = Field(default_factory=tuple)
    languages: tuple[str, ...] = Field(default_factory=tuple)
    
    # Human Readable Intelligence
    identity_summary: str
    skills_summary: str
    experience_summary: str
    education_summary: str
    certification_summary: str
    language_summary: str
    career_progression_summary: str
    intelligence_summary: str
    
    strength_signals: tuple[CandidateSignal, ...] = Field(default_factory=tuple)
    risk_signals: tuple[CandidateSignal, ...] = Field(default_factory=tuple)
    
    completeness_score: float = Field(ge=0.0, le=100.0)
    profile_quality_score: float = Field(ge=0.0, le=100.0)

class CandidateIntelligenceCatalog(IntelligenceArtifact):
    """Global catalog containing all candidate profiles and signals."""
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    profiles: tuple[CandidateProfile, ...] = Field(default_factory=tuple)
    all_signals: tuple[CandidateSignal, ...] = Field(default_factory=tuple)
