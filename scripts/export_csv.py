import json
import csv
from pathlib import Path

def export_ranked_csv():
    # Input/Output paths
    in_path = Path("artifacts/ranked_candidate_catalog.json")
    out_path = Path("artifacts/top_100_recommended_candidates.csv")
    
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
            # Synthesize reasoning string from top factors
            reasoning_parts = []
            top_factors = c.get("top_factors", [])
            factor_contributions = c.get("factor_contributions", {})
            
            if top_factors:
                for factor in top_factors:
                    if factor in factor_contributions:
                        reasoning_parts.append(f"{factor}: {factor_contributions[factor]:.2f}")
            reasoning = " | ".join(reasoning_parts) if reasoning_parts else "Score produced by core algorithms."
            
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
