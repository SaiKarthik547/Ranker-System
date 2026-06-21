"""
Schema contracts.
"""

import uuid

from pydantic import Field

from src.contracts.base import BaseContract, IntelligenceArtifact
from src.contracts.enums import FieldType
from src.contracts.types import ArtifactId, PrimitiveValue


class SchemaField(BaseContract):
    """Immutable representation of a single discovered data attribute."""

    field_id: ArtifactId = Field(default_factory=uuid.uuid4)
    field_name: str = Field(min_length=1)
    field_path: str = Field(min_length=1)
    parent_field: str | None = None
    data_type: FieldType
    nullable: bool
    cardinality: int | None = Field(default=None, ge=0)
    uniqueness: float | None = Field(default=None, ge=0.0, le=1.0)
    is_identifier: bool = False
    sample_values: tuple[PrimitiveValue, ...] = Field(default_factory=tuple)


class SchemaGraph(IntelligenceArtifact):
    """Aggregation of all SchemaFields representing the total structural topology."""

    schema_id: ArtifactId = Field(default_factory=uuid.uuid4)
    fields: tuple[SchemaField, ...] = Field(min_length=1)
    record_count: int = Field(ge=0)
    nesting_depth: int = Field(ge=0)
    relationships: tuple[str, ...] = Field(default_factory=tuple)
