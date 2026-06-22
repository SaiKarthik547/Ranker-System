import uuid
from pydantic import Field
from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.types import ArtifactId
from src.contracts.enums import NodeType, EdgeType
from src.contracts.evidence import Evidence
from src.contracts.confidence import Confidence

class GraphNode(BaseContract):
    node_id: str
    node_type: NodeType
    label: str
    source_artifact_id: str | None = None
    properties: tuple[tuple[str, str | int | float | bool], ...] = Field(default_factory=tuple)

class GraphEdge(BaseContract):
    edge_id: ArtifactId = Field(default_factory=uuid.uuid4)
    source_node_id: str
    target_node_id: str
    edge_type: EdgeType
    weight: float = Field(ge=0.0, le=1.0, default=1.0)
    evidence: tuple[Evidence, ...] = Field(default_factory=tuple)
    confidence: Confidence

class GraphStatistics(BaseContract):
    total_nodes: int = 0
    total_edges: int = 0
    density: float = 0.0
    connected_components: int = 0
    largest_component_size: int = 0
    average_candidate_degree: float = 0.0
    average_entity_degree: float = 0.0
    node_type_counts: tuple[tuple[str, int], ...] = Field(default_factory=tuple)
    edge_type_counts: tuple[tuple[str, int], ...] = Field(default_factory=tuple)

class KnowledgeGraph(IntelligenceArtifact):
    graph_id: ArtifactId = Field(default_factory=uuid.uuid4)
    node_count: int = 0
    edge_count: int = 0
    nodes: tuple[GraphNode, ...] = Field(default_factory=tuple)
    edges: tuple[GraphEdge, ...] = Field(default_factory=tuple)
