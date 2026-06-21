# 04_DATA_CONTRACTS.md

Version: 1.0

Status: Architecture Critical

Project:
Universal Dataset Intelligence Platform

Phase:
Phase 1 — Dataset Intelligence Engine

---

# Purpose

This document defines every shared data contract used across the system.

These contracts are the ONLY approved communication mechanism between modules.

Modules must never exchange:

* raw dictionaries
* anonymous objects
* dynamic payloads
* untyped structures

All communication must use approved contracts.

---

# Contract Design Principles

Every contract must be:

Immutable

Serializable

Versioned

Traceable

Evidence-Based

Confidence-Aware

Auditable

Extensible

---

# Universal Metadata Contract

Every artifact produced anywhere in the platform must contain:

Artifact Metadata

Fields:

artifact_id

artifact_type

artifact_version

created_at

producer_module

pipeline_run_id

schema_version

confidence

evidence_count

tags

This metadata is mandatory.

---

# Confidence Contract

Purpose:

Represent confidence consistently across the platform.

Fields:

confidence_score

confidence_level

confidence_method

confidence_factors

confidence_explanation

---

Confidence Levels

VERY_LOW

LOW

MEDIUM

HIGH

VERY_HIGH

---

Confidence Rules

No hardcoded confidence values.

Confidence must be derived.

Every confidence value requires explanation.

---

# Evidence Contract

Purpose:

Support explainability.

Fields:

evidence_id

evidence_type

source_artifact

source_location

source_value

reasoning

confidence

timestamp

---

Rule

No intelligence artifact may exist without evidence.

---

# Dataset Record Contract

Purpose:

Standardized dataset record representation.

Fields:

record_id

source_type

source_location

raw_payload

normalized_payload

metadata

---

Used only inside ingestion.

Never exposed externally.

---

# Schema Field Contract

Purpose:

Represent discovered fields.

Fields:

field_id

field_path

field_name

parent_field

data_type

nullable

uniqueness

cardinality

sample_values

confidence

evidence

---

Examples

profile.skills

education.degree

career_history.company

---

# Schema Graph Contract

Purpose:

Represent entire discovered schema.

Fields:

schema_id

fields

relationships

nesting_depth

record_count

confidence

evidence

metadata

---

# Profile Metric Contract

Purpose:

Represent statistical findings.

Fields:

metric_id

field_path

metric_name

metric_value

calculation_method

confidence

evidence

---

Examples

null_rate

uniqueness

entropy

distribution

frequency

---

# Profile Report Contract

Purpose:

Aggregate profiling results.

Fields:

report_id

field_metrics

quality_metrics

distribution_metrics

summary

confidence

evidence

metadata

---

# Semantic Concept Contract

Purpose:

Represent discovered concepts.

Fields:

concept_id

concept_name

concept_type

aliases

parent_concepts

child_concepts

examples

confidence

evidence

---

Examples

Machine Learning

Databases

Cloud Computing

Finance

Healthcare

---

# Semantic Catalog Contract

Fields:

catalog_id

concepts

taxonomy

relationships

confidence

evidence

metadata

---

# Entity Contract

Purpose:

Represent discovered entities.

Fields:

entity_id

entity_type

canonical_value

normalized_value

aliases

source_fields

frequency

confidence

evidence

metadata

---

Entity Types

PERSON

ORGANIZATION

LOCATION

TECHNOLOGY

SKILL

CERTIFICATION

PROJECT

PRODUCT

IDENTIFIER

UNKNOWN

---

# Entity Catalog Contract

Fields:

catalog_id

entities

entity_count

entity_types

confidence

evidence

metadata

---

# Relationship Contract

Purpose:

Represent inferred relationships.

Fields:

relationship_id

source_entity

relationship_type

target_entity

direction

confidence

evidence

metadata

---

Examples

WORKED_AT

HAS_SKILL

LOCATED_IN

OWNS

CREATED

EARNED

USES

---

# Relationship Catalog Contract

Fields:

catalog_id

relationships

relationship_count

confidence

evidence

metadata

---

# Pattern Contract

Purpose:

Represent discovered patterns.

Fields:

pattern_id

pattern_type

description

frequency

support

confidence

evidence

metadata

---

Pattern Types

CO_OCCURRENCE

SEQUENCE

TRANSITION

HIERARCHY

REPEATED_STRUCTURE

---

# Pattern Catalog Contract

Fields:

catalog_id

patterns

pattern_count

confidence

evidence

metadata

---

# Cluster Contract

Purpose:

Represent discovered clusters.

Fields:

cluster_id

cluster_name

cluster_description

member_count

representative_features

confidence

evidence

metadata

---

# Cluster Catalog Contract

Fields:

catalog_id

clusters

cluster_count

confidence

evidence

metadata

---

# Anomaly Contract

Purpose:

Represent discovered anomalies.

Fields:

anomaly_id

anomaly_type

severity

description

affected_records

affected_entities

confidence

evidence

metadata

---

Anomaly Types

STRUCTURAL

STATISTICAL

TEMPORAL

SEMANTIC

RELATIONSHIP

QUALITY

---

Severity Levels

LOW

MEDIUM

HIGH

CRITICAL

---

# Anomaly Catalog Contract

Fields:

catalog_id

anomalies

anomaly_count

severity_distribution

confidence

evidence

metadata

---

# Recommendation Contract

Purpose:

Represent intelligence recommendations.

Fields:

recommendation_id

recommendation_type

description

priority

supporting_evidence

confidence

metadata

---

# Intelligence Summary Contract

Purpose:

High-level findings.

Fields:

summary_id

title

description

key_findings

warnings

recommendations

confidence

evidence

metadata

---

# Intelligence Report Contract

Purpose:

Final Phase 1 output.

Fields:

report_id

dataset_summary

schema_summary

profiling_summary

semantic_summary

entity_summary

relationship_summary

pattern_summary

cluster_summary

anomaly_summary

recommendations

warnings

confidence

evidence

metadata

---

# Artifact Registry Contract

Purpose:

Track generated artifacts.

Fields:

artifact_id

artifact_type

artifact_version

producer_module

dependencies

created_at

status

metadata

---

# Contract Evolution Rules

Future versions may:

Add fields

Add metadata

Add artifact types

Future versions must NOT:

Remove required fields

Rename existing fields

Change semantic meaning

Break compatibility

---

# Validation Rules

Every contract requires:

Schema validation

Type validation

Confidence validation

Evidence validation

Version validation

Metadata validation

Any artifact failing validation is rejected.

---

# Definition Of Contract Compliance

A module is contract-compliant only if:

It consumes approved contracts.

It produces approved contracts.

It validates contracts.

It preserves evidence.

It preserves confidence.

It preserves metadata.

If any condition fails:

The module is non-compliant.
