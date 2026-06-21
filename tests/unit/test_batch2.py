"""
Tests for Milestone 1 Batch 2 (Intelligence Infrastructure Contracts).
"""

import uuid

import pytest
from pydantic import ValidationError

from src.contracts import ArtifactMetadata, Confidence, Evidence
from src.contracts.enums import ArtifactType, ConfidenceLevel


def test_artifact_metadata_instantiation() -> None:
    metadata = ArtifactMetadata(
        artifact_type=ArtifactType.DATASET_RECORD,
        producer_module="ingestion_pipeline",
        pipeline_run_id=uuid.uuid4(),
        tags=("v1", "test"),
    )
    assert metadata.artifact_type == ArtifactType.DATASET_RECORD
    assert metadata.tags == ("v1", "test")


def test_confidence_instantiation() -> None:
    confidence = Confidence(
        confidence_score=0.85,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_method="statistical_inference",
        confidence_factors=(("null_rate", 0.9),),
        confidence_explanation="Derived from test.",
    )
    assert confidence.confidence_score == 0.85
    assert confidence.confidence_factors[0] == ("null_rate", 0.9)


def test_evidence_instantiation() -> None:
    evidence = Evidence(
        evidence_type="profiling_metric",
        source_artifact=uuid.uuid4(),
        source_location="profile.skills",
        source_value="Python",
        reasoning="High frequency",
    )
    assert evidence.evidence_type == "profiling_metric"
    assert evidence.source_value == "Python"


def test_metadata_immutability() -> None:
    metadata = ArtifactMetadata(
        artifact_type=ArtifactType.DATASET_RECORD,
        producer_module="ingestion_pipeline",
        pipeline_run_id=uuid.uuid4(),
        tags=("v1", "test"),
    )
    with pytest.raises(ValidationError):
        metadata.schema_version = "2.0.0"

    with pytest.raises(TypeError):
        metadata.tags[0] = "hacked"  # type: ignore[index]


def test_metadata_roundtrip() -> None:
    metadata = ArtifactMetadata(
        artifact_type=ArtifactType.DATASET_RECORD,
        producer_module="ingestion_pipeline",
        pipeline_run_id=uuid.uuid4(),
        tags=("v1", "test"),
    )
    json_str = metadata.model_dump_json()
    restored = ArtifactMetadata.model_validate_json(json_str)
    assert restored == metadata
    assert isinstance(restored.tags, tuple)
