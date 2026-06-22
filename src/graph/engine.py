import uuid
from typing import Dict, Set
from src.contracts import (
    ArtifactMetadata, Confidence, Evidence,
    EntityCatalog, RelationshipCatalog, PatternCatalog, ClusterCatalog, AnomalyCatalog, CandidateIntelligenceCatalog,
    GraphNode, GraphEdge, GraphStatistics, KnowledgeGraph
)
from src.contracts.enums import ArtifactType, ConfidenceLevel, NodeType, EdgeType

class KnowledgeGraphEngine:
    def process(
        self,
        entity_catalog: EntityCatalog,
        relationship_catalog: RelationshipCatalog,
        pattern_catalog: PatternCatalog,
        cluster_catalog: ClusterCatalog,
        anomaly_catalog: AnomalyCatalog,
        candidate_catalog: CandidateIntelligenceCatalog,
        run_id: uuid.UUID
    ) -> tuple[KnowledgeGraph, GraphStatistics]:
        
        nodes: Dict[str, GraphNode] = {}
        edges: list[GraphEdge] = []
        
        # Helper to add nodes safely
        def add_node(n: GraphNode) -> None:
            if n.node_id not in nodes:
                nodes[n.node_id] = n

        # 1. Add Candidates from CandidateIntelligenceCatalog
        for profile in candidate_catalog.profiles:
            n = GraphNode(
                node_id=f"candidate_{profile.candidate_id}",
                node_type=NodeType.CANDIDATE,
                label=f"Candidate {profile.candidate_id}",
                source_artifact_id=str(profile.candidate_id),
                properties=(
                    ("profile_quality_score", profile.profile_quality_score),
                    ("completeness_score", profile.completeness_score)
                )
            )
            add_node(n)
            
        # 2. Add Entities from EntityCatalog & Link to Candidates
        # Based on Rule 2, edges originate from artifacts.
        # entity_catalog has entities that contain source_record_id!
        for ent in entity_catalog.entities:
            # We add the entity as a node
            ent_id = f"entity_{ent.entity_name}"
            node_type = NodeType.SKILL
            if ent.entity_type == "COMPANY": node_type = NodeType.COMPANY
            elif ent.entity_type == "CERTIFICATION": node_type = NodeType.CERTIFICATION
            elif ent.entity_type == "LANGUAGE": node_type = NodeType.LANGUAGE
            
            n = GraphNode(
                node_id=ent_id,
                node_type=node_type,
                label=ent.entity_name,
                source_artifact_id=str(ent.entity_id),
                properties=()
            )
            add_node(n)
            
            # Edge: Candidate -> Entity
            if ent.source_record_id:
                cand_id = f"candidate_{ent.source_record_id}"
                # We construct evidence pointing to the entity artifact
                ev = Evidence(
                    evidence_type="entity_extraction",
                    source_artifact=ent.entity_id,
                    source_location=str(ent.source_field_path),
                    source_value=str(ent.entity_name),
                    reasoning=f"Extracted {ent.entity_name} from {ent.source_field_path}"
                )
                conf = Confidence(
                    confidence_score=0.9,
                    confidence_level=ConfidenceLevel.HIGH,
                    confidence_method="extraction",
                    confidence_explanation="Direct phase 1 extraction"
                )
                e = GraphEdge(
                    source_node_id=cand_id,
                    target_node_id=ent_id,
                    edge_type=EdgeType.POSSESSES_ENTITY,
                    weight=1.0,
                    evidence=(ev,),
                    confidence=conf
                )
                edges.append(e)

        # 3. Add Relationships from RelationshipCatalog
        for rel in relationship_catalog.relationships:
            # Assumes entities in relationships match entity names
            src_id = f"entity_{rel.source_entity}"
            tgt_id = f"entity_{rel.target_entity}"
            if src_id in nodes and tgt_id in nodes:
                ev = Evidence(
                    evidence_type="relationship_discovery",
                    source_artifact=rel.relationship_id,
                    source_value=str(rel.relationship_type),
                    reasoning=rel.relationship_type
                )
                conf = Confidence(
                    confidence_score=0.8,
                    confidence_level=ConfidenceLevel.MEDIUM,
                    confidence_method="co-occurrence",
                    confidence_explanation="Relationship Catalog"
                )
                try:
                    e_type = EdgeType(rel.relationship_type)
                except ValueError:
                    e_type = EdgeType.RELATED_TO
                
                e = GraphEdge(
                    source_node_id=src_id,
                    target_node_id=tgt_id,
                    edge_type=e_type,
                    weight=rel.weight,
                    evidence=(ev,),
                    confidence=conf
                )
                edges.append(e)

        # 4. Add Patterns, Clusters, Anomalies...
        # For simplicity in Phase 3, we add nodes for patterns.
        for pat in pattern_catalog.patterns:
            n = GraphNode(
                node_id=f"pattern_{pat.pattern_id}",
                node_type=NodeType.PATTERN,
                label=pat.pattern_name,
                source_artifact_id=str(pat.pattern_id),
                properties=(("frequency", pat.frequency),)
            )
            add_node(n)
            
        for cl in cluster_catalog.clusters:
            n = GraphNode(
                node_id=f"cluster_{cl.cluster_id}",
                node_type=NodeType.CLUSTER,
                label=cl.cluster_name,
                source_artifact_id=str(cl.cluster_id),
                properties=(("size", cl.size),)
            )
            add_node(n)

        for an in anomaly_catalog.anomalies:
            n = GraphNode(
                node_id=f"anomaly_{an.anomaly_id}",
                node_type=NodeType.ANOMALY,
                label=an.description,
                source_artifact_id=str(an.anomaly_id),
                properties=(("severity", an.severity),)
            )
            add_node(n)

        # Validate Referential Integrity
        node_ids = set(nodes.keys())
        valid_edges = []
        for e in edges:
            if e.source_node_id in node_ids and e.target_node_id in node_ids:
                valid_edges.append(e)
            else:
                raise ValueError(f"Referential integrity failed: Edge connects missing nodes. Src: {e.source_node_id}, Tgt: {e.target_node_id}")

        # Compute connected components using simple BFS
        visited: Set[str] = set()
        adj_list: Dict[str, list[str]] = {nid: [] for nid in node_ids}
        for e in valid_edges:
            adj_list[e.source_node_id].append(e.target_node_id)
            adj_list[e.target_node_id].append(e.source_node_id)

        components = 0
        largest_component_size = 0
        for nid in node_ids:
            if nid not in visited:
                components += 1
                queue = [nid]
                visited.add(nid)
                curr_size = 0
                while queue:
                    curr = queue.pop(0)
                    curr_size += 1
                    for neighbor in adj_list[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                if curr_size > largest_component_size:
                    largest_component_size = curr_size

        # Compute stats
        num_nodes = len(nodes)
        num_edges = len(valid_edges)
        density = 0.0
        if num_nodes > 1:
            density = num_edges / (num_nodes * (num_nodes - 1))

        # Node type counts
        nt_counts: Dict[str, int] = {}
        for n in nodes.values():
            nt_counts[n.node_type.value] = nt_counts.get(n.node_type.value, 0) + 1
            
        # Edge type counts
        et_counts: Dict[str, int] = {}
        for e in valid_edges:
            et_counts[e.edge_type.value] = et_counts.get(e.edge_type.value, 0) + 1

        # Degrees
        candidate_nodes = [nid for nid, n in nodes.items() if n.node_type == NodeType.CANDIDATE]
        entity_nodes = [nid for nid, n in nodes.items() if n.node_type in [NodeType.SKILL, NodeType.COMPANY, NodeType.CERTIFICATION, NodeType.LANGUAGE, NodeType.ROLE, NodeType.EDUCATION]]

        candidate_degrees = sum(len(adj_list[nid]) for nid in candidate_nodes)
        entity_degrees = sum(len(adj_list[nid]) for nid in entity_nodes)

        avg_candidate_degree = candidate_degrees / len(candidate_nodes) if candidate_nodes else 0.0
        avg_entity_degree = entity_degrees / len(entity_nodes) if entity_nodes else 0.0

        stats = GraphStatistics(
            total_nodes=num_nodes,
            total_edges=num_edges,
            density=density,
            connected_components=components,
            largest_component_size=largest_component_size,
            average_candidate_degree=avg_candidate_degree,
            average_entity_degree=avg_entity_degree,
            node_type_counts=tuple((k, v) for k, v in nt_counts.items()),
            edge_type_counts=tuple((k, v) for k, v in et_counts.items())
        )

        meta = ArtifactMetadata(
            artifact_type=ArtifactType.KNOWLEDGE_GRAPH,
            producer_module="graph_engine",
            pipeline_run_id=run_id
        )
        conf = Confidence(
            confidence_score=0.9,
            confidence_level=ConfidenceLevel.HIGH,
            confidence_method="graph_assembly",
            confidence_explanation="Referentially validated from catalogs"
        )

        kg = KnowledgeGraph(
            metadata=meta,
            confidence=conf,
            node_count=num_nodes,
            edge_count=num_edges,
            nodes=tuple(nodes.values()),
            edges=tuple(valid_edges)
        )

        return kg, stats
