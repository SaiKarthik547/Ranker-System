import uuid
import json
from pathlib import Path

from src.ingestion.engine import IngestionEngine
from src.schema.engine import SchemaDiscoveryEngine
from src.profiling.engine import ProfilingEngine
from src.semantic.engine import SemanticEngine
from src.entities.engine import EntityExtractionEngine
from src.relationships.engine import RelationshipDiscoveryEngine
from src.patterns.engine import PatternDiscoveryEngine
from src.clusters.engine import ClusteringEngine
from src.anomalies.engine import AnomalyDetectionEngine
from src.reports.engine import ReportEngine
from src.intelligence.candidate_engine import CandidateIntelligenceEngine
from src.graph.engine import KnowledgeGraphEngine
from src.graph.centrality import GraphCentralityEngine
from src.intelligence.job_engine import JobIntelligenceEngine
from src.intelligence.alignment_engine import AlignmentIntelligenceEngine
from src.intelligence.scoring_engine import ScoringIntelligenceEngine
from src.intelligence.ranking_engine import RankingPolicyEngine
from src.contracts.job import JobDescription
from src.contracts.ranking import RankingPolicy

class PipelineOrchestrator:
    def __init__(self) -> None:
        self.ingestion = IngestionEngine()
        self.schema = SchemaDiscoveryEngine()
        self.profiling = ProfilingEngine()
        self.semantic = SemanticEngine()
        self.entity = EntityExtractionEngine()
        self.relationship = RelationshipDiscoveryEngine()
        self.pattern = PatternDiscoveryEngine()
        self.cluster = ClusteringEngine()
        self.anomaly = AnomalyDetectionEngine()
        self.report = ReportEngine()
        self.candidate = CandidateIntelligenceEngine()
        self.graph = KnowledgeGraphEngine()
        self.centrality = GraphCentralityEngine()
        self.job = JobIntelligenceEngine()
        self.alignment = AlignmentIntelligenceEngine()
        self.scoring = ScoringIntelligenceEngine()
        self.ranking = RankingPolicyEngine()
        
    def run(self, input_file: str) -> None:
        run_id = uuid.uuid4()
        out_dir = Path("artifacts")
        out_dir.mkdir(exist_ok=True)
        
        print("1. Ingestion...")
        records = self.ingestion.process(input_file, run_id)
        with open(out_dir / "dataset_records.json", "w") as f:
            json.dump([json.loads(r.model_dump_json()) for r in records], f, indent=2)
            
        print("2. Schema Discovery...")
        schema_graph = self.schema.process(records, run_id)
        with open(out_dir / "schema_graph.json", "w") as f:
            f.write(schema_graph.model_dump_json(indent=2))
            
        print("3. Profiling...")
        profile_report = self.profiling.process(records, schema_graph, run_id)
        with open(out_dir / "profile_report.json", "w") as f:
            f.write(profile_report.model_dump_json(indent=2))
            
        print("4. Semantic Analysis...")
        semantic_catalog = self.semantic.process(records, schema_graph, run_id)
        with open(out_dir / "semantic_catalog.json", "w") as f:
            f.write(semantic_catalog.model_dump_json(indent=2))
            
        print("5. Entity Extraction...")
        entity_catalog = self.entity.process(records, schema_graph, semantic_catalog, run_id)
        with open(out_dir / "entity_catalog.json", "w") as f:
            f.write(entity_catalog.model_dump_json(indent=2))
            
        print("6. Relationship Discovery...")
        relationship_catalog = self.relationship.process(records, entity_catalog, run_id)
        with open(out_dir / "relationship_catalog.json", "w") as f:
            f.write(relationship_catalog.model_dump_json(indent=2))
            
        print("7. Pattern Discovery...")
        pattern_catalog = self.pattern.process(records, run_id)
        with open(out_dir / "pattern_catalog.json", "w") as f:
            f.write(pattern_catalog.model_dump_json(indent=2))
            
        print("8. Clustering...")
        cluster_catalog = self.cluster.process(records, run_id)
        with open(out_dir / "cluster_catalog.json", "w") as f:
            f.write(cluster_catalog.model_dump_json(indent=2))
            
        print("9. Anomaly Detection...")
        anomaly_catalog = self.anomaly.process(records, run_id)
        with open(out_dir / "anomaly_catalog.json", "w") as f:
            f.write(anomaly_catalog.model_dump_json(indent=2))
            
        print("10. Report Generation...")
        intelligence_report = self.report.process(run_id)
        with open(out_dir / "intelligence_report.json", "w") as f:
            f.write(intelligence_report.model_dump_json(indent=2))
            
        print("--- PHASE 2 ---")
        print("11. Candidate Intelligence Engine...")
        candidate_catalog = self.candidate.process(
            records=records,
            schema_graph=schema_graph,
            profile_report=profile_report,
            semantic_catalog=semantic_catalog,
            entity_catalog=entity_catalog,
            relationship_catalog=relationship_catalog,
            pattern_catalog=pattern_catalog,
            cluster_catalog=cluster_catalog,
            anomaly_catalog=anomaly_catalog,
            run_id=run_id
        )
        
        with open(out_dir / "candidate_profiles.json", "w") as f:
            f.write("[" + ",\n".join(p.model_dump_json(indent=2) for p in candidate_catalog.profiles) + "]")
            
        with open(out_dir / "candidate_signals.json", "w") as f:
            f.write("[" + ",\n".join(s.model_dump_json(indent=2) for s in candidate_catalog.all_signals) + "]")
            
        with open(out_dir / "candidate_intelligence_catalog.json", "w") as f:
            f.write(candidate_catalog.model_dump_json(indent=2))
            
        print("--- PHASE 3 ---")
        print("12. Knowledge Graph Engine...")
        knowledge_graph, graph_statistics = self.graph.process(
            entity_catalog=entity_catalog,
            relationship_catalog=relationship_catalog,
            pattern_catalog=pattern_catalog,
            cluster_catalog=cluster_catalog,
            anomaly_catalog=anomaly_catalog,
            candidate_catalog=candidate_catalog,
            run_id=run_id
        )
        
        with open(out_dir / "knowledge_graph.json", "w") as f:
            f.write(knowledge_graph.model_dump_json(indent=2))
            
        with open(out_dir / "graph_statistics.json", "w") as f:
            f.write(graph_statistics.model_dump_json(indent=2))
            
        print("13. Graph Centrality Engine (Phase 3.6)...")
        centrality_catalog = self.centrality.process(knowledge_graph, run_id)
        with open(out_dir / "graph_centrality.json", "w") as f:
            f.write(centrality_catalog.model_dump_json(indent=2))
            
        print("--- PHASE 4 ---")
        print("14. Job Intelligence Engine...")
        
        # Load sample jobs
        import os
        job_file = Path("data/sample_job_descriptions.json")
        jobs = []
        if job_file.exists():
            with open(job_file, "r") as f:
                jobs_data = json.load(f)
                jobs = [JobDescription(**j) for j in jobs_data]
        else:
            print(f"Warning: {job_file} not found. Running Phase 4 with empty jobs list.")
            
        job_catalog = self.job.process(jobs, knowledge_graph, run_id)
        with open(out_dir / "job_intelligence_catalog.json", "w") as f:
            f.write(job_catalog.model_dump_json(indent=2))
            
        print("--- PHASE 5 ---")
        print("15. Candidate-Job Alignment Engine...")
        alignment_catalog = self.alignment.process(
            candidate_catalog=candidate_catalog,
            job_catalog=job_catalog,
            knowledge_graph=knowledge_graph,
            centrality_catalog=centrality_catalog,
            run_id=run_id
        )
        with open(out_dir / "candidate_job_alignment_catalog.json", "w") as f:
            f.write(alignment_catalog.model_dump_json(indent=2))
            
        print("--- PHASE 6 ---")
        print("16. Scoring Intelligence Engine...")
        scoring_catalog = self.scoring.process(
            alignment_catalog=alignment_catalog,
            run_id=run_id
        )
        with open(out_dir / "candidate_job_scoring_catalog.json", "w") as f:
            f.write(scoring_catalog.model_dump_json(indent=2))
            
        print("--- PHASE 7 ---")
        print("17. Ranking Policy Engine...")
        ranking_policy = RankingPolicy(sort_order="DESC", max_results=100)
        ranked_catalog = self.ranking.process(
            scoring_catalog=scoring_catalog,
            policy=ranking_policy,
            run_id=run_id
        )
        with open(out_dir / "ranked_candidate_catalog.json", "w") as f:
            f.write(ranked_catalog.model_dump_json(indent=2))
            
        print("Done!")
