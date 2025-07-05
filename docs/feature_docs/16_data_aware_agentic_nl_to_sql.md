# Requirement Document

## Title

Data-Aware Agentic NL-to-SQL

## Author

jayadev

## Date

2024-06-12

## Background / Context

LLM-only NL-to-SQL systems are limited by their lack of data awareness: they know the schema, but not the actual values in the data. This leads to issues with value aliases, typos, synonyms, and ambiguous queries. To address this, we propose a set of agentic components that make the NL-to-SQL system data-aware, robust, and user-friendly.

## Objective

Implement a set of agents that augment the NL-to-SQL pipeline with data awareness, including value sampling, alias/synonym mapping, fuzzy matching, interactive clarification, and feedback learning.

## Scope

Included:
- Value Sampling Agent: Profiles column values and augments LLM prompts with real data samples.
- Alias & Synonym Agent: Maintains and applies mappings from business/user terms to canonical values.
- Fuzzy Matching Agent: Applies fuzzy matching to user-provided values for robust filtering.
- Interactive Clarification Agent: Engages users in dialog to resolve ambiguity or errors.
- Feedback Loop Agent: Incorporates user feedback to improve value mapping and synonym dictionaries.
- Integration with existing NL-to-SQL and schema agents.
- Unit and integration tests for all agents.

Excluded:
- Full query execution and result retrieval.
- Downstream analytics or visualization.

## Functional Requirements

- Value Sampling Agent must sample and cache representative values for relevant columns.
- Alias & Synonym Agent must map user/business terms to canonical values and be updatable.
- Fuzzy Matching Agent must match user input to closest known value using string similarity.
- Interactive Clarification Agent must detect ambiguity and prompt the user for clarification.
- Feedback Loop Agent must learn from user corrections and update mappings.
- Agents must be orchestratable in a pipeline and independently testable.

## Non-Functional Requirements

- Agents must be modular, extensible, and performant.
- Value sampling must not overload the database.
- User interactions must be clear and minimize friction.

## Acceptance Criteria

- NL-to-SQL queries with value aliases, typos, or synonyms are correctly mapped to valid SQL.
- Ambiguous queries trigger clarification dialogs.
- User feedback is incorporated into future queries.
- All agent logic is covered by tests.

## Dependencies / Impact

- Existing schema and NL-to-SQL agents.
- Database access for value sampling.

## Additional Notes

This agentic system will make NL-to-SQL robust for real-world, messy user input and evolving business language. 