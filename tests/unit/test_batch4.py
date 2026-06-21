"""
Tests for Milestone 1 Batch 4 (Schema Contracts).
"""

import uuid

import pytest
from pydantic import ValidationError

from src.contracts import ArtifactMetadata, Confidence, Evidence, SchemaField, SchemaGraph
from src.contracts.enums import ArtifactType, ConfidenceLevel, FieldType


def get_mock_metadata() -> ArtifactMetadata:
    return ArtifactMetadata(
        artifact_type=ArtifactType.SCHEMA_GRAPH,
        producer_module="schema_discovery",
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


def get_mock_schema_field() -> SchemaField:
    return SchemaField(
        field_name="user_id",
        field_path="data.user_id",
        parent_field="data",
        data_type=FieldType.INTEGER,
        nullable=False,
        cardinality=1000,
        uniqueness=1.0,
        is_identifier=True,
        sample_values=(1, 2, 3),
    )


def test_schema_field_instantiation() -> None:
    field = get_mock_schema_field()
    assert field.data_type == FieldType.INTEGER
    assert field.is_identifier is True
    assert isinstance(field.sample_values, tuple)


def test_schema_field_validation() -> None:
    with pytest.raises(ValidationError):
        # Missing required
        SchemaField(field_name="test")  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        # Uniqueness clamping replacement: explicit failure
        SchemaField(
            field_name="test",
            field_path="test",
            data_type=FieldType.STRING,
            nullable=False,
            uniqueness=1.5,
        )

    with pytest.raises(ValidationError):
        # Negative cardinality
        SchemaField(
            field_name="test",
            field_path="test",
            data_type=FieldType.STRING,
            nullable=False,
            cardinality=-5,
        )


def test_schema_field_immutability() -> None:
    field = get_mock_schema_field()
    with pytest.raises(ValidationError):
        field.data_type = FieldType.STRING

    # Tuple strictly prevents nested assignment
    with pytest.raises(TypeError):
        field.sample_values[0] = 5  # type: ignore[index]


def test_schema_field_roundtrip() -> None:
    field = get_mock_schema_field()
    restored = SchemaField.model_validate_json(field.model_dump_json())
    assert restored == field
    assert isinstance(restored.sample_values, tuple)


def test_schema_graph_instantiation() -> None:
    field = get_mock_schema_field()
    graph = SchemaGraph(
        metadata=get_mock_metadata(),
        confidence=get_mock_confidence(),
        evidence=(get_mock_evidence(),),
        fields=(field,),
        record_count=100,
        nesting_depth=2,
    )
    assert graph.record_count == 100
    assert len(graph.fields) == 1
    assert graph.fields[0].field_name == "user_id"


def test_schema_graph_validation() -> None:
    # Empty fields array
    with pytest.raises(ValidationError):
        SchemaGraph(
            metadata=get_mock_metadata(),
            confidence=get_mock_confidence(),
            evidence=(get_mock_evidence(),),
            fields=(),
            record_count=100,
            nesting_depth=2,
        )

    # Negative record count
    with pytest.raises(ValidationError):
        SchemaGraph(
            metadata=get_mock_metadata(),
            confidence=get_mock_confidence(),
            evidence=(get_mock_evidence(),),
            fields=(get_mock_schema_field(),),
            record_count=-1,
            nesting_depth=2,
        )


def test_schema_graph_immutability() -> None:
    field = get_mock_schema_field()
    graph = SchemaGraph(
        metadata=get_mock_metadata(),
        confidence=get_mock_confidence(),
        evidence=(get_mock_evidence(),),
        fields=(field,),
        record_count=100,
        nesting_depth=2,
    )
    with pytest.raises(ValidationError):
        graph.record_count = 200

    with pytest.raises(TypeError):
        # Tuples prevent item assignment
        graph.fields[0] = field  # type: ignore[index]


def test_schema_graph_roundtrip() -> None:
    field = get_mock_schema_field()
    graph = SchemaGraph(
        metadata=get_mock_metadata(),
        confidence=get_mock_confidence(),
        evidence=(get_mock_evidence(),),
        fields=(field,),
        record_count=100,
        nesting_depth=2,
    )
    restored = SchemaGraph.model_validate_json(graph.model_dump_json())
    assert restored == graph
    assert isinstance(restored.fields, tuple)
