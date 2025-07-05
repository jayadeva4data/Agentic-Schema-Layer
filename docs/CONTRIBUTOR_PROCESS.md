# Contributor Process Guidelines

This document outlines the required process for all contributors to this project, ensuring clarity, traceability, and high-quality contributions.

---

## 1. Requirement Document Preparation

- **Start by creating a requirement document** using the template in `docs/feature_docs/REQUIREMENT_TEMPLATE.md`.
- **Location:**
  - Create a new folder for your requirement under `docs/feature_docs/` named as `REQ-<id>-<short-title>/` (e.g., `REQ-123-websocket-reconnect`).
  - Place your filled requirement document as `requirement.md` in this folder.
- **Approval:**
  - The requirement document must be reviewed and approved by the team before any development begins.

## 2. Development Process

- **Branching:**
  - Create a new branch using the convention: `<user-name>/<type-of-commit>/<REQ-id>-<short-title>`
    - Example: `john/feature/REQ-123-websocket-reconnect`
- **Implementation:**
  - Develop the feature or fix as per the approved requirement.
  - Keep your changes focused and atomic.

## 3. Committing Changes

- **Follow the commit guidelines in `docs/COMMIT_GUIDELINES.md`.**
- **Reference the requirement:**
  - Mention the requirement ID in your commit messages (e.g., `Implements REQ-123: Add reconnect logic`).
- **Unit testing is mandatory before every commit.**
- **Stage only the files you have changed.**

## 4. Raising a Pull Request

- **PR Description:**
  - Use the PR template in your requirement folder (copy from `docs/feature_docs/pr_template.md` if needed).
  - Save the PR description as `pr_description.md` in the same requirement folder.
  - Reference the requirement document in your PR description (e.g., "See requirement: `docs/feature_docs/REQ-123-websocket-reconnect/requirement.md`").
- **Review:**
  - PR must be reviewed and approved by at least one other team member before merging.

## 5. Organizing Files

- **All artifacts related to a requirement should be in the same folder:**
  - `docs/feature_docs/REQ-<id>-<short-title>/`
    - `requirement.md` (the requirement document)
    - `pr_description.md` (the PR description)
    - Any related design diagrams, notes, or supporting files

## 6. Example Workflow

```bash
# 1. Prepare requirement doc and get approval
mkdir -p docs/feature_docs/REQ-123-websocket-reconnect
cp docs/feature_docs/REQUIREMENT_TEMPLATE.md docs/feature_docs/REQ-123-websocket-reconnect/requirement.md
# (Fill out and get approval)

# 2. Create branch
git checkout -b john/feature/REQ-123-websocket-reconnect

# 3. Develop, test, and commit
# (Make changes, run tests, commit with reference to REQ-123)

# 4. Prepare PR description
cp docs/feature_docs/pr_template.md docs/feature_docs/REQ-123-websocket-reconnect/pr_description.md
# (Fill out PR description)

# 5. Raise PR referencing the requirement doc
# (Use the PR description file and reference the requirement doc path)
```

---

**Following this process ensures every change is well-documented, reviewed, and traceable from requirement to implementation.**
