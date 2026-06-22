import uuid
import json
import re
from pathlib import Path
from src.contracts import DatasetRecord, ArtifactMetadata, Confidence
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.entities import EntityCatalog
from src.contracts.job import JobProfile, JobRequirement, JobSignal, JobIntelligenceCatalog

class JobIntelligenceEngine:
    def process(self, jd_record: DatasetRecord, jd_entity_catalog: EntityCatalog, run_id: uuid.UUID) -> JobIntelligenceCatalog:
        requirements = []
        signals = []
        
        text = jd_record.raw_payload.get("document_text", "")
        
        # 1. Title/Profile
        title_match = re.search(r'Job Description:\s*(.*)', text, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        job_id = "JOB_" + str(uuid.uuid4())[:8]
        
        profiles = [JobProfile(job_id=job_id, title=title)]
        
        # Audit dictionary
        audit = {
            "skills": [],
            "required_skills": [],
            "preferred_skills": [],
            "experience_years": 0,
            "locations": [],
            "disqualifiers": []
        }
        
        # 2. Extract Experience
        exp_match = re.search(r'(\d+)\s*(?:-|to)\s*(\d+)\s*years', text, re.IGNORECASE)
        if exp_match:
            exp_years = int(exp_match.group(1))
            audit["experience_years"] = exp_years
            requirements.append(JobRequirement(
                requirement_type="REQUIRES_EXPERIENCE",
                target_value=str(exp_years),
                severity="MUST_HAVE"
            ))
            
        # 3. Process Entities
        def get_source_text(val, text):
            # Find the sentence containing the value
            idx = text.lower().find(val.lower())
            if idx == -1: return ""
            start = max(0, text.rfind('\n', 0, idx))
            end = text.find('\n', idx)
            if end == -1: end = len(text)
            return text[start:end].strip()
            
        for ent in jd_entity_catalog.entities:
            val = ent.entity_name
            path = ent.source_field_path
            src_text = get_source_text(val, text)
            
            if "location" in path:
                if val not in audit["locations"]:
                    audit["locations"].append(val)
                    requirements.append(JobRequirement(
                        requirement_type="LOCATION_REQUIREMENT",
                        target_value=val,
                        severity="MUST_HAVE",
                        source_text=src_text
                    ))
            elif "employment_type" in path:
                requirements.append(JobRequirement(
                    requirement_type="EMPLOYMENT_TYPE",
                    target_value=val,
                    severity="MUST_HAVE",
                    source_text=src_text
                ))
            elif "seniority" in path:
                requirements.append(JobRequirement(
                    requirement_type="REQUIRES_SENIORITY",
                    target_value=val,
                    severity="MUST_HAVE",
                    source_text=src_text
                ))
            elif "notice_period" in path:
                requirements.append(JobRequirement(
                    requirement_type="NOTICE_PERIOD_REQUIREMENT",
                    target_value=val,
                    severity="PREFERS",
                    source_text=src_text
                ))
            elif "disqualifier_company" in path:
                audit["disqualifiers"].append(val)
                requirements.append(JobRequirement(
                    requirement_type="DISQUALIFIER_COMPANY",
                    target_value=val,
                    severity="MUST_HAVE", # Handled in alignment
                    source_text=src_text
                ))
            elif "skill" in path:
                if val not in audit["skills"]:
                    audit["skills"].append(val)
                    
                    req_idx = text.lower().find("things you absolutely need")
                    pref_idx = text.lower().find("things we'd like you to have")
                    skill_idx = text.find(val)
                    
                    is_preferred = False
                    if pref_idx != -1 and skill_idx > pref_idx:
                        is_preferred = True
                        
                    if is_preferred:
                        audit["preferred_skills"].append(val)
                        requirements.append(JobRequirement(
                            requirement_type="PREFERS_SKILL",
                            target_value=val,
                            severity="NICE_TO_HAVE",
                            source_text=src_text
                        ))
                    else:
                        audit["required_skills"].append(val)
                        requirements.append(JobRequirement(
                            requirement_type="REQUIRES_SKILL",
                            target_value=val,
                            severity="MUST_HAVE",
                            source_text=src_text
                        ))
                        
        # Write Audit
        out_dir = Path("artifacts")
        out_dir.mkdir(exist_ok=True)
        with open(out_dir / "job_extraction_audit.json", "w") as f:
            json.dump(audit, f, indent=2)
            
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.JOB_INTELLIGENCE_CATALOG,
            producer_module="job_engine",
            pipeline_run_id=run_id
        )
        conf = Confidence(
            confidence_score=0.9,
            confidence_level=ConfidenceLevel.HIGH,
            confidence_method="heuristic",
            confidence_explanation="Job description deterministic extraction"
        )
        
        return JobIntelligenceCatalog(
            metadata=meta,
            confidence=conf,
            profiles=tuple(profiles),
            requirements=tuple(requirements),
            signals=tuple(signals)
        )
