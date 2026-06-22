import uuid
from collections.abc import Mapping
from typing import Any
from src.contracts import DatasetRecord, ArtifactMetadata, Confidence, SchemaGraph, SemanticCatalog
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.entities import Entity, EntityCatalog

class EntityExtractionEngine:
    def process(self, records: list[DatasetRecord], schema: SchemaGraph, semantic: SemanticCatalog, run_id: uuid.UUID) -> EntityCatalog:
        entities = []
        
        # Load skill dictionary from Candidates for intersection (if available from semantic catalog or graph)
        # But we don't have direct access to Candidate Entity Catalog here. We must extract entities organically.
        import re
        
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
                
                # JD Unstructured Text Extraction
                if path.endswith("document_text") and isinstance(obj, str):
                    # 1. Location Entities
                    location_matches = re.finditer(r'(?:Location|Work Location|Office)[:\s]+([^,\n]+)', obj, re.IGNORECASE)
                    for m in location_matches:
                        loc = m.group(1).strip()
                        if 0 < len(loc) < 50:
                            entities.append(Entity(entity_name=loc, entity_type="LOCATION", source_record_id=record_id, source_field_path="document_text.location"))
                    
                    for loc in ["Remote", "Hybrid", "Onsite", "Pune", "Noida", "Bangalore", "Hyderabad", "Chennai", "Delhi", "Mumbai"]:
                        if re.search(r'\b' + loc + r'\b', obj, re.IGNORECASE):
                            entities.append(Entity(entity_name=loc, entity_type="LOCATION", source_record_id=record_id, source_field_path="document_text.location"))
                            
                    # 2. Employment Type
                    for emp in ["Contract", "Full-time", "Internship", "Part-time"]:
                        if re.search(r'\b' + emp + r'\b', obj, re.IGNORECASE):
                            entities.append(Entity(entity_name=emp, entity_type="ROLE", source_record_id=record_id, source_field_path="document_text.employment_type"))
                            
                    # 3. Seniority
                    for sen in ["Junior", "Mid", "Senior", "Lead", "Principal", "Architect"]:
                        if re.search(r'\b' + sen + r'\b', obj, re.IGNORECASE):
                            entities.append(Entity(entity_name=sen, entity_type="ROLE", source_record_id=record_id, source_field_path="document_text.seniority"))
                            
                    # 4. Notice Period
                    for np in ["Immediate joiner", "15 days", "30 days", "60 days", "90 days"]:
                        if re.search(r'\b' + np.replace(" ", r'\s+') + r'\b', obj, re.IGNORECASE):
                            entities.append(Entity(entity_name=np, entity_type="ROLE", source_record_id=record_id, source_field_path="document_text.notice_period"))
                            
                    # 5. Common Tech Skills (Deterministic Rules)
                    # We will organically extract known tech keywords.
                    tech_keywords = ["Python", "Java", "C++", "AWS", "GCP", "Azure", "React", "Node", "SQL", "NoSQL", 
                                     "Pinecone", "Weaviate", "Milvus", "FAISS", "Qdrant", "Elasticsearch", "OpenSearch",
                                     "LangChain", "OpenAI", "LLM", "RAG", "BGE", "E5", "Sentence-Transformers", 
                                     "NDCG", "MRR", "MAP", "A/B test", "LoRA", "QLoRA", "PEFT", "XGBoost"]
                    for tech in tech_keywords:
                        if re.search(r'\b' + re.escape(tech) + r'\b', obj, re.IGNORECASE):
                            entities.append(Entity(entity_name=tech, entity_type="SKILL", source_record_id=record_id, source_field_path="document_text.skill"))
                            
                    # 6. Disqualifier Companies (Explicitly from text)
                    if re.search(r'consulting firms\s*\((.*?)\)', obj, re.IGNORECASE):
                        match = re.search(r'consulting firms\s*\((.*?)\)', obj, re.IGNORECASE)
                        comps = [c.strip() for c in match.group(1).split(',')]
                        for c in comps:
                            if c.lower() != 'etc.':
                                entities.append(Entity(entity_name=c, entity_type="COMPANY", source_record_id=record_id, source_field_path="document_text.disqualifier_company"))
            
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
