# Commit Guidelines

## 1. Branch Naming Convention

- Always create a new branch for your work.
- Use the format:

  ``` text
  <user-name>/<type-of-commit>/<name-of-commit>
  ```

  - **user-name**: Your username (for tracking who made the change).
  - **type-of-commit**: One of `feature`, `fix`, or `refactor`.
  - **name-of-commit**: A brief, descriptive name for the change (use hyphens to separate words).
- **Example:**

  ``` text
  john/feature/websocket-reconnect
  alice/fix/client-error-handling
  bob/refactor/test-structure
  ```

## 2. Staging Changes

- **Always add only the files you have changed.**  
  Avoid using `git add .` or `git add -A` as it may include unintended files.
- Use:

  ``` text
  git add <file1> <file2> ...
  ```

- Review your changes with `git status` and `git diff` before committing.

## 3. Commit Message and Description

- **Commit message** should be clear, concise, and self-explanatory.
  - Use the imperative mood (e.g., “Add reconnect logic to client”).
  - Keep the subject line under 50 characters if possible.
- **Description** (body) should provide additional context if needed:
  - What was changed and why.
  - Any relevant background or links to issues/tickets.
  - Steps to reproduce or test, if applicable.

## 4. Atomic Commits

- Each commit should represent a single logical change.
- Avoid bundling unrelated changes in one commit.

## 5. Test and Lint Before Commit

- **Unit testing is mandatory before committing any changes.**
- **There should be no linting errors or warnings when committing changes.**
- Run all relevant tests before committing.
- Run a linter (e.g., flake8, pylint, black, isort) and resolve all errors and warnings.
- Ensure your changes do not break existing functionality.

## 6. Logging

- **Add detailed logging wherever possible to aid debugging and monitoring.**
- Use appropriate log levels (info, warning, error, debug) for different types of messages.
- A standard logging module will be set up in the future; for now, use Python's built-in `logging` module or clear print statements as placeholders.

## 7. Reference Issues or PRs (if applicable)

- If your commit addresses a GitHub issue or relates to a PR, reference it in the description (e.g., “Fixes #42”).

## 8. Write Meaningful Commit Messages

- Avoid generic messages like “update”, “fix”, or “changes”.
- Be specific about what and why.

## 9. Avoid Committing Sensitive Data

- Double-check that you are not committing secrets, credentials, or large files that should be ignored.

## 10. Do not forget to publish the branch, if you are creating it for the first time

- After creating a new branch for a requirement or feature, you must publish it to the remote repository before raising a PR or collaborating with others.
- Use one of the following commands to publish your branch for the first time:
  
  ```bash
  git push -u origin <branch-name>
  # or equivalently
  git push --set-upstream origin <branch-name>
  ```
  
- Replace `<branch-name>` with your actual branch name (e.g., `jayadev/feature/REQ-4-logging-config-setup`).
- This step is required only the first time you push a new branch. Subsequent pushes can use `git push`.

---

## Example Workflow

```bash
# Create a branch
git checkout -b john/feature/websocket-reconnect

# Make changes, then add only the files you changed
git add app/ws/client.py tests/test_ws_client.py

# Add detailed logging where appropriate
# (Use logging module or print statements as needed)

# Run unit tests (MANDATORY)
make test

# Run linter and fix all errors/warnings (MANDATORY)
flake8 .
# or
pylint app/ tests/
# or
black --check .

# Commit with a clear message and description
git commit -m "Add reconnect logic to WebSocket client

- Implements automatic reconnection on connection loss.
- Updates client to handle server restarts gracefully.
- Related to #123."
```
