import uuid
from collections import defaultdict
from typing import Dict
from src.contracts import KnowledgeGraph, ArtifactMetadata, Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel, EdgeType, NodeType
from src.contracts.centrality import TopGraphEntity, EntityCentralityCatalog

class GraphCentralityEngine:
    def process(self, kg: KnowledgeGraph, run_id: uuid.UUID) -> EntityCentralityCatalog:
        degrees: Dict[str, int] = defaultdict(int)
        relationships: Dict[str, int] = defaultdict(int)
        candidates: Dict[str, int] = defaultdict(int)
        
        # Parse edges
        for e in kg.edges:
            src = e.source_node_id
            tgt = e.target_node_id
            
            degrees[src] += 1
            degrees[tgt] += 1
            
            if e.edge_type == EdgeType.RELATED_TO:
                relationships[src] += 1
                relationships[tgt] += 1
            elif e.edge_type == EdgeType.POSSESSES_ENTITY:
                # Target is usually the entity, source is candidate
                candidates[tgt] += 1
        
        entities = []
        max_degree = max(degrees.values()) if degrees else 1
        
        for n in kg.nodes:
            if n.node_type in [NodeType.SKILL, NodeType.COMPANY, NodeType.CERTIFICATION, NodeType.LANGUAGE, NodeType.ROLE, NodeType.EDUCATION]:
                d = degrees[n.node_id]
                entities.append(TopGraphEntity(
                    entity_id=n.node_id,
                    entity_type=n.node_type.value,
                    label=n.label,
                    degree=d,
                    normalized_degree=d / max_degree,
                    relationship_count=relationships[n.node_id],
                    connected_candidate_count=candidates[n.node_id]
                ))
                
        # Sort and take top 50
        entities.sort(key=lambda x: x.degree, reverse=True)
        top_50 = tuple(entities[:50])
        
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.ENTITY_CENTRALITY_CATALOG,
            producer_module="centrality_engine",
            pipeline_run_id=run_id
        )
        conf = Confidence(
            confidence_score=1.0,
            confidence_level=ConfidenceLevel.HIGH,
            confidence_method="graph_analytics",
            confidence_explanation="Topological metric extraction"
        )
        
        return EntityCentralityCatalog(
            metadata=meta,
            confidence=conf,
            top_entities=top_50
        )
