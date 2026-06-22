import uuid
from src.contracts import KnowledgeGraph, ArtifactMetadata, Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.job import JobDescription, JobProfile, JobRequirement, JobSignal, JobIntelligenceCatalog

class JobIntelligenceEngine:
    def process(self, jobs: list[JobDescription], kg: KnowledgeGraph, run_id: uuid.UUID) -> JobIntelligenceCatalog:
        profiles = []
        requirements = []
        signals = []
        
        # NOTE: STRICT ARCHITECTURE RULE
        # This layer ONLY extracts job intelligence artifacts.
        # It MUST NOT compute candidate matches, comparisons, or rankings here.
        
        for job in jobs:
            profiles.append(JobProfile(
                job_id=job.job_id,
                title=job.title
            ))
            
            # Extract experience requirements
            if job.experience > 0:
                requirements.append(JobRequirement(
                    requirement_type="REQUIRES_EXPERIENCE",
                    target_value=str(job.experience),
                    severity="MUST_HAVE"
                ))
                
            # Extract skills/technologies
            for req in job.requirements:
                # We could potentially align req with KnowledgeGraph nodes here to map it to standard identifiers
                # but no candidate matching is allowed.
                requirements.append(JobRequirement(
                    requirement_type="REQUIRES_SKILL",
                    target_value=req,
                    severity="MUST_HAVE"
                ))
                
            # Generate signals
            signals.append(JobSignal(
                signal_name="IS_SENIOR",
                signal_value=bool(job.experience >= 5 or "senior" in job.title.lower())
            ))
            
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.JOB_INTELLIGENCE_CATALOG,
            producer_module="job_engine",
            pipeline_run_id=run_id
        )
        conf = Confidence(
            confidence_score=0.9,
            confidence_level=ConfidenceLevel.HIGH,
            confidence_method="heuristic",
            confidence_explanation="Job description deterministic extraction"
        )
        
        return JobIntelligenceCatalog(
            metadata=meta,
            confidence=conf,
            profiles=tuple(profiles),
            requirements=tuple(requirements),
            signals=tuple(signals)
        )
