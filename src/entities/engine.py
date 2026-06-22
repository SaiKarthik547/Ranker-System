import uuid
from collections.abc import Mapping
from typing import Any
from src.contracts import DatasetRecord, ArtifactMetadata, Confidence, SchemaGraph, SemanticCatalog
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.entities import Entity, EntityCatalog

class EntityExtractionEngine:
    def process(self, records: list[DatasetRecord], schema: SchemaGraph, semantic: SemanticCatalog, run_id: uuid.UUID) -> EntityCatalog:
        entities = []
        
        # Discover identifier field
        id_field = "id"
        for f in schema.fields:
            if f.is_identifier:
                id_field = f.field_path
                break
                
        # We will extract entities dynamically by looking at semantic types or field structures
        for r in records:
            payload = r.raw_payload
            record_id = str(payload.get(id_field, str(uuid.uuid4())))
            
            def extract_lists(obj: dict[Any, Any] | Mapping[Any, Any] | list[Any] | tuple[Any, ...] | set[Any] | str | int | float | bool | None, path: str = "") -> None:
                if isinstance(obj, Mapping):
                    for k, v in obj.items():
                        extract_lists(v, path + "." + k if path else k)
                elif isinstance(obj, (list, tuple, set)):
                    for item in obj:
                        extract_lists(item, path)
                elif isinstance(obj, str):
                    path_lower = path.lower()
                    e_type = None
                    
                    if "skill" in path_lower and ("name" in path_lower or "skill" in path.split(".")[-1].lower()): e_type = "SKILL"
                    elif "company" in path_lower or "employer" in path_lower: e_type = "COMPANY"
                    elif "cert" in path_lower and "name" in path_lower: e_type = "CERTIFICATION"
                    elif "lang" in path_lower and "language" in path_lower: e_type = "LANGUAGE"
                    elif "institution" in path_lower or "degree" in path_lower or "field_of_study" in path_lower: e_type = "EDUCATION"
                    elif "title" in path_lower or "role" in path_lower: e_type = "ROLE"
                    
                    if e_type and 0 < len(obj.strip()) < 100:
                        ent = Entity(
                            entity_name=obj.strip(),
                            entity_type=e_type,
                            source_record_id=record_id,
                            source_field_path=path
                        )
                        entities.append(ent)
            
            extract_lists(payload)
            
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.ENTITY_CATALOG,
            producer_module="entity_engine",
            pipeline_run_id=run_id,
        )
        conf = Confidence(confidence_score=0.9, confidence_level=ConfidenceLevel.HIGH, confidence_method="heuristic", confidence_explanation="dynamic extraction")
        return EntityCatalog(
            metadata=meta,
            confidence=conf,
            entities=tuple(entities)
        )
