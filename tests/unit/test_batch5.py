"""
Tests for Milestone 1 Batch 5 (Profiling Contracts).
"""

import uuid

import pytest
from pydantic import ValidationError

from src.contracts import ArtifactMetadata, Confidence, Evidence, ProfileMetric, ProfileReport
from src.contracts.enums import ArtifactType, ConfidenceLevel, MetricType


def get_mock_metadata() -> ArtifactMetadata:
    return ArtifactMetadata(
        artifact_type=ArtifactType.PROFILE_REPORT,
        producer_module="profiling_engine",
        pipeline_run_id=uuid.uuid4(),
    )


def get_mock_confidence() -> Confidence:
    return Confidence(
        confidence_score=0.9,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_method="test",
        confidence_explanation="test",
    )


def get_mock_evidence() -> Evidence:
    return Evidence(
        evidence_type="test",
        source_artifact=uuid.uuid4(),
        reasoning="test",
    )


def test_profile_metric_instantiation() -> None:
    # Test valid nullability
    metric = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.NULLABILITY,
        metric_value=0.05,
        calculation_method="count",
    )
    assert metric.metric_value == 0.05

    # Test valid cardinality
    metric_card = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.CARDINALITY,
        metric_value=100,
        calculation_method="distinct",
    )
    assert metric_card.metric_value == 100

    # Test valid distribution
    dist = (("child", 0.2), ("adult", 0.8))
    metric_dist = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.DISTRIBUTION,
        metric_value=dist,
        calculation_method="histogram",
    )
    assert metric_dist.metric_value == dist


def test_profile_metric_validation() -> None:
    # Test invalid nullability bounds
    with pytest.raises(ValidationError):
        ProfileMetric(
            field_path="user.age",
            metric_type=MetricType.NULLABILITY,
            metric_value=1.5,
            calculation_method="count",
        )

    # Test invalid nullability type
    with pytest.raises(ValidationError):
        ProfileMetric(
            field_path="user.age",
            metric_type=MetricType.NULLABILITY,
            metric_value=5,  # int instead of float
            calculation_method="count",
        )

    # Test invalid cardinality
    with pytest.raises(ValidationError):
        ProfileMetric(
            field_path="user.age",
            metric_type=MetricType.CARDINALITY,
            metric_value=-1,
            calculation_method="distinct",
        )


def test_profile_metric_immutability() -> None:
    metric = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.NULLABILITY,
        metric_value=0.05,
        calculation_method="count",
    )
    with pytest.raises(ValidationError):
        metric.metric_value = 0.1

    # Test tuple immutability
    dist = (("child", 0.2), ("adult", 0.8))
    metric_dist = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.DISTRIBUTION,
        metric_value=dist,
        calculation_method="histogram",
    )
    with pytest.raises(TypeError):
        metric_dist.metric_value[0] = ("senior", 0.1)  # type: ignore[index]


def test_profile_report_instantiation() -> None:
    metric = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.NULLABILITY,
        metric_value=0.05,
        calculation_method="count",
    )
    report = ProfileReport(
        metadata=get_mock_metadata(),
        confidence=get_mock_confidence(),
        evidence=(get_mock_evidence(),),
        field_metrics=(metric,),
    )
    assert len(report.field_metrics) == 1
    assert report.summary is None


def test_profile_report_validation() -> None:
    # Empty field metrics
    with pytest.raises(ValidationError):
        ProfileReport(
            metadata=get_mock_metadata(),
            confidence=get_mock_confidence(),
            evidence=(get_mock_evidence(),),
            field_metrics=(),
        )


def test_profile_report_immutability() -> None:
    metric = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.NULLABILITY,
        metric_value=0.05,
        calculation_method="count",
    )
    report = ProfileReport(
        metadata=get_mock_metadata(),
        confidence=get_mock_confidence(),
        evidence=(get_mock_evidence(),),
        field_metrics=(metric,),
    )
    with pytest.raises(ValidationError):
        report.summary = "new summary"

    with pytest.raises(TypeError):
        report.field_metrics[0] = metric  # type: ignore[index]


def test_profile_roundtrip() -> None:
    metric = ProfileMetric(
        field_path="user.age",
        metric_type=MetricType.NULLABILITY,
        metric_value=0.05,
        calculation_method="count",
    )
    report = ProfileReport(
        metadata=get_mock_metadata(),
        confidence=get_mock_confidence(),
        evidence=(get_mock_evidence(),),
        field_metrics=(metric,),
        summary="Test report",
    )
    json_str = report.model_dump_json()
    restored = ProfileReport.model_validate_json(json_str)
    
    assert restored == report
    assert restored.field_metrics[0].metric_type == MetricType.NULLABILITY
    assert isinstance(restored.field_metrics, tuple)
