import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId

# --- Input Model ---
class JobDescription(BaseContract):
    job_id: str
    title: str
    requirements: list[str] = Field(default_factory=list)
    experience: int = 0

# --- Intelligence Artifacts ---
class JobRequirement(BaseContract):
    requirement_id: ArtifactId = Field(default_factory=uuid.uuid4)
    requirement_type: str  # e.g. REQUIRES_SKILL, PREFERS_SKILL, REQUIRES_EXPERIENCE
    target_value: str
    severity: str = "MUST_HAVE"

class JobSignal(BaseContract):
    signal_id: ArtifactId = Field(default_factory=uuid.uuid4)
    signal_name: str
    signal_value: str | float | bool

class JobProfile(BaseContract):
    profile_id: ArtifactId = Field(default_factory=uuid.uuid4)
    job_id: str
    title: str

class JobIntelligenceCatalog(IntelligenceArtifact):
    catalog_id: ArtifactId = Field(default_factory=uuid.uuid4)
    profiles: tuple[JobProfile, ...] = Field(default_factory=tuple)
    requirements: tuple[JobRequirement, ...] = Field(default_factory=tuple)
    signals: tuple[JobSignal, ...] = Field(default_factory=tuple)
