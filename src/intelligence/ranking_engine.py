import uuid
from typing import List, Dict
from src.contracts import ScoringCatalog, ArtifactMetadata, Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.ranking import RankingPolicy, RankedCandidate, RankedCandidateCatalog

class RankingPolicyEngine:
    def process(self, scoring_catalog: ScoringCatalog, policy: RankingPolicy, run_id: uuid.UUID) -> RankedCandidateCatalog:
        # Group scores by job_id
        from collections import defaultdict
        grouped_scores = defaultdict(list)
        for s in scoring_catalog.scores:
            grouped_scores[s.job_id].append(s)
            
        ranked_items: List[RankedCandidate] = []
        
        for job_id, scores_for_job in grouped_scores.items():
            # Sort deterministically within the job
            sorted_scores = sorted(
                scores_for_job,
                key=lambda s: (-s.final_score if policy.sort_order == "DESC" else s.final_score, s.candidate_id)
            )
            
            if policy.max_results > 0:
                sorted_scores = sorted_scores[:policy.max_results]
                
            for index, score in enumerate(sorted_scores, start=1):
                # Extract top 2 factors by contribution
                sorted_factors = sorted(score.factors, key=lambda f: -f.contribution)
                top_2 = sorted_factors[:2]
                
                ranked_items.append(RankedCandidate(
                    rank=index,
                    candidate_id=score.candidate_id,
                    job_id=score.job_id,
                    score_id=score.score_id,
                    alignment_id=score.alignment_id,
                    final_score=score.final_score,
                    factor_count=len(score.factors),
                    evidence_count=0,
                    top_factors=tuple(f.factor_name for f in top_2),
                    factor_contributions=tuple(f.contribution for f in top_2)
                ))
            
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.RANKED_CANDIDATE_CATALOG,
            producer_module="ranking_engine",
            pipeline_run_id=run_id
        )
        
        conf = Confidence(
            confidence_score=1.0,
            confidence_level=ConfidenceLevel.HIGH,
            confidence_method="deterministic_sort",
            confidence_explanation=f"Ranked {len(ranked_items)} items using Policy(order={policy.sort_order})"
        )
        
        return RankedCandidateCatalog(
            metadata=meta,
            confidence=conf,
            generation_policy=policy,
            ranked_candidates=tuple(ranked_items)
        )
