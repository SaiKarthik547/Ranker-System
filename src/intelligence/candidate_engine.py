import uuid
from src.contracts import (
    DatasetRecord, ArtifactMetadata, Confidence, SchemaGraph, ProfileReport,
    SemanticCatalog, EntityCatalog, RelationshipCatalog, PatternCatalog,
    ClusterCatalog, AnomalyCatalog
)
from src.contracts.enums import ArtifactType, ConfidenceLevel, CandidateSignalType, SignalCategory
from src.contracts.candidates import CandidateSignal, CandidateProfile, CandidateIntelligenceCatalog
from src.contracts.entities import Entity

class CandidateIntelligenceEngine:
    def process(
        self,
        records: list[DatasetRecord],
        schema_graph: SchemaGraph,
        profile_report: ProfileReport,
        semantic_catalog: SemanticCatalog,
        entity_catalog: EntityCatalog,
        relationship_catalog: RelationshipCatalog,
        pattern_catalog: PatternCatalog,
        cluster_catalog: ClusterCatalog,
        anomaly_catalog: AnomalyCatalog,
        run_id: uuid.UUID
    ) -> CandidateIntelligenceCatalog:
        profiles = []
        all_signals = []
        
        # Discover identifier field dynamically
        id_field = "id"
        for f in schema_graph.fields:
            if f.is_identifier:
                id_field = f.field_path
                break
                
        # Group entities by candidate
        candidate_entities: dict[str, list[Entity]] = {}
        for ent in entity_catalog.entities:
            cid = str(ent.source_record_id)
            if cid not in candidate_entities:
                candidate_entities[cid] = []
            candidate_entities[cid].append(ent)
            
        for r in records:
            payload = r.raw_payload
            cid = str(payload.get(id_field, "UNKNOWN"))
            
            # Fetch entities purely from EntityCatalog provenance
            my_entities = candidate_entities.get(cid, [])
            
            # Reconstruct profile exclusively from generic entities 
            skills = tuple(set(e.entity_name for e in my_entities if e.entity_type == "SKILL"))
            companies = tuple(set(e.entity_name for e in my_entities if e.entity_type == "COMPANY"))
            roles = tuple(set(e.entity_name for e in my_entities if e.entity_type == "GENERAL" and "title" in str(e.source_field_path).lower()))
            certifications = tuple(set(e.entity_name for e in my_entities if e.entity_type == "CERTIFICATION"))
            languages = tuple(set(e.entity_name for e in my_entities if e.entity_type == "LANGUAGE"))
            
            # Signals collection
            strength_sigs = []
            risk_sigs = []
            
            # Heuristics based entirely on inferred entities
            if len(skills) > 10:
                sig = CandidateSignal(
                    signal_name=CandidateSignalType.HIGH_SKILL_DENSITY,
                    signal_type=SignalCategory.STRENGTH,
                    rationale=(f"Candidate possesses {len(skills)} extracted skills.",)
                )
                strength_sigs.append(sig)
                all_signals.append(sig)
                
            if not certifications:
                sig = CandidateSignal(
                    signal_name=CandidateSignalType.MISSING_CERTIFICATIONS,
                    signal_type=SignalCategory.RISK,
                    rationale=("Candidate profile has 0 certifications extracted.",)
                )
                risk_sigs.append(sig)
                all_signals.append(sig)
                
            if not companies:
                sig = CandidateSignal(
                    signal_name=CandidateSignalType.LIMITED_EXPERIENCE,
                    signal_type=SignalCategory.RISK,
                    rationale=("Candidate has no identified company affiliations.",)
                )
                risk_sigs.append(sig)
                all_signals.append(sig)

            # Profile Quality Score based on intelligence depth
            completeness_score = len(my_entities) * 5
            quality_score = min(100.0, float(completeness_score) + min(30.0, len(skills)*2) + (len(strength_sigs)*5))
            
            # Text Summaries
            ident_sum = f"Candidate {cid}."
            skills_sum = f"Candidate holds {len(skills)} inferred skills."
            exp_sum = f"Experienced across {len(companies)} companies."
            edu_sum = f"Education metrics deferred to full graph traversal."
            cert_sum = f"Earned {len(certifications)} professional certifications."
            lang_sum = f"Fluent in {len(languages)} languages."
            career_sum = f"Total identified roles: {len(roles)}."
            intel_sum = f"Overall profile depth is scored at {quality_score:.1f}. Showing {len(strength_sigs)} strengths and {len(risk_sigs)} risks."
            
            # Build Profile
            meta = ArtifactMetadata(
                artifact_type=ArtifactType.CANDIDATE_PROFILE,
                producer_module="candidate_engine",
                pipeline_run_id=run_id,
            )
            conf = Confidence(confidence_score=0.85, confidence_level=ConfidenceLevel.HIGH, confidence_method="graph_inference", confidence_explanation="reconstructed from Phase 1 entity provenance")
            
            profile = CandidateProfile(
                metadata=meta,
                confidence=conf,
                candidate_id=cid,
                skills=skills,
                companies=companies,
                roles=roles,
                certifications=certifications,
                languages=languages,
                identity_summary=ident_sum,
                skills_summary=skills_sum,
                experience_summary=exp_sum,
                education_summary=edu_sum,
                certification_summary=cert_sum,
                language_summary=lang_sum,
                career_progression_summary=career_sum,
                intelligence_summary=intel_sum,
                strength_signals=tuple(strength_sigs),
                risk_signals=tuple(risk_sigs),
                completeness_score=min(100.0, completeness_score),
                profile_quality_score=quality_score
            )
            profiles.append(profile)
            
        cat_meta = ArtifactMetadata(
            artifact_type=ArtifactType.CANDIDATE_CATALOG,
            producer_module="candidate_engine",
            pipeline_run_id=run_id,
        )
        cat_conf = Confidence(confidence_score=1.0, confidence_level=ConfidenceLevel.VERY_HIGH, confidence_method="aggregation", confidence_explanation="rolled up candidates")
        return CandidateIntelligenceCatalog(
            metadata=cat_meta,
            confidence=cat_conf,
            profiles=tuple(profiles),
            all_signals=tuple(all_signals)
        )
