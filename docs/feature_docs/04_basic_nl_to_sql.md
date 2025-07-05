# Requirement Document

## Title

Basic NL-to-SQL Translation

## Author

jayadev

## Date

2024-06-11

## Background / Context

Translating natural language queries to SQL is a core capability of the semantic layer. A basic agent using schema metadata will enable initial end-to-end query flows.

## Objective

Implement a simple agent that maps natural language queries to SQL using schema metadata.

## Scope

Included:
- NL-to-SQL translation using schema metadata
- Use of LangChain for prompt management
- Unit and integration tests

Excluded:
- Advanced ambiguity resolution
- Multi-agent orchestration

## Functional Requirements

- Parse natural language queries
- Map business terms to schema elements
- Generate SQL queries
- All logic must be tested

## Non-Functional Requirements (if any)

- Translation must be accurate for basic queries
- Code must be modular and testable

## Acceptance Criteria

- NL queries are translated to correct SQL for sample cases
- All tests pass

## Dependencies / Impact

- Schema metadata and embeddings

## Additional Notes

This is the first step towards a fully agentic query translation pipeline. 