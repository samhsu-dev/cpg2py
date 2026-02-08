"""
Unit tests for Storage class.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cpg2py import storage_from_json
from cpg2py._abc import Storage


@pytest.mark.unit
class TestStorage:
    """Test cases for Storage class."""

    def test_storage_init_creates_empty_graph(self, storage: Storage) -> None:
        """
        Tests that Storage initialization creates an empty graph.

        Arrange: Create a new Storage instance
        Act: Check initial state
        Assert: Graph has no nodes or edges
        """
        assert storage is not None
        assert len(list(storage.get_nodes())) == 0
        assert len(list(storage.get_edges())) == 0

    def test_storage_add_node_adds_new_node(self, storage: Storage) -> None:
        """
        Tests that adding a new node succeeds.

        Arrange: Empty storage
        Act: Add a node
        Assert: Node is added and exists
        """
        result = storage.add_node("node1")
        assert result is True
        assert storage.contains_node("node1") is True

    def test_storage_add_node_duplicate_returns_false(self, storage: Storage) -> None:
        """
        Tests that adding a duplicate node returns False.

        Arrange: Storage with existing node
        Act: Add the same node again
        Assert: Returns False, node count unchanged
        """
        storage.add_node("node1")
        result = storage.add_node("node1")
        assert result is False
        assert len(list(storage.get_nodes())) == 1

    def test_storage_add_node_multiple_adds_all_nodes(self, storage: Storage) -> None:
        """
        Tests that multiple nodes can be added.

        Arrange: Empty storage
        Act: Add multiple nodes
        Assert: All nodes are added
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        assert len(list(storage.get_nodes())) == 3

    def test_storage_contains_node_returns_true_for_existing(self, storage: Storage) -> None:
        """
        Tests that contains_node returns True for existing nodes.

        Arrange: Storage with a node
        Act: Check if node exists
        Assert: Returns True
        """
        storage.add_node("node1")
        assert storage.contains_node("node1") is True

    def test_storage_contains_node_returns_false_for_missing(self, storage: Storage) -> None:
        """
        Tests that contains_node returns False for missing nodes.

        Arrange: Empty storage
        Act: Check if non-existent node exists
        Assert: Returns False
        """
        assert storage.contains_node("node1") is False

    def test_storage_add_edge_adds_new_edge(self, storage: Storage) -> None:
        """
        Tests that adding a new edge succeeds.

        Arrange: Storage with source and target nodes
        Act: Add an edge
        Assert: Edge is added and exists
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "EDGE_TYPE")
        result = storage.add_edge(edge_id)
        assert result is True
        assert storage.contains_edge(edge_id) is True

    def test_storage_add_edge_duplicate_returns_false(self, storage: Storage) -> None:
        """
        Tests that adding a duplicate edge returns False.

        Arrange: Storage with existing edge
        Act: Add the same edge again
        Assert: Returns False
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "EDGE_TYPE")
        storage.add_edge(edge_id)
        result = storage.add_edge(edge_id)
        assert result is False

    def test_storage_add_edge_missing_source_returns_false(self, storage: Storage) -> None:
        """
        Tests that adding edge with missing source node returns False.

        Arrange: Storage without source node
        Act: Add edge with missing source
        Assert: Returns False
        """
        storage.add_node("node2")
        edge_id = ("node1", "node2", "EDGE_TYPE")
        result = storage.add_edge(edge_id)
        assert result is False

    def test_storage_add_edge_missing_target_returns_false(self, storage: Storage) -> None:
        """
        Tests that adding edge with missing target node returns False.

        Arrange: Storage without target node
        Act: Add edge with missing target
        Assert: Returns False
        """
        storage.add_node("node1")
        edge_id = ("node1", "node2", "EDGE_TYPE")
        result = storage.add_edge(edge_id)
        assert result is False

    def test_storage_out_edges_returns_all_outgoing_edges(self, storage: Storage) -> None:
        """
        Tests that out_edges returns all outgoing edges for a node.

        Arrange: Storage with multiple outgoing edges
        Act: Get outgoing edges
        Assert: All outgoing edges are returned
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        edge1 = ("node1", "node2", "TYPE1")
        edge2 = ("node1", "node3", "TYPE2")
        storage.add_edge(edge1)
        storage.add_edge(edge2)
        out_edges = list(storage.out_edges("node1"))
        assert len(out_edges) == 2
        assert edge1 in out_edges
        assert edge2 in out_edges

    def test_storage_in_edges_returns_all_incoming_edges(self, storage: Storage) -> None:
        """
        Tests that in_edges returns all incoming edges for a node.

        Arrange: Storage with multiple incoming edges
        Act: Get incoming edges
        Assert: All incoming edges are returned
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        edge1 = ("node1", "node2", "TYPE1")
        edge2 = ("node3", "node2", "TYPE2")
        storage.add_edge(edge1)
        storage.add_edge(edge2)
        in_edges = list(storage.in_edges("node2"))
        assert len(in_edges) == 2
        assert edge1 in in_edges
        assert edge2 in in_edges

    def test_storage_successors_returns_all_successor_nodes(self, storage: Storage) -> None:
        """
        Tests that successors returns all successor nodes.

        Arrange: Storage with multiple successors
        Act: Get successors
        Assert: All successor nodes are returned
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        storage.add_edge(("node1", "node2", "TYPE1"))
        storage.add_edge(("node1", "node3", "TYPE2"))
        successors = list(storage.successors("node1"))
        assert len(successors) == 2
        assert "node2" in successors
        assert "node3" in successors

    def test_storage_predecessors_returns_all_predecessor_nodes(self, storage: Storage) -> None:
        """
        Tests that predecessors returns all predecessor nodes.

        Arrange: Storage with multiple predecessors
        Act: Get predecessors
        Assert: All predecessor nodes are returned
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        storage.add_edge(("node1", "node2", "TYPE1"))
        storage.add_edge(("node3", "node2", "TYPE2"))
        predecessors = list(storage.predecessors("node2"))
        assert len(predecessors) == 2
        assert "node1" in predecessors
        assert "node3" in predecessors

    def test_storage_set_node_props_sets_properties(self, storage: Storage) -> None:
        """
        Tests that set_node_props sets node properties.

        Arrange: Storage with a node
        Act: Set node properties
        Assert: Properties are set correctly
        """
        storage.add_node("node1")
        props = {"name": "test", "type": "AST"}
        result = storage.set_node_props("node1", props)
        assert result is True
        node_props = storage.get_node_props("node1")
        assert node_props["name"] == "test"
        assert node_props["type"] == "AST"

    def test_storage_set_node_props_nonexistent_returns_false(self, storage: Storage) -> None:
        """
        Tests that set_node_props returns False for nonexistent node.

        Arrange: Empty storage
        Act: Set properties for non-existent node
        Assert: Returns False
        """
        props = {"name": "test"}
        result = storage.set_node_props("node1", props)
        assert result is False

    def test_storage_get_node_props_returns_properties(self, storage: Storage) -> None:
        """
        Tests that get_node_props returns node properties.

        Arrange: Storage with node and properties
        Act: Get node properties
        Assert: Properties are returned correctly
        """
        storage.add_node("node1")
        props = {"name": "test", "type": "AST"}
        storage.set_node_props("node1", props)
        retrieved_props = storage.get_node_props("node1")
        assert retrieved_props is not None
        assert retrieved_props["name"] == "test"

    def test_storage_get_node_props_nonexistent_returns_none(self, storage: Storage) -> None:
        """
        Tests that get_node_props returns None for nonexistent node.

        Arrange: Empty storage
        Act: Get properties for non-existent node
        Assert: Returns None
        """
        props = storage.get_node_props("node1")
        assert props is None

    def test_storage_set_node_prop_sets_single_property(self, storage: Storage) -> None:
        """
        Tests that set_node_prop sets a single property.

        Arrange: Storage with a node
        Act: Set single property
        Assert: Property is set correctly
        """
        storage.add_node("node1")
        result = storage.set_node_prop("node1", "name", "test")
        assert result is True
        value = storage.get_node_prop("node1", "name")
        assert value == "test"

    def test_storage_get_node_prop_returns_property_value(self, storage: Storage) -> None:
        """
        Tests that get_node_prop returns property value.

        Arrange: Storage with node and property
        Act: Get property value
        Assert: Correct value is returned
        """
        storage.add_node("node1")
        storage.set_node_prop("node1", "name", "test")
        value = storage.get_node_prop("node1", "name")
        assert value == "test"

    def test_storage_get_node_prop_nonexistent_returns_none(self, storage: Storage) -> None:
        """
        Tests that get_node_prop returns None for nonexistent property.

        Arrange: Empty storage
        Act: Get property from non-existent node
        Assert: Returns None
        """
        value = storage.get_node_prop("node1", "name")
        assert value is None

    def test_storage_set_edge_props_sets_properties(self, storage: Storage) -> None:
        """
        Tests that set_edge_props sets edge properties.

        Arrange: Storage with an edge
        Act: Set edge properties
        Assert: Properties are set correctly
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "TYPE")
        storage.add_edge(edge_id)
        props = {"weight": 1.0, "label": "test"}
        result = storage.set_edge_props(edge_id, props)
        assert result is True
        edge_props = storage.get_edge_props(edge_id)
        assert edge_props["weight"] == 1.0
        assert edge_props["label"] == "test"

    def test_storage_set_edge_props_nonexistent_returns_false(self, storage: Storage) -> None:
        """
        Tests that set_edge_props returns False for nonexistent edge.

        Arrange: Empty storage
        Act: Set properties for non-existent edge
        Assert: Returns False
        """
        props = {"weight": 1.0}
        edge_id = ("node1", "node2", "TYPE")
        result = storage.set_edge_props(edge_id, props)
        assert result is False

    def test_storage_get_edge_props_returns_properties(self, storage: Storage) -> None:
        """
        Tests that get_edge_props returns edge properties.

        Arrange: Storage with edge and properties
        Act: Get edge properties
        Assert: Properties are returned correctly
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "TYPE")
        storage.add_edge(edge_id)
        props = {"weight": 1.0}
        storage.set_edge_props(edge_id, props)
        retrieved_props = storage.get_edge_props(edge_id)
        assert retrieved_props is not None
        assert retrieved_props["weight"] == 1.0

    def test_storage_set_edge_prop_sets_single_property(self, storage: Storage) -> None:
        """
        Tests that set_edge_prop sets a single property.

        Arrange: Storage with an edge
        Act: Set single property
        Assert: Property is set correctly
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "TYPE")
        storage.add_edge(edge_id)
        result = storage.set_edge_prop(edge_id, "weight", 1.0)
        assert result is True
        value = storage.get_edge_prop(edge_id, "weight")
        assert value == 1.0

    def test_storage_get_edge_prop_returns_property_value(self, storage: Storage) -> None:
        """
        Tests that get_edge_prop returns property value.

        Arrange: Storage with edge and property
        Act: Get property value
        Assert: Correct value is returned
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "TYPE")
        storage.add_edge(edge_id)
        storage.set_edge_prop(edge_id, "weight", 1.0)
        value = storage.get_edge_prop(edge_id, "weight")
        assert value == 1.0

    def test_storage_remove_node_removes_node(self, storage: Storage) -> None:
        """
        Tests that remove_node removes a node.

        Arrange: Storage with a node
        Act: Remove node
        Assert: Node is removed
        """
        storage.add_node("node1")
        result = storage.remove_node("node1")
        assert result is True
        assert storage.contains_node("node1") is False

    def test_storage_remove_node_nonexistent_returns_false(self, storage: Storage) -> None:
        """
        Tests that remove_node returns False for nonexistent node.

        Arrange: Empty storage
        Act: Remove non-existent node
        Assert: Returns False
        """
        result = storage.remove_node("node1")
        assert result is False

    def test_storage_remove_edge_removes_edge(self, storage: Storage) -> None:
        """
        Tests that remove_edge removes an edge.

        Arrange: Storage with an edge
        Act: Remove edge
        Assert: Edge is removed
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "TYPE")
        storage.add_edge(edge_id)
        result = storage.remove_edge(edge_id)
        assert result is True
        assert storage.contains_edge(edge_id) is False

    def test_storage_remove_edge_nonexistent_returns_false(self, storage: Storage) -> None:
        """
        Tests that remove_edge returns False for nonexistent edge.

        Arrange: Empty storage
        Act: Remove non-existent edge
        Assert: Returns False
        """
        edge_id = ("node1", "node2", "TYPE")
        result = storage.remove_edge(edge_id)
        assert result is False

    def test_storage_get_nodes_empty_returns_empty_iterable(self, storage: Storage) -> None:
        """
        Tests that get_nodes on empty storage returns empty iterable.

        Arrange: Empty storage
        Act: Get all nodes
        Assert: Empty list
        """
        nodes = list(storage.get_nodes())
        assert nodes == []

    def test_storage_get_nodes_returns_all_nodes(self, storage: Storage) -> None:
        """
        Tests that get_nodes returns all nodes.

        Arrange: Storage with multiple nodes
        Act: Get all nodes
        Assert: All nodes are returned
        """
        storage.add_node("node1")
        storage.add_node("node2")
        nodes = list(storage.get_nodes())
        assert len(nodes) == 2
        assert "node1" in nodes
        assert "node2" in nodes

    def test_storage_get_edges_empty_returns_empty_iterable(self, storage: Storage) -> None:
        """
        Tests that get_edges on empty storage returns empty iterable.

        Arrange: Empty storage
        Act: Get all edges
        Assert: Empty list
        """
        edges = list(storage.get_edges())
        assert edges == []

    def test_storage_out_edges_nonexistent_node_returns_empty(self, storage: Storage) -> None:
        """
        Tests that out_edges for nonexistent node returns empty iterable.

        Arrange: Storage without the node
        Act: out_edges for missing node
        Assert: Empty list
        """
        out = list(storage.out_edges("nonexistent"))
        assert out == []

    def test_storage_in_edges_nonexistent_node_returns_empty(self, storage: Storage) -> None:
        """
        Tests that in_edges for nonexistent node returns empty iterable.

        Arrange: Storage without the node
        Act: in_edges for missing node
        Assert: Empty list
        """
        inc = list(storage.in_edges("nonexistent"))
        assert inc == []

    def test_storage_successors_nonexistent_node_returns_empty(self, storage: Storage) -> None:
        """
        Tests that successors for nonexistent node returns empty iterable.

        Arrange: Storage without the node
        Act: successors for missing node
        Assert: Empty list
        """
        succ = list(storage.successors("nonexistent"))
        assert succ == []

    def test_storage_predecessors_nonexistent_node_returns_empty(self, storage: Storage) -> None:
        """
        Tests that predecessors for nonexistent node returns empty iterable.

        Arrange: Storage without the node
        Act: predecessors for missing node
        Assert: Empty list
        """
        pred = list(storage.predecessors("nonexistent"))
        assert pred == []

    def test_storage_set_node_props_empty_dict_succeeds(self, storage: Storage) -> None:
        """
        Tests that set_node_props with empty dict does not fail.

        Arrange: Storage with a node
        Act: set_node_props with {}
        Assert: Returns True, node still exists
        """
        storage.add_node("n1")
        result = storage.set_node_props("n1", {})
        assert result is True
        assert storage.contains_node("n1")

    def test_storage_set_edge_props_empty_dict_succeeds(self, storage: Storage) -> None:
        """
        Tests that set_edge_props with empty dict does not fail.

        Arrange: Storage with an edge
        Act: set_edge_props with {}
        Assert: Returns True, edge still exists
        """
        storage.add_node("a")
        storage.add_node("b")
        eid = ("a", "b", "T")
        storage.add_edge(eid)
        result = storage.set_edge_props(eid, {})
        assert result is True
        assert storage.contains_edge(eid)

    def test_storage_remove_node_clears_connected_edges_from_get_edges(
        self, storage: Storage
    ) -> None:
        """
        Tests that remove_node removes node and its edges from get_edges.

        Arrange: Storage with node and edges
        Act: remove_node
        Assert: get_edges no longer contains those edges
        """
        storage.add_node("n1")
        storage.add_node("n2")
        storage.add_edge(("n1", "n2", "E1"))
        storage.remove_node("n1")
        edges = list(storage.get_edges())
        assert ("n1", "n2", "E1") not in edges
        assert len(edges) == 0

    def test_storage_add_node_id_normalized_to_string(self, storage: Storage) -> None:
        """
        Tests that add_node accepts numeric-like id and stores as string.

        Arrange: Empty storage
        Act: add_node with int-like id, contains_node with string
        Assert: Node exists and is found by string key
        """
        storage.add_node(42)  # type: ignore[arg-type]
        assert storage.contains_node("42")
        nodes = list(storage.get_nodes())
        assert "42" in nodes

    def test_storage_add_edge_multiple_same_endpoints_different_type(
        self, storage: Storage
    ) -> None:
        """
        Tests that multiple edges same endpoints different type are all stored.

        Arrange: Two nodes
        Act: Add two edges (a,b,T1) and (a,b,T2)
        Assert: Both edges exist
        """
        storage.add_node("a")
        storage.add_node("b")
        assert storage.add_edge(("a", "b", "T1")) is True
        assert storage.add_edge(("a", "b", "T2")) is True
        edges = list(storage.get_edges())
        assert ("a", "b", "T1") in edges
        assert ("a", "b", "T2") in edges

    def test_storage_get_edges_returns_all_edges(self, storage: Storage) -> None:
        """
        Tests that get_edges returns all edges.

        Arrange: Storage with an edge
        Act: Get all edges
        Assert: All edges are returned
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "TYPE")
        storage.add_edge(edge_id)
        edges = list(storage.get_edges())
        assert len(edges) == 1
        assert edge_id in edges

    def test_storage_save_json_empty_graph_succeeds(self, storage: Storage, temp_dir: Path) -> None:
        """
        Tests that save_json on empty graph writes valid JSON and does not raise.

        Arrange: Empty storage
        Act: save_json to path
        Assert: File exists and load_json succeeds
        """
        path = temp_dir / "empty.json"
        storage.save_json(path)
        assert path.exists()
        other = Storage()
        other.load_json(path)
        assert list(other.get_nodes()) == []
        assert list(other.get_edges()) == []

    def test_storage_load_json_empty_nodes_and_edges_succeeds(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """
        Tests that load_json with empty nodes and edges clears and loads empty graph.

        Arrange: JSON with "nodes": {}, "edges": []
        Act: load_json
        Assert: get_nodes and get_edges are empty
        """
        path = temp_dir / "empty_graph.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"nodes": {}, "edges": []}')
        storage.load_json(path)
        assert list(storage.get_nodes()) == []
        assert list(storage.get_edges()) == []

    def test_storage_load_json_edge_without_props_key_uses_empty_props(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """
        Tests that load_json edge without "props" key is loaded with empty properties.

        Arrange: JSON edge object without "props"
        Act: load_json
        Assert: Edge exists, get_edge_props returns {} or None
        """
        path = temp_dir / "no_props.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                '{"nodes": {"1": {}, "2": {}}, ' '"edges": [{"from": "1", "to": "2", "type": "T"}]}'
            )
        storage.load_json(path)
        assert storage.contains_edge(("1", "2", "T"))
        assert storage.get_edge_props(("1", "2", "T")) == {}

    def test_storage_load_json_missing_nodes_key_raises(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """
        Tests that load_json with missing "nodes" key raises ValueError.

        Arrange: JSON with only "edges"
        Act: load_json
        Assert: ValueError
        """
        path = temp_dir / "no_nodes.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"edges": []}')
        with pytest.raises(ValueError, match="nodes.*edges"):
            storage.load_json(path)

    def test_storage_load_json_missing_edges_key_raises(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """
        Tests that load_json with missing "edges" key raises ValueError.

        Arrange: JSON with only "nodes"
        Act: load_json
        Assert: ValueError
        """
        path = temp_dir / "no_edges.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"nodes": {}}')
        with pytest.raises(ValueError, match="nodes.*edges"):
            storage.load_json(path)

    def test_storage_load_json_edge_missing_from_raises(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """
        Tests that load_json with edge missing "from" raises KeyError.

        Arrange: JSON edge without "from"
        Act: load_json
        Assert: KeyError
        """
        path = temp_dir / "bad_edge.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"nodes": {"1": {}, "2": {}}, ' '"edges": [{"to": "2", "type": "T"}]}')
        with pytest.raises(KeyError):
            storage.load_json(path)

    def test_storage_save_json_and_load_json_roundtrip(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """save_json and load_json roundtrip preserves nodes, edges, and properties."""
        storage.add_node("n1")
        storage.add_node("n2")
        storage.set_node_prop("n1", "name", "a")
        storage.add_edge(("n1", "n2", "CONNECTS"))
        storage.set_edge_prop(("n1", "n2", "CONNECTS"), "w", 1)
        path = temp_dir / "graph.json"
        storage.save_json(path)
        assert path.exists()
        other = Storage()
        other.load_json(path)
        assert other.contains_node("n1")
        assert other.contains_node("n2")
        assert other.get_node_prop("n1", "name") == "a"
        assert other.contains_edge(("n1", "n2", "CONNECTS"))
        assert other.get_edge_prop(("n1", "n2", "CONNECTS"), "w") == 1

    def test_storage_load_json_replaces_existing_graph(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """load_json replaces current graph with file contents."""
        storage.add_node("old")
        path = temp_dir / "graph.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"nodes": {"new": {}}, "edges": []}')
        storage.load_json(path)
        assert storage.contains_node("new") is True
        assert storage.contains_node("old") is False

    def test_storage_load_json_invalid_structure_raises(
        self, storage: Storage, temp_dir: Path
    ) -> None:
        """load_json raises ValueError when JSON lacks nodes or edges keys."""
        path = temp_dir / "bad.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write("{}")
        with pytest.raises(ValueError, match="nodes.*edges"):
            storage.load_json(path)

    def test_storage_from_json_creates_populated_storage(self, temp_dir: Path) -> None:
        """storage_from_json returns Storage populated from JSON file."""
        path = temp_dir / "graph.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                '{"nodes": {"1": {"name": "a"}, "2": {}}, '
                '"edges": [{"from": "1", "to": "2", "type": "T", "props": {"k": "v"}}]}'
            )
        storage = storage_from_json(path)
        assert storage.contains_node("1")
        assert storage.contains_node("2")
        assert storage.get_node_prop("1", "name") == "a"
        assert storage.contains_edge(("1", "2", "T"))
        assert storage.get_edge_prop(("1", "2", "T"), "k") == "v"

    def test_storage_from_json_nonexistent_path_raises(self, temp_dir: Path) -> None:
        """
        Tests that storage_from_json on nonexistent path raises OSError.

        Arrange: Path that does not exist
        Act: storage_from_json(path)
        Assert: FileNotFoundError or OSError
        """
        path = temp_dir / "does_not_exist.json"
        with pytest.raises((FileNotFoundError, OSError)):
            storage_from_json(path)
