"""
Unit tests for Edge class.
"""
from __future__ import annotations

import pytest

from cpg2py._abc import Storage
from cpg2py._cpg import CpgGraph


@pytest.mark.unit
class TestEdge:
    """Test cases for Edge class."""

    def test_edge_id_returns_edge_tuple(
        self, graph_with_single_edge: CpgGraph
    ) -> None:
        """
        Tests that edge.id returns the edge tuple.

        Arrange: Graph with nodes and edge
        Act: Get edge and access id property
        Assert: Returns correct edge tuple
        """
        edge_id = ("node1", "node2", "TYPE")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.id == edge_id

    def test_edge_start_returns_integer_with_primary_key(
        self,
        graph_with_single_edge: CpgGraph,
        storage_with_single_edge: Storage,
    ) -> None:
        """
        Tests that edge.start returns integer using primary key.

        Arrange: Graph with edge and start property
        Act: Get edge and access start property
        Assert: Returns correct integer value
        """
        edge_id = ("node1", "node2", "TYPE")
        storage_with_single_edge.set_edge_prop(edge_id, "start", "1")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.start == 1

    def test_edge_start_returns_integer_with_alternative_key(
        self,
        graph_with_single_edge: CpgGraph,
        storage_with_single_edge: Storage,
    ) -> None:
        """
        Tests that edge.start returns integer using alternative key.

        Arrange: Graph with edge and start:START_ID property
        Act: Get edge and access start property
        Assert: Returns correct integer value
        """
        edge_id = ("node1", "node2", "TYPE")
        storage_with_single_edge.set_edge_prop(edge_id, "start:START_ID", "1")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.start == 1

    def test_edge_end_returns_integer_with_primary_key(
        self,
        graph_with_single_edge: CpgGraph,
        storage_with_single_edge: Storage,
    ) -> None:
        """
        Tests that edge.end returns integer using primary key.

        Arrange: Graph with edge and end property
        Act: Get edge and access end property
        Assert: Returns correct integer value
        """
        edge_id = ("node1", "node2", "TYPE")
        storage_with_single_edge.set_edge_prop(edge_id, "end", "2")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.end == 2

    def test_edge_end_returns_integer_with_alternative_key(
        self,
        graph_with_single_edge: CpgGraph,
        storage_with_single_edge: Storage,
    ) -> None:
        """
        Tests that edge.end returns integer using alternative key.

        Arrange: Graph with edge and end:END_ID property
        Act: Get edge and access end property
        Assert: Returns correct integer value
        """
        edge_id = ("node1", "node2", "TYPE")
        storage_with_single_edge.set_edge_prop(edge_id, "end:END_ID", "2")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.end == 2

    def test_edge_type_returns_string_with_primary_key(
        self,
        graph_with_single_edge: CpgGraph,
        storage_with_single_edge: Storage,
    ) -> None:
        """
        Tests that edge.type returns string using primary key.

        Arrange: Graph with edge and type property
        Act: Get edge and access type property
        Assert: Returns correct string value
        """
        edge_id = ("node1", "node2", "TYPE")
        storage_with_single_edge.set_edge_prop(edge_id, "type", "PARENT_OF")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.type == "PARENT_OF"

    def test_edge_type_returns_string_with_alternative_key(
        self,
        graph_with_single_edge: CpgGraph,
        storage_with_single_edge: Storage,
    ) -> None:
        """
        Tests that edge.type returns string using alternative key.

        Arrange: Graph with edge and type:TYPE property
        Act: Get edge and access type property
        Assert: Returns correct string value
        """
        edge_id = ("node1", "node2", "TYPE")
        storage_with_single_edge.set_edge_prop(edge_id, "type:TYPE", "PARENT_OF")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.type == "PARENT_OF"

    def test_edge_var_returns_string(
        self,
        graph_with_single_edge: CpgGraph,
        storage_with_single_edge: Storage,
    ) -> None:
        """
        Tests that edge.var returns string.

        Arrange: Graph with edge and var property
        Act: Get edge and access var property
        Assert: Returns correct string value
        """
        edge_id = ("node1", "node2", "TYPE")
        storage_with_single_edge.set_edge_prop(edge_id, "var", "variable_name")
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.var == "variable_name"

    def test_edge_set_property_sets_single_property(
        self, graph_with_single_edge: CpgGraph
    ) -> None:
        """set_property sets one edge property and get_property returns it."""
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        result = edge.set_property("weight", 0.5)
        assert result is True
        assert edge.get_property("weight") == 0.5

    def test_edge_get_property_no_names_returns_none(
        self, graph_with_single_edge: CpgGraph
    ) -> None:
        """get_property with no alternative names returns None."""
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.get_property() is None

    def test_edge_get_property_all_alternatives_missing_returns_none(
        self, graph_with_single_edge: CpgGraph
    ) -> None:
        """get_property with all alternatives missing returns None."""
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        assert edge.get_property("missing1", "missing2") is None

    def test_edge_set_properties_sets_multiple_properties(
        self, graph_with_single_edge: CpgGraph
    ) -> None:
        """set_properties updates multiple edge properties."""
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        result = edge.set_properties({"w": 1, "label": "x"})
        assert result is True
        assert edge.get_property("w") == 1
        assert edge.get_property("label") == "x"

    def test_edge_set_properties_empty_dict_succeeds(
        self, graph_with_single_edge: CpgGraph
    ) -> None:
        """set_properties with empty dict returns True and does not fail."""
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        result = edge.set_properties({})
        assert result is True

    def test_edge_properties_returns_none_or_empty_when_no_props_set(
        self, graph_with_single_edge: CpgGraph
    ) -> None:
        """properties returns None or empty dict when no properties set on edge."""
        edge = graph_with_single_edge.edge("node1", "node2", "TYPE")
        props = edge.properties
        assert props is None or props == {}

    def test_edge_id_is_tuple_of_strings(
        self, graph: CpgGraph, storage: Storage
    ) -> None:
        """edge_id is (from_nid, to_nid, edge_type) with all strings."""
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_edge(("node1", "node2", "FLOWS_TO"))
        edge = graph.edge("node1", "node2", "FLOWS_TO")
        eid = edge.edge_id
        assert eid == ("node1", "node2", "FLOWS_TO")
        assert all(isinstance(x, str) for x in eid)
