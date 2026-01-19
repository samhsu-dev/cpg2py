# Test Suite for cpg2py

This directory contains the test suite for the cpg2py package, following the testing standards defined in `.cursor/rules/testing.instructions.mdc`.

## Layout Profile

This project uses **Profile B**: `tests/` root directory with files named `test_<component>.<ext>`.

## Test Structure

- `test_storage.py`: Unit tests for Storage class (graph structure and properties)
- `test_graph.py`: Unit and integration tests for Graph class and graph query operations
- `test_node.py`: Unit tests for Node class and node properties
- `test_edge.py`: Unit tests for Edge class and edge properties
- `test_exceptions.py`: Unit tests for custom exception classes
- `conftest.py`: Shared fixtures and test utilities

## Running Tests

### Prerequisites

Install development dependencies:

```bash
uv sync --dev
```

### Unit Tests (Default)

Run all unit tests:

```bash
uv run pytest tests/ -m unit
```

Or simply (unit tests are the default):

```bash
uv run pytest tests/
```

### Integration Tests

Run integration tests separately:

```bash
uv run pytest tests/ -m integration
```

### All Tests

Run both unit and integration tests:

```bash
uv run pytest tests/ -m "unit or integration"
```

### Specific Test Files

Run a specific test file:

```bash
uv run pytest tests/test_storage.py
```

### With Coverage

Run tests with coverage report:

```bash
uv run pytest tests/ --cov=cpg2py --cov-report=html --cov-report=term
```

Coverage threshold is set to ≥90% in `pyproject.toml`. The build will fail if coverage drops below this threshold.

### Verbose Output

Run with verbose output:

```bash
uv run pytest tests/ -v
```

### Stop on First Failure

Run with stop-on-first-failure mode for debugging:

```bash
uv run pytest tests/ -x
```

### Parallel Execution

Run tests in parallel (if pytest-xdist is installed):

```bash
uv run pytest tests/ -n auto
```

## Test Organization

### Unit Tests

Unit tests are isolated from external systems and test a single unit per test file. They are marked with `@pytest.mark.unit`.

- Test individual components in isolation
- Use fixtures for setup
- Follow Arrange → Act → Assert pattern
- One behavior per test case
- Naming: `test_<component>_<condition>_<expected>`

### Integration Tests

Integration tests involve cross-module or external interactions (e.g., file I/O). They are marked with `@pytest.mark.integration`.

- Test interactions between components
- Use temporary resources for file operations
- Run separately from unit tests

## Test Coverage

The test suite covers:

- Node and edge creation and management
- Graph traversal operations (successors, predecessors, children, parents)
- Property access and manipulation
- Exception handling
- CSV file loading via `cpg_graph` factory function

## Fixtures

Shared fixtures are defined in `conftest.py`:

- `storage`: Fresh Storage instance
- `graph`: Graph instance backed by Storage
- `sample_nodes`: Sample node data
- `sample_edges`: Sample edge data
- `populated_storage`: Storage with sample data
- `populated_graph`: Graph with sample data
- `temp_dir`: Temporary directory for file-based tests
- `sample_node_csv`: Sample node CSV file
- `sample_edge_csv`: Sample edge CSV file

## Test Standards

All tests follow these standards:

1. **Structure**: Arrange → Act → Assert pattern
2. **Naming**: `test_<component>_<condition>_<expected>`
3. **Isolation**: Tests are independent with no shared mutable state
4. **Assertions**: One focused assertion per test (or multiple when verifying a single behavior)
5. **Fixtures**: Centralized reusable setup via fixtures
6. **Coverage**: Target ≥90% for statements/branches
