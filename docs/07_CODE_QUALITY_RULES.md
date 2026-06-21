# 07_CODE_QUALITY_RULES.md

Version: 1.0

Status: Mandatory

Project:
Universal Dataset Intelligence Platform

Applies To:

All Phases

All Modules

All Generated Code

All Human-Written Code

---

# Purpose

This document defines:

Code quality standards

Maintainability standards

Readability standards

Refactoring rules

Review requirements

Code rejection criteria

Any code violating this document must be rejected.

---

# Core Philosophy

Code is written for:

Humans

Future Engineers

Reviewers

Maintainers

Not only for machines.

Readability and correctness are prioritized over cleverness.

---

# Golden Rule

If a new engineer cannot understand the code within minutes:

The code is too complex.

Refactor.

---

# Simplicity Rule

Prefer:

Simple

Explicit

Predictable

Deterministic

Over:

Clever

Magical

Implicit

Hidden

---

# Naming Rules

Names must explain intent.

Good:

SchemaDiscoveryEngine

RelationshipCatalog

EntityExtractor

Bad:

Manager

Processor

Handler

Util

Helper

Thing

DataStuff

---

# Variable Naming

Forbidden:

x

y

z

tmp

data

obj

val

result2

stuff

Good:

entity_catalog

relationship_graph

schema_field

anomaly_score

confidence_metrics

---

# Function Rules

Functions must:

Do one thing

Do it well

Have predictable outputs

Have explicit inputs

---

# Function Size Limits

Preferred:

<= 30 lines

Warning:

30-60 lines

Review Required:

60-100 lines

Rejected:

> 100 lines

unless justified.

---

# Function Complexity Rules

Maximum cyclomatic complexity target:

10

Warning:

10-15

Review:

15-20

Reject:

> 20

unless formally approved.

---

# Function Documentation

Every public function must document:

Purpose

Inputs

Outputs

Exceptions

Side Effects

Complexity Notes

---

# Class Rules

A class must represent:

One concept

One responsibility

One abstraction

---

# Class Size Limits

Preferred:

<300 lines

Review:

300-600 lines

Reject:

> 600 lines

unless approved.

---

# File Size Limits

Preferred:

<500 lines

Review:

500-1000 lines

Reject:

> 1000 lines

unless justified.

---

# Module Rules

A module must answer one question.

Examples:

schema

entities

relationships

anomalies

patterns

Forbidden:

Mixed responsibilities

---

# Dependency Rules

Allowed:

Downstream dependencies

Forbidden:

Circular dependencies

Cross-layer violations

Hidden dependencies

Global dependencies

---

# Import Rules

Imports must be:

Explicit

Minimal

Necessary

Forbidden:

Wildcard imports

Unused imports

Side-effect imports

---

# Global State Rules

Global mutable state prohibited.

Allowed:

Configuration constants

Immutable metadata

Forbidden:

Shared mutable data

Hidden caches

Global registries without ownership

---

# Error Handling Rules

Never:

except:
pass

Never:

except Exception:
return None

Every exception must:

Be classified

Be logged

Be explainable

---

# Logging Rules

Use structured logging.

Every log must include:

module

operation

status

duration

context

Never use print statements.

---

# Configuration Rules

Configuration must live outside business logic.

Forbidden:

Hardcoded paths

Hardcoded dataset names

Hardcoded thresholds

Hardcoded secrets

---

# Magic Number Rules

Forbidden:

score > 42

Required:

Named constants

Documented rationale

---

# Type Safety Rules

All public interfaces must use typing.

All contracts must be typed.

Untyped interfaces are prohibited.

---

# Documentation Rules

Every module requires:

Purpose

Responsibilities

Inputs

Outputs

Dependencies

Failure Conditions

Metrics

---

# Refactoring Rules

Refactor when:

Function exceeds limits

Class exceeds limits

File exceeds limits

Responsibilities become mixed

Complexity grows

Naming becomes unclear

---

# Dead Code Policy

Dead code prohibited.

Unused functions prohibited.

Unused classes prohibited.

Unused modules prohibited.

Delete immediately.

---

# Placeholder Policy

Forbidden:

pass

TODO

FIXME

placeholder implementations

mock business logic

fake returns

stubs pretending to be complete

---

# Testability Rules

Every component must be testable.

If difficult to test:

Architecture likely wrong.

Refactor.

---

# Contract Compliance Rules

All module interfaces must use:

Approved contracts

No custom payloads

No anonymous dictionaries

No undocumented structures

---

# Explainability Rules

Every intelligence-producing component must generate:

Evidence

Confidence

Explanation

Outputs without explainability are invalid.

---

# Performance Rules

Optimize only after correctness.

However:

Avoid obvious inefficiencies.

Avoid repeated scans.

Avoid duplicated parsing.

Avoid unnecessary allocations.

Prefer streaming when possible.

---

# AI Code Review Rules

Every generated file must be reviewed for:

Dead code

Unused imports

Unused variables

Placeholder logic

Architecture violations

Contract violations

Testing gaps

Naming issues

Complexity issues

---

# Pull Request Checklist

Before approval:

Compiles

Passes tests

Uses contracts

Uses typing

Uses logging

Has documentation

No dead code

No TODOs

No placeholders

No architecture violations

No hidden assumptions

---

# Automatic Rejection Criteria

Reject immediately if code contains:

pass

TODO implementations

Fake tests

Hardcoded dataset assumptions

Hardcoded schema assumptions

Silent failures

Dead code

Unused abstractions

Circular dependencies

Hidden side effects

Undocumented public interfaces

---

# Definition Of High Quality Code

Code is high quality only if it is:

Correct

Understandable

Maintainable

Observable

Testable

Typed

Documented

Deterministic

Explainable

Extensible

Anything less is technical debt.

---

# Final Principle

Future maintainability is a feature.

Readable code is a feature.

Observability is a feature.

Explainability is a feature.

A working system that cannot be understood is incomplete.
