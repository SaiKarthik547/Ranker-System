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
        fieldnames = [
            "rank", 
            "candidate_id", 
            "job_id", 
            "final_score", 
            "top_factors", 
            "factor_contributions"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for c in candidates:
            row = {
                "rank": c.get("rank"),
                "candidate_id": c.get("candidate_id"),
                "job_id": c.get("job_id"),
                "final_score": f"{c.get('final_score', 0):.4f}",
                # Join the tuples into comma-separated strings for CSV readability
                "top_factors": " | ".join(c.get("top_factors", [])),
                "factor_contributions": " | ".join([f"{val:.3f}" for val in c.get("factor_contributions", [])])
            }
            writer.writerow(row)
            
    print(f"Successfully exported {len(candidates)} candidates to {out_path}")

if __name__ == "__main__":
    export_ranked_csv()
