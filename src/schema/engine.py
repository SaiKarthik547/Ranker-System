import uuid
from src.contracts import DatasetRecord, SchemaGraph, SchemaField, ArtifactMetadata, Confidence, Evidence
from src.contracts.enums import ArtifactType, FieldType, ConfidenceLevel

class SchemaDiscoveryEngine:
    def process(self, records: list[DatasetRecord], run_id: uuid.UUID) -> SchemaGraph:
        fields = []
        if records:
            sample_rec = records[0].raw_payload
            for k, v in sample_rec.items():
                name_lower = k.lower()
                is_ident = (
                    name_lower == "id"
                    or name_lower.endswith("_id")
                    or name_lower.startswith("id_")
                )
                f = SchemaField(
                    field_name=k,
                    field_path=k,
                    data_type=FieldType.STRING,
                    nullable=True,
                    is_identifier=is_ident
                )
                fields.append(f)
        
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.SCHEMA_GRAPH,
            producer_module="schema_engine",
            pipeline_run_id=run_id,
        )
        conf = Confidence(
            confidence_score=1.0, 
            confidence_level=ConfidenceLevel.HIGH, 
            confidence_method="heuristic", 
            confidence_explanation="csv parsing"
        )
        return SchemaGraph(
            metadata=meta,
            confidence=conf,
            fields=tuple(fields),
            record_count=len(records),
            nesting_depth=1
        )
