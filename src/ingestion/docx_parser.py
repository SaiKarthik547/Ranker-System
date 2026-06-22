import uuid
from docx import Document
from pathlib import Path
from src.contracts.ingestion import DatasetRecord
from src.contracts.enums import SourceType, ArtifactType
from src.contracts.metadata import ArtifactMetadata

class DocxParser:
    def process(self, file_path: str, run_id: uuid.UUID) -> DatasetRecord:
        """Parses a DOCX file into a single DatasetRecord."""
        doc = Document(file_path)
        text_content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        
        # We store the text under a structured payload
        raw_payload = {
            "document_text": text_content,
            "filename": Path(file_path).name,
            "type": "JOB_DESCRIPTION"
        }
        
        meta = ArtifactMetadata(
            artifact_type=ArtifactType.DATASET_RECORD,
            producer_module="docx_parser",
            pipeline_run_id=run_id
        )
        
        return DatasetRecord(
            metadata=meta,
            source_type=SourceType.UNKNOWN,
            source_uri=file_path,
            raw_payload=raw_payload,
            normalized_payload=raw_payload
        )
