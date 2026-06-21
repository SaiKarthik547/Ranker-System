"""
Tests for Milestone 1 Batch 3 (Ingestion).
"""

import json
import uuid
from types import MappingProxyType

import pytest
from pydantic import ValidationError

from src.contracts import ArtifactMetadata, DatasetRecord
from src.contracts.enums import ArtifactType, SourceType


def get_mock_metadata() -> ArtifactMetadata:
    """Helper to get a valid Metadata instance."""
    return ArtifactMetadata(
        artifact_type=ArtifactType.DATASET_RECORD,
        producer_module="ingestion",
        pipeline_run_id=uuid.uuid4(),
    )


def test_dataset_record_instantiation() -> None:
    """Test instantiation and automatic MappingProxyType conversion."""
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.CSV,
        raw_payload={"key": "value"},
    )
    assert record.source_type == SourceType.CSV
    assert isinstance(record.raw_payload, MappingProxyType)
    assert record.raw_payload["key"] == "value"


def test_dataset_record_validation() -> None:
    """Test strict validation constraints."""
    with pytest.raises(ValidationError):
        # Missing raw_payload
        DatasetRecord(
            metadata=get_mock_metadata(),
            source_type=SourceType.CSV,
        )  # type: ignore[call-arg]


def test_dataset_record_immutability() -> None:
    """Test both top-level and deep immutability."""
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.CSV,
        raw_payload={"key": "value"},
    )
    # Top-level immutability
    with pytest.raises(ValidationError):
        record.source_type = SourceType.JSON

    # Nested mutability blocked natively by python TypeError
    with pytest.raises(TypeError):
        record.raw_payload["key"] = "hacked"  # type: ignore[index]


def test_dataset_record_serialization() -> None:
    """Test model_dump_json handles MappingProxyType smoothly."""
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.CSV,
        raw_payload={"key": "value"},
    )
    json_str = record.model_dump_json()
    data = json.loads(json_str)
    assert data["raw_payload"]["key"] == "value"


def test_dataset_record_roundtrip() -> None:
    """Test serialization and deserialization retains immutable wrappers."""
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.CSV,
        raw_payload={"key": "value"},
    )
    json_str = record.model_dump_json()
    restored = DatasetRecord.model_validate_json(json_str)
    
    # Ensure it's still a MappingProxyType after roundtrip
    assert isinstance(restored.raw_payload, MappingProxyType)
    assert restored.raw_payload["key"] == "value"
