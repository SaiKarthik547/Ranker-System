"""
Tests for Milestone 1 Batch 3 (Ingestion Contracts).
"""

import uuid
from types import MappingProxyType

import pytest
from pydantic import ValidationError

from src.contracts import ArtifactMetadata, DatasetRecord
from src.contracts.enums import ArtifactType, SourceType


def get_mock_metadata() -> ArtifactMetadata:
    return ArtifactMetadata(
        artifact_type=ArtifactType.DATASET_RECORD,
        producer_module="ingestion",
        pipeline_run_id=uuid.uuid4(),
        tags=("v1", "test"),
    )


def test_dataset_record_instantiation() -> None:
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.CSV,
        source_uri="s3://bucket/test.csv",
        raw_payload={"key": "value", "list_data": [1, 2, 3], "nested": {"inner": "data"}},
    )
    assert record.source_type == SourceType.CSV
    assert isinstance(record.raw_payload, MappingProxyType)
    assert isinstance(record.raw_payload["nested"], MappingProxyType)
    assert isinstance(record.raw_payload["list_data"], tuple)
    assert record.raw_payload["key"] == "value"


def test_dataset_record_validation() -> None:
    with pytest.raises(ValidationError):
        # Missing required
        DatasetRecord(source_type=SourceType.API)  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        # Empty URI
        DatasetRecord(
            metadata=get_mock_metadata(),
            source_type=SourceType.API,
            source_uri="",
            raw_payload={"key": "value"},
        )


def test_dataset_record_deep_immutability() -> None:
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.CSV,
        source_uri="s3://bucket/test.csv",
        raw_payload={"key": "value", "list_data": [1, 2, 3], "nested": {"inner": "data"}},
    )
    
    # Top level immutability
    with pytest.raises(ValidationError):
        record.source_uri = "hacked"

    # Deep mapping immutability blocked natively by python TypeError
    with pytest.raises(TypeError):
        record.raw_payload["key"] = "hacked"  # type: ignore[index]

    with pytest.raises(TypeError):
        record.raw_payload["nested"]["inner"] = "hacked"  # type: ignore[index]

    with pytest.raises(TypeError):
        record.raw_payload["list_data"][0] = 5  # type: ignore[index]


def test_dataset_record_serialization() -> None:
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.API,
        source_uri="https://api.test.com",
        raw_payload={"key": "value", "list_data": [1, 2, 3], "nested": {"inner": "data"}},
    )
    dumped = record.model_dump()
    # Dicts should be natively un-proxied
    assert isinstance(dumped["raw_payload"], dict)
    assert isinstance(dumped["raw_payload"]["nested"], dict)
    assert isinstance(dumped["raw_payload"]["list_data"], list)

    json_str = record.model_dump_json()
    assert '"key":"value"' in json_str.replace(" ", "")


def test_dataset_record_roundtrip() -> None:
    record = DatasetRecord(
        metadata=get_mock_metadata(),
        source_type=SourceType.API,
        source_uri="https://api.test.com",
        raw_payload={"key": "value", "list_data": [1, 2, 3], "nested": {"inner": "data"}},
    )
    json_str = record.model_dump_json()
    restored = DatasetRecord.model_validate_json(json_str)

    assert restored == record
    # MappingProxyType automatically applied on reconstruction
    assert isinstance(restored.raw_payload, MappingProxyType)
    assert isinstance(restored.raw_payload["nested"], MappingProxyType)
    assert isinstance(restored.raw_payload["list_data"], tuple)
