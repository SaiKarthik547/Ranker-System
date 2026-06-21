"""
Enumerations for data contracts.
"""

from enum import StrEnum


class ConfidenceLevel(StrEnum):
    """Levels of derived confidence."""

    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class SeverityLevel(StrEnum):
    """Severity levels for anomalies."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EntityType(StrEnum):
    """Types of extracted entities."""

    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    TECHNOLOGY = "TECHNOLOGY"
    SKILL = "SKILL"
    CERTIFICATION = "CERTIFICATION"
    PROJECT = "PROJECT"
    PRODUCT = "PRODUCT"
    IDENTIFIER = "IDENTIFIER"
    UNKNOWN = "UNKNOWN"


class PatternType(StrEnum):
    """Types of discovered patterns."""

    CO_OCCURRENCE = "CO_OCCURRENCE"
    SEQUENCE = "SEQUENCE"
    TRANSITION = "TRANSITION"
    HIERARCHY = "HIERARCHY"
    REPEATED_STRUCTURE = "REPEATED_STRUCTURE"


class AnomalyType(StrEnum):
    """Types of discovered anomalies."""

    STRUCTURAL = "STRUCTURAL"
    STATISTICAL = "STATISTICAL"
    TEMPORAL = "TEMPORAL"
    SEMANTIC = "SEMANTIC"
    RELATIONSHIP = "RELATIONSHIP"
    QUALITY = "QUALITY"


class RelationshipType(StrEnum):
    """Types of inferred relationships."""

    WORKED_AT = "WORKED_AT"
    HAS_SKILL = "HAS_SKILL"
    LOCATED_IN = "LOCATED_IN"
    OWNS = "OWNS"
    CREATED = "CREATED"
    EARNED = "EARNED"
    USES = "USES"


class DirectionType(StrEnum):
    """Directionality of relationships."""

    DIRECTED = "DIRECTED"
    BIDIRECTIONAL = "BIDIRECTIONAL"


class ArtifactType(StrEnum):
    """All generated artifact types."""

    DATASET_RECORD = "DATASET_RECORD"
    SCHEMA_GRAPH = "SCHEMA_GRAPH"
    PROFILE_REPORT = "PROFILE_REPORT"
    SEMANTIC_CATALOG = "SEMANTIC_CATALOG"
    ENTITY_CATALOG = "ENTITY_CATALOG"
    RELATIONSHIP_CATALOG = "RELATIONSHIP_CATALOG"
    PATTERN_CATALOG = "PATTERN_CATALOG"
    CLUSTER_CATALOG = "CLUSTER_CATALOG"
    ANOMALY_CATALOG = "ANOMALY_CATALOG"
    INTELLIGENCE_REPORT = "INTELLIGENCE_REPORT"
    INTELLIGENCE_SUMMARY = "INTELLIGENCE_SUMMARY"
    SCHEMA_FIELD = "SCHEMA_FIELD"
    PROFILE_METRIC = "PROFILE_METRIC"
    SEMANTIC_CONCEPT = "SEMANTIC_CONCEPT"
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    PATTERN = "PATTERN"
    CLUSTER = "CLUSTER"
    ANOMALY = "ANOMALY"
    RECOMMENDATION = "RECOMMENDATION"
    ARTIFACT_REGISTRY = "ARTIFACT_REGISTRY"


class SourceType(StrEnum):
    """Source origin of a dataset record."""

    CSV = "CSV"
    JSON = "JSON"
    JSONL = "JSONL"
    PARQUET = "PARQUET"
    DATABASE = "DATABASE"
    API = "API"
    STREAM = "STREAM"
    UNKNOWN = "UNKNOWN"


class FieldType(StrEnum):
    """Discovered data type of a schema field."""

    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"
    UNKNOWN = "UNKNOWN"


class MetricType(StrEnum):
    """Statistical metric types."""

    NULLABILITY = "NULLABILITY"
    CARDINALITY = "CARDINALITY"
    DISTRIBUTION = "DISTRIBUTION"
    UNIQUENESS = "UNIQUENESS"
    ENTROPY = "ENTROPY"
    FREQUENCY = "FREQUENCY"
    MIN = "MIN"
    MAX = "MAX"
    MEAN = "MEAN"
    MEDIAN = "MEDIAN"
    STDDEV = "STDDEV"
    MODE = "MODE"
    UNKNOWN = "UNKNOWN"
