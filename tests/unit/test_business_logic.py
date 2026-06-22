import pytest
import uuid
from src.intelligence.alignment_engine import AlignmentIntelligenceEngine
from src.intelligence.scoring_engine import ScoringIntelligenceEngine
from src.intelligence.ranking_engine import RankingPolicyEngine
from src.contracts.candidates import CandidateIntelligenceCatalog, CandidateProfile
from src.contracts.job import JobIntelligenceCatalog, JobRequirement, JobProfile
from src.contracts.graph import KnowledgeGraph, GraphEdge, GraphNode
from src.contracts.centrality import EntityCentralityCatalog, TopGraphEntity
from src.contracts.enums import EdgeType, NodeType, ConfidenceLevel, ArtifactType
from src.contracts.evidence import Evidence
from src.contracts.confidence import Confidence
from src.contracts.alignment import AlignmentCatalog, CandidateJobAlignment, AlignmentSignal, AlignmentEvidence
from src.contracts.scoring import ScoringCatalog, CandidateJobScore
from src.contracts.ranking import RankingPolicy
from src.contracts.metadata import ArtifactMetadata

def test_alignment_skill_signal_mapping():
    engine = AlignmentIntelligenceEngine()
    run_id = uuid.uuid4()
    meta = ArtifactMetadata(artifact_type=ArtifactType.CANDIDATE_CATALOG, producer_module="test", pipeline_run_id=uuid.uuid4())
    conf = Confidence(confidence_level=ConfidenceLevel.HIGH, confidence_score=1.0, confidence_method="test", confidence_explanation="test")
    
    cand_cat = CandidateIntelligenceCatalog(
        metadata=meta, confidence=conf,
        profiles=(CandidateProfile(
            metadata=meta, confidence=conf,
            candidate_id="C1", identity_summary="", skills_summary="", experience_summary="", 
            education_summary="", certification_summary="", language_summary="", career_progression_summary="", 
            intelligence_summary="", completeness_score=100.0, profile_quality_score=100.0
        ),)
    )
    
    job_cat = JobIntelligenceCatalog(
        metadata=ArtifactMetadata(artifact_type=ArtifactType.JOB_INTELLIGENCE_CATALOG, producer_module="test", pipeline_run_id=uuid.uuid4()), confidence=conf,
        profiles=(JobProfile(job_id="J1", title="Software Engineer"),),
        requirements=(
            JobRequirement(requirement_id=uuid.uuid4(), requirement_type="REQUIRES_SKILL", target_value="Python"),
        )
    )
    
    graph = KnowledgeGraph(
        metadata=ArtifactMetadata(artifact_type=ArtifactType.KNOWLEDGE_GRAPH, producer_module="test", pipeline_run_id=uuid.uuid4()), confidence=conf,
        nodes=(
            GraphNode(node_id="C1", label="C1", node_type=NodeType.CANDIDATE),
            GraphNode(node_id="E1", label="Python", node_type=NodeType.SKILL),
        ),
        edges=(
            GraphEdge(
                source_node_id="C1", target_node_id="E1", edge_type=EdgeType.POSSESSES_ENTITY,
                confidence=conf
            ),
        )
    )
    
    cent_cat = EntityCentralityCatalog(
        metadata=ArtifactMetadata(artifact_type=ArtifactType.ENTITY_CENTRALITY_CATALOG, producer_module="test", pipeline_run_id=uuid.uuid4()), confidence=conf,
        top_entities=(TopGraphEntity(entity_id="E1", entity_type="SKILL", label="Python", normalized_degree=1.0),)
    )
    
    alignment_cat = engine.process(cand_cat, job_cat, graph, cent_cat, run_id)
    alignments = alignment_cat.alignments
    assert len(alignments) == 1
    
    alignment = alignments[0]
    
    signals = alignment.alignment_signals
    assert len(signals) == 1
    assert signals[0].signal_name == "REQUIRED_SKILL_MET"
    assert signals[0].signal_value == "Python"
    
    evidences = alignment.alignment_evidence
    assert len(evidences) == 1
    assert evidences[0].evidence_type == "SKILL_MATCH"

def test_scoring_skill_contribution():
    engine = ScoringIntelligenceEngine()
    meta = ArtifactMetadata(artifact_type=ArtifactType.ALIGNMENT_CATALOG, producer_module="test", pipeline_run_id=uuid.uuid4())
    conf = Confidence(confidence_level=ConfidenceLevel.HIGH, confidence_score=1.0, confidence_method="test", confidence_explanation="test")
    
    alignment = CandidateJobAlignment(
        candidate_id="C1",
        job_id="J1",
        alignment_signals=(
            AlignmentSignal(candidate_id="C1", job_id="J1", signal_name="REQUIRED_SKILL_MET", signal_value="Python"),
        ),
        alignment_evidence=(
            AlignmentEvidence(candidate_id="C1", job_id="J1", evidence_type="SKILL_MATCH", evidence_text="Has skill Python", entity_centrality=0.8),
        )
    )
    
    alignment_cat = AlignmentCatalog(metadata=meta, confidence=conf, alignments=(alignment,))
    score_cat = engine.process(alignment_cat, run_id=uuid.uuid4())
    
    assert len(score_cat.scores) == 1
    score = score_cat.scores[0]
    
    factor = next((f for f in score.factors if f.factor_name == "SKILL_MATCH_FACTOR"), None)
    assert factor is not None
    assert factor.contribution > 0.0

def test_ranking_changes_when_skill_matches_change():
    engine = RankingPolicyEngine()
    meta = ArtifactMetadata(artifact_type=ArtifactType.SCORING_CATALOG, producer_module="test", pipeline_run_id=uuid.uuid4())
    conf = Confidence(confidence_level=ConfidenceLevel.HIGH, confidence_score=1.0, confidence_method="test", confidence_explanation="test")
    
    score1 = CandidateJobScore(metadata=meta, confidence=conf, alignment_id=uuid.uuid4(), candidate_id="C1", job_id="J1", final_score=0.9, factors=tuple())
    score2 = CandidateJobScore(metadata=meta, confidence=conf, alignment_id=uuid.uuid4(), candidate_id="C2", job_id="J1", final_score=0.5, factors=tuple())
    
    score_cat = ScoringCatalog(metadata=meta, confidence=conf, scores=(score1, score2))
    ranked_cat = engine.process(score_cat, policy=RankingPolicy(), run_id=uuid.uuid4())
    assert ranked_cat.ranked_candidates[0].candidate_id == "C1"
    
    score1_new = CandidateJobScore(metadata=meta, confidence=conf, alignment_id=uuid.uuid4(), candidate_id="C1", job_id="J1", final_score=0.3, factors=tuple())
    score2_new = CandidateJobScore(metadata=meta, confidence=conf, alignment_id=uuid.uuid4(), candidate_id="C2", job_id="J1", final_score=0.8, factors=tuple())
    
    score_cat_flipped = ScoringCatalog(metadata=meta, confidence=conf, scores=(score1_new, score2_new))
    ranked_cat_flipped = engine.process(score_cat_flipped, policy=RankingPolicy(), run_id=uuid.uuid4())
    assert ranked_cat_flipped.ranked_candidates[0].candidate_id == "C2"
