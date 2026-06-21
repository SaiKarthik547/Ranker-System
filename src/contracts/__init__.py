"""
Data Contracts Package.
Defines all the shared Pydantic models and structures across the system.
"""

from src.contracts.base import BaseArtifact, BaseContract, IntelligenceArtifact
from src.contracts.confidence import Confidence
from src.contracts.evidence import Evidence
from src.contracts.ingestion import DatasetRecord
from src.contracts.metadata import ArtifactMetadata
from src.contracts.profiling import ProfileMetric, ProfileReport
from src.contracts.schema import SchemaField, SchemaGraph

# Resolve forward references natively to avoid runtime evaluation errors
ArtifactMetadata.model_rebuild()
Evidence.model_rebuild()
BaseArtifact.model_rebuild()
IntelligenceArtifact.model_rebuild()
DatasetRecord.model_rebuild()
SchemaGraph.model_rebuild()
ProfileReport.model_rebuild()

__all__ = [
    "BaseContract",
    "BaseArtifact",
    "IntelligenceArtifact",
    "Confidence",
    "Evidence",
    "ArtifactMetadata",
    "DatasetRecord",
    "SchemaField",
    "SchemaGraph",
    "ProfileMetric",
    "ProfileReport",
]
