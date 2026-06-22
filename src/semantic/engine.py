import uuid
from src.contracts.ingestion import DatasetRecord
from src.contracts.schema import SchemaGraph
from src.contracts.metadata import ArtifactMetadata
from src.contracts.confidence import Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.semantic import SemanticConcept, SemanticCatalog

class SemanticEngine:
    def process(self, records: list[DatasetRecord], schema: SchemaGraph, run_id: uuid.UUID) -> SemanticCatalog:
        from src.semantic.domain_taxonomy import DOMAIN_CONCEPTS
        
        concepts = []
        
        # We also need to extract from actual data to find value-level concepts
        # So we iterate over the schema fields, but to get values, we need the records.
        # But this engine might just declare schema-level concepts, or does it do record-level?
        # A SemanticCatalog typically holds global concepts, but if we want it to map to records,
        # we actually just need to discover the concepts present in the dataset.
        
        discovered_domains = set()
        
        for r in records:
            payload = r.raw_payload
            
            import collections.abc
            
            def extract_domains(obj: any):
                if isinstance(obj, collections.abc.Mapping):
                    for v in obj.values():
                        extract_domains(v)
                elif isinstance(obj, (list, tuple, set)):
                    for item in obj:
                        extract_domains(item)
                elif isinstance(obj, str):
                    val = obj.lower()
                    for domain, keywords in DOMAIN_CONCEPTS.items():
                        if any(kw.lower() == val for kw in keywords) or any(kw.lower() in val.split() for kw in keywords):
                            discovered_domains.add(domain)
            
            extract_domains(payload)
            
        for domain in discovered_domains:
            concepts.append(SemanticConcept(
                field_path="dataset",
                concept_name=domain,
                concept_type="inferred_domain"
            ))

        for field in schema.fields:
            name = field.field_name.lower()
            concept_name = "unknown"
            if "skill" in name:
                concept_name = "skills"
            elif "education" in name:
                concept_name = "education"
            elif "language" in name:
                concept_name = "language"
            elif "career" in name or "history" in name or "experience" in name:
                concept_name = "experience"
            elif "cert" in name:
                concept_name = "certification"
            elif "employer" in name or "company" in name:
                concept_name = "employer"
            elif "role" in name or "title" in name:
                concept_name = "job role"
            elif "email" in name:
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
