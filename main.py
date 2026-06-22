import sys
import os

# Ensure src module is discoverable if run from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.orchestration.pipeline import PipelineOrchestrator

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <candidates_file> <job_description_file>")
        sys.exit(1)
        
    pipeline = PipelineOrchestrator()
    pipeline.run(sys.argv[1], sys.argv[2])
