import json
import csv
from pathlib import Path

def export_ranked_csv():
    # Input/Output paths
    in_path = Path("artifacts/ranked_candidate_catalog.json")
    out_dir = Path("Result")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "top_100_recommended_candidates.csv"
    
    if not in_path.exists():
        print(f"Error: {in_path} not found. Please run main.py first.")
        return
        
    with open(in_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    candidates = catalog.get("ranked_candidates", [])
    
    if not candidates:
        print("No candidates found in catalog.")
        return
        
    # Write to CSV
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        # Define columns we want in the CSV
        fieldnames = ["candidate_id", "rank", "score", "reasoning"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for c in candidates:
            # Synthesize human-readable reasoning string from evidence
            reasoning_parts = []
            
            evidence = c.get("evidence", [])
            req_skills = sum(1 for e in evidence if e.get("evidence_type") == "REQUIRED_SKILL_MATCH")
            pref_skills = sum(1 for e in evidence if e.get("evidence_type") == "PREFERRED_SKILL_MATCH")
            
            if req_skills > 0:
                skill_word = "skills" if req_skills > 1 else "skill"
                reasoning_parts.append(f"{req_skills} required {skill_word} matched")
            if pref_skills > 0:
                skill_word = "skills" if pref_skills > 1 else "skill"
                reasoning_parts.append(f"{pref_skills} preferred {skill_word} matched")
                
            top_factors = c.get("top_factors", [])
            has_centrality = any("CENTRALITY" in f.get("factor", "") and f.get("contribution", 0) >= 0.01 for f in top_factors)
            if has_centrality:
                reasoning_parts.append("high-value niche skill profile")
                
            reasoning = "; ".join(reasoning_parts) if reasoning_parts else "Baseline structural fit"
            
            # Explicitly flag disqualifiers for negative scores
            if c.get("final_score", 0) < 0:
                reasoning = "Failed disqualifier check (" + reasoning + ")"
            
            row = {
                "candidate_id": c.get("candidate_id"),
                "rank": c.get("rank"),
                "score": f"{c.get('final_score', 0):.4f}",
                "reasoning": reasoning
            }
            writer.writerow(row)
            
    print(f"Successfully exported {len(candidates)} candidates to {out_path}")

if __name__ == "__main__":
    export_ranked_csv()
