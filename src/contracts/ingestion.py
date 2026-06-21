"""
Ingestion contracts.
"""

import uuid
from types import MappingProxyType
from typing import Any, Mapping

from pydantic import Field, field_serializer, field_validator

from src.contracts.base import BaseArtifact
from src.contracts.enums import SourceType
from src.contracts.types import ArtifactId


def freeze_payload(value: Any) -> Any:
    """Recursively freeze a payload into deep immutable structures."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: freeze_payload(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze_payload(v) for v in value)
    return value


def unfreeze_payload(value: Any) -> Any:
    """Recursively unfreeze a payload back into native dicts/lists for serialization."""
    if isinstance(value, Mapping):
        return {k: unfreeze_payload(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [unfreeze_payload(v) for v in value]
    return value


class DatasetRecord(BaseArtifact):
    """Immutable representation of a single data record ingested into the system."""

    record_id: ArtifactId = Field(default_factory=uuid.uuid4)
    source_type: SourceType
    source_uri: str = Field(min_length=1)
    raw_payload: Mapping[str, Any]
    normalized_payload: Mapping[str, Any] | None = None

    @field_validator("raw_payload", "normalized_payload", mode="after")
    @classmethod
    def enforce_immutability(cls, v: Any) -> Any:
        """Ensure payloads are deeply immutable upon assignment."""
        if v is None:
            return None
        return freeze_payload(v)

    @field_serializer("raw_payload", "normalized_payload")
    def serialize_mapping_proxy(self, v: Any) -> Any:
        """Convert deep immutable structures back to dicts/lists for JSON serialization."""
        if v is None:
            return None
        return unfreeze_payload(v)
