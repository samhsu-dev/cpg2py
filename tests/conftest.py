"""
Shared fixtures and test utilities for cpg2py tests.
"""
import tempfile
from pathlib import Path
from typing import Generator, List, Tuple

import pytest

from cpg2py._abc import Storage
from cpg2py._cpg import CpgGraph


@pytest.fixture
def storage() -> Storage:
    """Fresh Storage instance per test."""
    return Storage()


@pytest.fixture
def graph(storage: Storage) -> CpgGraph:
    """Provides a CpgGraph backed by the given storage."""
    return CpgGraph(storage)


@pytest.fixture
def storage_with_single_edge(storage: Storage) -> Storage:
    """Storage with two nodes and one edge (node1, node2, TYPE)."""
    storage.add_node("node1")
    storage.add_node("node2")
    storage.add_edge(("node1", "node2", "TYPE"))
    return storage


@pytest.fixture
def graph_with_single_edge(storage_with_single_edge: Storage) -> CpgGraph:
    """CpgGraph with two nodes and one edge (node1, node2, TYPE)."""
    return CpgGraph(storage_with_single_edge)


@pytest.fixture
def sample_nodes() -> List[str]:
    """Sample node IDs for tests."""
    return ["node1", "node2", "node3"]


@pytest.fixture
def sample_edges() -> List[Tuple[str, str, str]]:
    """Sample edge tuples (from_node, to_node, edge_type)."""
    return [
        ("node1", "node2", "TYPE1"),
        ("node1", "node3", "TYPE2"),
        ("node3", "node2", "TYPE1"),
    ]


@pytest.fixture
def populated_storage(
    storage: Storage,
    sample_nodes: List[str],
    sample_edges: List[Tuple[str, str, str]],
) -> Storage:
    """Storage with sample_nodes and sample_edges added."""
    for node_id in sample_nodes:
        storage.add_node(node_id)
    for edge_id in sample_edges:
        storage.add_edge(edge_id)
    return storage


@pytest.fixture
def populated_graph(populated_storage: Storage) -> CpgGraph:
    """CpgGraph with sample nodes and edges."""
    return CpgGraph(populated_storage)


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Temporary directory for file-based tests; auto-cleaned."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_node_csv(temp_dir: Path) -> Path:
    """Path to a sample node CSV for integration tests."""
    node_csv = temp_dir / "nodes.csv"
    with open(node_csv, "w", encoding="utf-8") as f:
        f.write("id:int\tname\ttype\n")
        f.write("1\tnode1\tAST\n")
        f.write("2\tnode2\tAST\n")
    return node_csv


@pytest.fixture
def sample_edge_csv(temp_dir: Path) -> Path:
    """Path to a sample edge CSV for integration tests."""
    edge_csv = temp_dir / "edges.csv"
    with open(edge_csv, "w", encoding="utf-8") as f:
        f.write("start\tend\ttype\n")
        f.write("1\t2\tPARENT_OF\n")
    return edge_csv
