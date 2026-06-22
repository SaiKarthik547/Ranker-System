import uuid
from src.contracts.ingestion import DatasetRecord
from src.contracts.schema import SchemaGraph
from src.contracts.metadata import ArtifactMetadata
from src.contracts.confidence import Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.semantic import SemanticConcept, SemanticCatalog

class SemanticEngine:
    def process(self, records: list[DatasetRecord], schema: SchemaGraph, run_id: uuid.UUID) -> SemanticCatalog:
        concepts = []
        for field in schema.fields:
            name = field.field_name.lower()
            concept_name = "unknown"
            if "email" in name:
                concept_name = "email"
            elif "phone" in name:
                concept_name = "phone"
            elif "name" in name:
                concept_name = "person_name"
            elif "address" in name or "city" in name:
                concept_name = "location"
            elif field.is_identifier:
                concept_name = "identifier"
                
            if concept_name != "unknown":
                concepts.append(SemanticConcept(
                    field_path=field.field_name,
                    concept_name=concept_name,
                    concept_type="inferred"
                ))
        
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.SEMANTIC_CATALOG,
            producer_module="semantic_engine",
            pipeline_run_id=run_id,
        )
        conf = Confidence(
            confidence_score=0.8, 
            confidence_level=ConfidenceLevel.HIGH, 
            confidence_method="heuristic", 
            confidence_explanation="regex column names"
        )
        return SemanticCatalog(
            metadata=meta,
            confidence=conf,
            concepts=tuple(concepts)
        )
