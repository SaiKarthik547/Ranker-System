# 01_ENGINEERING_CHARTER.md

Version: 1.0

Status: Mandatory

Applies To:

* Phase 1 Dataset Intelligence Engine
* Phase 2 Knowledge Graph & Dataset Memory
* Phase 3 Adaptive Ranking Engine
* Phase 4 Explainability Engine
* Phase 5 Evaluation & Learning Layer

---

# Purpose

This document defines the engineering constitution for the entire project.

Any generated code, architecture, test, workflow, implementation, refactor, optimization, or future extension must comply with this charter.

If generated code violates this charter, the code is considered invalid regardless of whether it compiles.

---

# Core Mission

Build a universal dataset intelligence and ranking platform that:

* understands unknown datasets
* discovers structure automatically
* discovers entities automatically
* discovers relationships automatically
* discovers anomalies automatically
* generates explainable intelligence
* supports adaptive ranking

without relying on dataset-specific assumptions.

---

# Foundational Principles

## Principle 1

Understanding Before Ranking

Forbidden:

Dataset
→ Ranking

Required:

Dataset
→ Understanding
→ Intelligence
→ Ranking

---

## Principle 2

Evidence Over Assumptions

Every conclusion must contain evidence.

Examples:

Allowed:

"This field behaves like an identifier because it is unique in 99.9% of records."

Not Allowed:

"This field is an identifier."

without supporting evidence.

---

## Principle 3

No Hidden Intelligence

Every score.

Every anomaly.

Every relationship.

Every recommendation.

must be traceable.

---

## Principle 4

No Dataset-Specific Logic

Forbidden:

candidate["skills"]

candidate["education"]

candidate["career"]

Allowed:

schema discovery

semantic inference

entity inference

relationship inference

---

## Principle 5

Modularity First

Every module must have a single responsibility.

A module should answer exactly one question.

---

# Architecture Rules

Each module must define:

Input

Output

Dependencies

Failure Conditions

Metrics

Confidence

Every module must be independently testable.

---

# Code Generation Rules

The system must never generate:

pass

TODO implementations

placeholder functions

mock production logic

fake algorithms

empty services

empty repositories

empty interfaces

unused abstractions

dead code

unused dependencies

silent failures

magic constants

hardcoded business rules

hardcoded dataset assumptions

---

# Explicitly Forbidden Patterns

Forbidden:

def analyze():
pass

Forbidden:

def detect():
return []

Forbidden:

except:
pass

Forbidden:

except Exception:
return None

Forbidden:

print("debug")

Forbidden:

global mutable state

Forbidden:

hidden side effects

Forbidden:

functions with unclear ownership

---

# Required Coding Standards

Every public function must contain:

Purpose

Inputs

Outputs

Errors

Complexity Notes

Every complex algorithm must contain:

Design rationale

Evidence

Expected behavior

Failure behavior

---

# Data Integrity Rules

Data must never be silently modified.

Every transformation must be:

traceable

reproducible

observable

---

# Testing Philosophy

The goal is not green tests.

The goal is correct behavior.

---

# Invalid Tests

Import tests

Object creation tests

Coverage inflation tests

Assertion-free tests

Mock-only workflows

---

# Valid Tests

Behavior tests

Integration tests

Adversarial tests

Failure tests

Data quality tests

End-to-end tests

---

# Adversarial Testing Requirement

Every intelligence module must be tested against:

broken schemas

missing values

corrupted records

unexpected nesting

mixed data types

outliers

duplicate identities

contradictory evidence

synthetic anomalies

---

# Logging Rules

All modules must emit:

module_name

execution_time

record_count

status

errors

warnings

confidence

No print statements allowed.

Structured logging only.

---

# Error Handling Rules

Errors must be classified as:

Recoverable

Non-Recoverable

Expected

Unexpected

Every exception must be logged.

No swallowed exceptions.

---

# Confidence Rules

Every intelligence artifact must contain confidence.

Examples:

Entity

Relationship

Pattern

Cluster

Anomaly

Recommendation

Confidence must be derived.

Never invented.

---

# Performance Philosophy

Correctness before optimization.

However:

No obviously inefficient architecture is allowed.

No unnecessary full scans.

No repeated expensive computation.

No duplicate parsing.

Streaming should be preferred whenever possible.

---

# Review Checklist

Before accepting any generated code:

Does it solve a real problem?

Does it contain placeholders?

Does it contain dead code?

Does it contain fake tests?

Does it violate modularity?

Is the behavior observable?

Is the output explainable?

Can the result be reproduced?

If any answer is negative:

Reject implementation.

---

# Definition Of Done

A feature is complete only when:

Implementation exists

Tests exist

Documentation exists

Failure handling exists

Logging exists

Evidence exists

Confidence exists

Review passes

Until all conditions are met:

The feature is not complete.
