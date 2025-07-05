# Requirement Document

## Title

Schema Parser MVP

## Author

jayadev

## Date

2024-06-11

## Background / Context

Understanding the database schema, relationships, and business context is essential for semantic query translation. Parsing dbt models, macros, and documentation provides the necessary metadata for downstream agents.

## Objective

Implement a parser that extracts tables, columns, relationships, and business terms from dbt models, macros, and documentation, and stores them in a structured format.

## Scope

Included:
- Parsing dbt models, macros, and docs
- Extracting tables, columns, relationships, business terms
- Storing metadata in JSON/YAML/DB
- Unit tests for all parsing logic

Excluded:
- Downstream agent integration
- Vector embedding generation

## Functional Requirements

- Parse dbt models to extract schema elements
- Parse dbt macros and documentation for business terms
- Build a structured metadata representation
- Provide a function to export metadata
- All parsing logic must be unit tested

## Non-Functional Requirements (if any)

- Parsing must handle errors gracefully
- Code must be modular and testable

## Acceptance Criteria

- Parser extracts correct schema metadata from sample dbt project
- Metadata is exported in structured format
- All tests pass

## Dependencies / Impact

- dbt project structure

## Additional Notes

This metadata will be used for semantic search and query translation in later phases. 