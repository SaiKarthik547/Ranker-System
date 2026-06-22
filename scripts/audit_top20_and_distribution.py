import json
import statistics
from pathlib import Path

def run_audit():
    with open("artifacts/ranked_candidate_catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    candidates = catalog.get("ranked_candidates", [])
    if not candidates:
        print("No candidates.")
        return
        
    scores = [c.get("final_score", 0.0) for c in candidates]
    
    print("--- PHASE 6: Score Distribution ---")
    print(f"Count: {len(scores)}")
    print(f"Min: {min(scores):.4f}")
    print(f"Max: {max(scores):.4f}")
    print(f"Mean: {statistics.mean(scores):.4f}")
    if len(scores) > 1:
        print(f"Standard Deviation: {statistics.stdev(scores):.4f}")
    
    print("\n--- PHASE 5: Top 20 Candidates Audit ---")
    with open("artifacts/candidate_job_alignment_catalog.json", "r", encoding="utf-8") as f:
        align_catalog = json.load(f)
        
    # Map candidate_id to their alignment
    alignments = {a["candidate_id"]: a for a in align_catalog.get("alignments", [])}
    
    for i, c in enumerate(candidates[:20]):
        cid = c.get("candidate_id")
        score = c.get("final_score", 0.0)
        a = alignments.get(cid, {})
        
        signals = a.get("alignment_signals", [])
        req_skills = sum(1 for s in signals if s["signal_name"] == "REQUIRED_SKILL_MET")
        pref_skills = sum(1 for s in signals if s["signal_name"] == "PREFERRED_SKILL_MET")
        disqualifiers = sum(1 for s in signals if s["signal_name"] == "DISQUALIFIER_COMPANY_MATCH")
        
        print(f"Rank {i+1}: Candidate {cid} | Score: {score:.4f} | ReqSkills: {req_skills} | PrefSkills: {pref_skills} | Disqualifiers: {disqualifiers}")

if __name__ == "__main__":
    run_audit()
