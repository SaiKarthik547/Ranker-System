import uuid
from typing import List
from src.contracts import AlignmentCatalog, ArtifactMetadata, Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.scoring import ScoringFactor, CandidateJobScore, ScoringCatalog

class ScoringIntelligenceEngine:
    def process(self, alignment_catalog: AlignmentCatalog, run_id: uuid.UUID) -> ScoringCatalog:
        scores = []
        
        for alignment in alignment_catalog.alignments:
            factors: List[ScoringFactor] = []
            
            # 1. Skill Match Factor
            skill_evidences = [e for e in alignment.alignment_evidence if e.evidence_type == "SKILL_MATCH"]
            skill_count = len(skill_evidences)
            
            # Normalize against an arbitrary small number for prototyping (e.g. 5 skills max)
            skill_norm = min(1.0, skill_count / 5.0)
            
            factors.append(ScoringFactor(
                factor_name="SKILL_MATCH_FACTOR",
                raw_strength=float(skill_count),
                normalized_strength=skill_norm,
                contribution=skill_norm,
                confidence=Confidence(
                    confidence_score=1.0,
                    confidence_level=ConfidenceLevel.HIGH,
                    confidence_method="deterministic",
                    confidence_explanation=f"Calculated from {skill_count} direct skill matches"
                )
            ))
            
            # 2. Experience Factor
            exp_signals = [s for s in alignment.alignment_signals if s.signal_name == "EXPERIENCE_ALIGNMENT"]
            exp_val = 1.0 if len(exp_signals) > 0 else 0.0
            
            factors.append(ScoringFactor(
                factor_name="EXPERIENCE_FACTOR",
                raw_strength=exp_val,
                normalized_strength=exp_val,
                contribution=exp_val,
                confidence=Confidence(
                    confidence_score=1.0,
                    confidence_level=ConfidenceLevel.HIGH,
                    confidence_method="deterministic",
                    confidence_explanation="Presence of EXPERIENCE_ALIGNMENT signal"
                )
            ))
            
            # 3. Centrality Rarity Factor
            centrality_values = [
                e.entity_centrality for e in skill_evidences 
                if e.entity_centrality is not None
            ]
            
            if centrality_values:
                # Calculate mean(1.0 - centrality)
                rarity = sum((1.0 - c) for c in centrality_values) / len(centrality_values)
            else:
                rarity = 0.5 # Default neutral rarity if no graph data
                
            factors.append(ScoringFactor(
                factor_name="CENTRALITY_RARITY_FACTOR",
                raw_strength=rarity,
                normalized_strength=rarity,
                contribution=rarity,
                confidence=Confidence(
                    confidence_score=0.9,
                    confidence_level=ConfidenceLevel.HIGH,
                    confidence_method="topological_inference",
                    confidence_explanation="Average inverse centrality of matched entities"
                )
            ))
            
            # Calculate final score deterministically via average (sum(contributions) / len(factors))
            final_score = sum(f.contribution for f in factors) / len(factors)
            
            scores.append(CandidateJobScore(
                alignment_id=alignment.alignment_id,
                candidate_id=alignment.candidate_id,
                job_id=alignment.job_id,
                factors=tuple(factors),
                final_score=final_score,
                metadata=ArtifactMetadata(
                    artifact_type=ArtifactType.CANDIDATE_JOB_SCORE,
                    producer_module="scoring_engine",
                    pipeline_run_id=run_id
                ),
                confidence=Confidence(
                    confidence_score=0.9,
                    confidence_level=ConfidenceLevel.HIGH,
                    confidence_method="aggregate",
                    confidence_explanation="Computed average from deterministically extracted factors"
                )
            ))
            
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.SCORING_CATALOG,
            producer_module="scoring_engine",
            pipeline_run_id=run_id
        )
        conf = Confidence(
            confidence_score=0.95,
            confidence_level=ConfidenceLevel.HIGH,
            confidence_method="aggregate",
            confidence_explanation="Scores generated entirely from AlignmentCatalog signals"
        )
            
        return ScoringCatalog(
            metadata=meta,
            confidence=conf,
            scores=tuple(scores)
        )
