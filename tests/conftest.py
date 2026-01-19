"""
Shared fixtures and test utilities for cpg2py tests.
"""
import tempfile
from pathlib import Path

import pytest

from cpg2py._abc import Storage
from cpg2py._cpg import CpgGraph


@pytest.fixture
def storage():
    """
    Provides a fresh Storage instance for each test.

    Returns:
        Storage: A new Storage instance
    """
    return Storage()


@pytest.fixture
def graph(storage):
    """
    Provides a Graph instance backed by a Storage for each test.

    Args:
        storage: Storage fixture

    Returns:
        CpgGraph: A new Graph instance
    """
    return CpgGraph(storage)


@pytest.fixture
def sample_nodes():
    """
    Provides sample node data for tests.

    Returns:
        list: List of node IDs
    """
    return ["node1", "node2", "node3"]


@pytest.fixture
def sample_edges():
    """
    Provides sample edge data for tests.

    Returns:
        list: List of edge tuples (from_node, to_node, edge_type)
    """
    return [
        ("node1", "node2", "TYPE1"),
        ("node1", "node3", "TYPE2"),
        ("node3", "node2", "TYPE1"),
    ]


@pytest.fixture
def populated_storage(storage, sample_nodes, sample_edges):
    """
    Provides a Storage instance with sample nodes and edges.

    Args:
        storage: Storage fixture
        sample_nodes: Sample node IDs fixture
        sample_edges: Sample edges fixture

    Returns:
        Storage: Storage instance with nodes and edges added
    """
    for node_id in sample_nodes:
        storage.add_node(node_id)
    for edge_id in sample_edges:
        storage.add_edge(edge_id)
    return storage


@pytest.fixture
def populated_graph(populated_storage):
    """
    Provides a Graph instance with sample nodes and edges.

    Args:
        populated_storage: Populated Storage fixture

    Returns:
        CpgGraph: Graph instance with nodes and edges
    """
    return CpgGraph(populated_storage)


@pytest.fixture
def temp_dir():
    """
    Provides a temporary directory for file-based tests.

    Yields:
        Path: Temporary directory path
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_node_csv(temp_dir):
    """
    Creates a sample node CSV file for integration tests.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to the created node CSV file
    """
    node_csv = temp_dir / "nodes.csv"
    with open(node_csv, "w", encoding="utf-8") as f:
        f.write("id:int\tname\ttype\n")
        f.write("1\tnode1\tAST\n")
        f.write("2\tnode2\tAST\n")
    return node_csv


@pytest.fixture
def sample_edge_csv(temp_dir):
    """
    Creates a sample edge CSV file for integration tests.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to the created edge CSV file
    """
    edge_csv = temp_dir / "edges.csv"
    with open(edge_csv, "w", encoding="utf-8") as f:
        f.write("start\tend\ttype\n")
        f.write("1\t2\tPARENT_OF\n")
    return edge_csv
