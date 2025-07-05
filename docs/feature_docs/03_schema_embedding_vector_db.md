# Requirement Document

## Title

Schema Embedding & Vector DB Integration

## Author

jayadev

## Date

2024-06-11

## Background / Context

Semantic search over schema elements enables intelligent mapping from business terms to technical schema. Embeddings and vector DB integration are foundational for this capability.

## Objective

Generate vector embeddings for schema elements and store them in a vector database. Provide an API to query schema elements semantically.

## Scope

Included:
- Embedding generation for tables, columns, docs
- Integration with Chroma or Pinecone
- API for semantic schema queries
- Unit and integration tests

Excluded:
- Full NL-to-SQL translation
- Downstream agent integration

## Functional Requirements

- Generate embeddings for schema elements
- Store embeddings in vector DB
- Provide API endpoint for semantic search
- All logic must be tested

## Non-Functional Requirements (if any)

- Embedding and search must be performant
- Code must be modular and testable

## Acceptance Criteria

- Embeddings are generated and stored for sample schema
- Semantic search API returns relevant results
- All tests pass

## Dependencies / Impact

- Schema metadata from previous task
- Vector DB setup

## Additional Notes

This enables semantic mapping for query translation in later phases. 