import csv
import json
import uuid
from pathlib import Path

from src.contracts import DatasetRecord, ArtifactMetadata
from src.contracts.enums import ArtifactType, SourceType


class IngestionEngine:
    def process(self, file_path: str, run_id: uuid.UUID, limit: int = 100) -> list[DatasetRecord]:
        path = Path(file_path)
        records = []
        
        if path.suffix == ".csv":
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if limit and i >= limit:
                        break
                    meta = ArtifactMetadata(
                        artifact_type=ArtifactType.DATASET_RECORD,
                        producer_module="ingestion_engine",
                        pipeline_run_id=run_id,
                    )
                    rec = DatasetRecord(
                        metadata=meta,
                        source_type=SourceType.CSV,
                        source_uri=path.name,
                        raw_payload=dict(row),
                    )
                    records.append(rec)
                    
        elif path.suffix == ".jsonl":
            with open(path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if limit and i >= limit:
                        break
                    row = json.loads(line)
                    meta = ArtifactMetadata(
                        artifact_type=ArtifactType.DATASET_RECORD,
                        producer_module="ingestion_engine",
                        pipeline_run_id=run_id,
                    )
                    rec = DatasetRecord(
                        metadata=meta,
                        source_type=SourceType.JSONL,
                        source_uri=path.name,
                        raw_payload=row,
                    )
                    records.append(rec)
                    
        return records
