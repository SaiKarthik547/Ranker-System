import uuid
import itertools
from collections import defaultdict
from src.contracts import DatasetRecord, ArtifactMetadata, Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.entities import EntityCatalog
from src.contracts.relationships import Relationship, RelationshipCatalog

class RelationshipDiscoveryEngine:
    def process(self, records: list[DatasetRecord], entities: EntityCatalog, run_id: uuid.UUID) -> RelationshipCatalog:
        VALID_RELATIONSHIP_RULES = {
            ("ROLE", "SKILL"): "ROLE_REQUIRES_SKILL",
            ("SKILL", "ROLE"): "ROLE_REQUIRES_SKILL",
            ("LANGUAGE", "LANGUAGE_PROFICIENCY"): "LANGUAGE_HAS_PROFICIENCY",
            ("LANGUAGE_PROFICIENCY", "LANGUAGE"): "LANGUAGE_HAS_PROFICIENCY",
            ("COMPANY_SIZE", "EMPLOYER"): "COMPANY_SIZE_OF_EMPLOYER",
            ("EMPLOYER", "COMPANY_SIZE"): "COMPANY_SIZE_OF_EMPLOYER",
            ("DEGREE", "SKILL"): "DEGREE_RELATES_TO_SKILL",
            ("SKILL", "DEGREE"): "DEGREE_RELATES_TO_SKILL",
            ("SKILL", "SKILL"): "SKILL_CO_OCCURS_WITH_SKILL"
        }
        
        # Group entity tuples by candidate ID
        candidate_entities: dict[str, set[tuple[str, str]]] = defaultdict(set)
        
        for ent in entities.entities:
            # ent.source_record_id maps to candidate
            if ent.source_record_id:
                candidate_entities[ent.source_record_id].add((ent.entity_name, ent.entity_type))
                
        # Count pairwise co-occurrences of valid types
        pair_counts: dict[tuple[str, str], int] = defaultdict(int)
        pair_types: dict[tuple[str, str], str] = {}
        
        for cid, ent_set in candidate_entities.items():
            # Generate all pairs within this candidate
            # Sorting ensures (A, B) is treated identical to (B, A)
            pairs = itertools.combinations(sorted(list(ent_set), key=lambda x: x[0]), 2)
            for p in pairs:
                src_name, src_type = p[0]
                tgt_name, tgt_type = p[1]
                
                rule = VALID_RELATIONSHIP_RULES.get((src_type, tgt_type))
                if rule:
                    key = (src_name, tgt_name)
                    pair_counts[key] += 1
                    pair_types[key] = rule
                
        rels = []
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.RELATIONSHIP_CATALOG,
            producer_module="relationship_engine",
            pipeline_run_id=run_id,
        )
        conf = Confidence(
            confidence_score=0.85, 
            confidence_level=ConfidenceLevel.HIGH, 
            confidence_method="co-occurrence", 
            confidence_explanation="Pairwise extraction across candidate boundaries"
        )
        
        if pair_counts:
            max_freq = max(pair_counts.values())
            
            for (src, tgt), freq in pair_counts.items():
                if freq >= 2:
                    weight = freq / max_freq
                    rels.append(Relationship(
                        source_entity=src,
                        target_entity=tgt,
                        relationship_type=pair_types[(src, tgt)],
                        weight=weight
                    ))
            
        return RelationshipCatalog(
            metadata=meta,
            confidence=conf,
            relationships=tuple(rels)
        )
