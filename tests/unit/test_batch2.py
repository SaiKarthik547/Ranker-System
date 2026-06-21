"""
Tests for Milestone 1 Batch 2 (Confidence, Evidence, Metadata).
"""

import json
import uuid

import pytest
from pydantic import ValidationError

from src.contracts import (
    ArtifactMetadata,
    BaseArtifact,
    Confidence,
    Evidence,
    IntelligenceArtifact,
)
from src.contracts.enums import ArtifactType, ConfidenceLevel


def get_mock_confidence() -> Confidence:
    """Helper to get a valid Confidence instance."""
    return Confidence(
        confidence_score=0.85,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_method="statistical_inference",
        confidence_factors={"null_rate": 0.9},
        confidence_explanation="Derived from test.",
    )


def test_confidence_instantiation() -> None:
    """Test standard instantiation."""
    conf = get_mock_confidence()
    assert conf.confidence_score == 0.85
    assert conf.confidence_level == ConfidenceLevel.HIGH


def test_confidence_validation() -> None:
    """Test bounds and required fields."""
    with pytest.raises(ValidationError):
        # Missing required
        Confidence(confidence_score=0.5)  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        # Score out of bounds (> 1.0)
        Confidence(
            confidence_score=1.5,
            confidence_level=ConfidenceLevel.HIGH,
            confidence_method="test",
            confidence_explanation="test",
        )


def test_confidence_immutability() -> None:
    """Test frozen=True."""
    conf = get_mock_confidence()
    with pytest.raises(ValidationError):
        conf.confidence_score = 0.9


def test_confidence_serialization() -> None:
    """Test model_dump_json()."""
    conf = get_mock_confidence()
    data = json.loads(conf.model_dump_json())
    assert data["confidence_score"] == 0.85
    assert data["confidence_level"] == "HIGH"


def test_confidence_roundtrip() -> None:
    """Test json load and dump matching."""
    conf = get_mock_confidence()
    restored = Confidence.model_validate_json(conf.model_dump_json())
    assert restored == conf


def get_mock_evidence() -> Evidence:
    """Helper to get a valid Evidence instance."""
    return Evidence(
        evidence_type="profiling_metric",
        source_artifact=uuid.uuid4(),
        source_location="profile.skills",
        source_value="Python",
        reasoning="High frequency",
    )


def test_evidence_instantiation() -> None:
    """Test standard instantiation."""
    ev = get_mock_evidence()
    assert ev.evidence_type == "profiling_metric"
    assert ev.timestamp is not None
    assert isinstance(ev.evidence_id, uuid.UUID)


def test_evidence_validation() -> None:
    """Test required fields."""
    with pytest.raises(ValidationError):
        # Missing reasoning
        Evidence(
            evidence_type="test",
            source_artifact=uuid.uuid4(),
        )  # type: ignore[call-arg]


def test_evidence_immutability() -> None:
    """Test frozen=True."""
    ev = get_mock_evidence()
    with pytest.raises(ValidationError):
        ev.reasoning = "changed"


def test_evidence_roundtrip() -> None:
    """Test json load and dump matching."""
    ev = get_mock_evidence()
    restored = Evidence.model_validate_json(ev.model_dump_json())
    assert restored == ev


def get_mock_metadata() -> ArtifactMetadata:
    """Helper to get a valid Metadata instance."""
    return ArtifactMetadata(
        artifact_type=ArtifactType.SCHEMA_GRAPH,
        producer_module="schema_discovery",
        pipeline_run_id=uuid.uuid4(),
    )


def test_metadata_instantiation() -> None:
    """Test standard instantiation and defaults."""
    meta = get_mock_metadata()
    assert meta.artifact_type == ArtifactType.SCHEMA_GRAPH
    assert meta.artifact_version == "1.0.0"
    assert meta.evidence_count == 0


def test_metadata_validation() -> None:
    """Test constraints (ge=0)."""
    with pytest.raises(ValidationError):
        # Missing pipeline_run_id
        ArtifactMetadata(
            artifact_type=ArtifactType.SCHEMA_GRAPH,
            producer_module="test",
        )  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        # Bad evidence_count (ge=0)
        ArtifactMetadata(
            artifact_type=ArtifactType.SCHEMA_GRAPH,
            producer_module="test",
            pipeline_run_id=uuid.uuid4(),
            evidence_count=-1,
        )


def test_metadata_immutability() -> None:
    """Test frozen=True."""
    meta = get_mock_metadata()
    with pytest.raises(ValidationError):
        meta.producer_module = "hacked"


def test_metadata_roundtrip() -> None:
    """Test json load and dump matching."""
    meta = get_mock_metadata()
    restored = ArtifactMetadata.model_validate_json(meta.model_dump_json())
    assert restored == meta


def test_base_artifact_resolution() -> None:
    """Verify forward reference 'ArtifactMetadata' resolved correctly."""
    meta = get_mock_metadata()
    artifact = BaseArtifact(metadata=meta)
    assert artifact.metadata.artifact_type == ArtifactType.SCHEMA_GRAPH


def test_intelligence_artifact_resolution() -> None:
    """Verify forward references 'Confidence' and 'Evidence' resolved correctly."""
    meta = get_mock_metadata()
    conf = get_mock_confidence()
    ev = get_mock_evidence()
    artifact = IntelligenceArtifact(
        metadata=meta,
        confidence=conf,
        evidence=[ev],
    )
    assert artifact.confidence.confidence_level == ConfidenceLevel.HIGH
    assert artifact.evidence[0].evidence_type == "profiling_metric"
