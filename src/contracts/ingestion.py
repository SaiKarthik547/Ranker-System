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


class DatasetRecord(BaseArtifact):
    """Immutable representation of a single ingested data row."""

    record_id: ArtifactId = Field(default_factory=uuid.uuid4)
    source_type: SourceType
    source_location: str | None = None
    raw_payload: Mapping[str, Any]
    normalized_payload: Mapping[str, Any] | None = None

    @field_validator("raw_payload", "normalized_payload", mode="after")
    @classmethod
    def ensure_mapping_proxy(
        cls, v: Mapping[str, Any] | None
    ) -> Mapping[str, Any] | None:
        """Ensure payloads are wrapped in an immutable MappingProxyType."""
        if v is None:
            return v
        if isinstance(v, MappingProxyType):
            return v
        return MappingProxyType(dict(v))

    @field_serializer("raw_payload", "normalized_payload")
    def serialize_mapping_proxy(
        self, v: Mapping[str, Any] | None
    ) -> dict[str, Any] | None:
        """Serialize MappingProxyType back to native dict for JSON."""
        if v is None:
            return None
        return dict(v)
