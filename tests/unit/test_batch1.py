"""
Tests for Milestone 1 Batch 1 (Base Contracts, Enums, Types).
"""

import json
import uuid

import pytest
from pydantic import ValidationError

from src.contracts.base import BaseContract
from src.contracts.enums import ArtifactType, ConfidenceLevel
from src.contracts.types import ArtifactId


class DummyContract(BaseContract):
    """Dummy contract for testing base functionality."""

    id: ArtifactId
    name: str


def test_base_contract_instantiation() -> None:
    """Test that a base contract can be instantiated cleanly."""
    contract = BaseContract()
    assert contract is not None


def test_subclass_instantiation() -> None:
    """Test that a subclass validates required fields."""
    test_id = uuid.uuid4()
    contract = DummyContract(id=test_id, name="test_dummy")
    assert contract.id == test_id
    assert contract.name == "test_dummy"


def test_subclass_validation() -> None:
    """Test that strict validation rejects missing or bad typed fields."""
    with pytest.raises(ValidationError):
        # Missing name
        DummyContract(id=uuid.uuid4())  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        # Bad type for name
        DummyContract(id=uuid.uuid4(), name=123)  # type: ignore[arg-type]


def test_contract_immutability() -> None:
    """Test that contracts reject post-instantiation mutation."""
    test_id = uuid.uuid4()
    contract = DummyContract(id=test_id, name="test_dummy")

    with pytest.raises(ValidationError) as exc:
        contract.name = "mutated"
    assert "Instance is frozen" in str(exc.value)


def test_contract_serialization() -> None:
    """Test native model_dump_json serialization."""
    test_id = uuid.uuid4()
    contract = DummyContract(id=test_id, name="test_dummy")
    json_str = contract.model_dump_json()

    data = json.loads(json_str)
    assert data["id"] == str(test_id)
    assert data["name"] == "test_dummy"


def test_contract_roundtrip() -> None:
    """Test serialization and deserialization roundtrip."""
    test_id = uuid.uuid4()
    contract = DummyContract(id=test_id, name="test_dummy")
    json_str = contract.model_dump_json()

    reconstructed = DummyContract.model_validate_json(json_str)
    assert reconstructed == contract
    assert reconstructed.id == contract.id


def test_enum_behavior() -> None:
    """Test that StrEnums behave properly as strings."""
    assert ArtifactType.SCHEMA_GRAPH == "SCHEMA_GRAPH"
    assert ConfidenceLevel.HIGH == "HIGH"


def test_types_behavior() -> None:
    """Test that custom type aliases function correctly."""
    val: ArtifactId = uuid.uuid4()
    assert isinstance(val, uuid.UUID)
