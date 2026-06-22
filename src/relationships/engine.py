import uuid
import itertools
from collections import defaultdict
from src.contracts import DatasetRecord, ArtifactMetadata, Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.entities import EntityCatalog
from src.contracts.relationships import Relationship, RelationshipCatalog

class RelationshipDiscoveryEngine:
    def process(self, records: list[DatasetRecord], entities: EntityCatalog, run_id: uuid.UUID) -> RelationshipCatalog:
        # Group entity names by candidate ID
        candidate_entities: dict[str, set[str]] = defaultdict(set)
        
        for ent in entities.entities:
            # ent.source_record_id maps to candidate
            if ent.source_record_id:
                candidate_entities[ent.source_record_id].add(ent.entity_name)
                
        # Count pairwise co-occurrences
        pair_counts: dict[tuple[str, str], int] = defaultdict(int)
        
        for cid, ent_set in candidate_entities.items():
            # Generate all pairs within this candidate
            # Sorting ensures (A, B) is treated identical to (B, A)
            pairs = itertools.combinations(sorted(list(ent_set)), 2)
            for p in pairs:
                pair_counts[p] += 1
                
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
                        relationship_type="RELATED_TO",
                        weight=weight
                    ))
            
        return RelationshipCatalog(
            metadata=meta,
            confidence=conf,
            relationships=tuple(rels)
        )
