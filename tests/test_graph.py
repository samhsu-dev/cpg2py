"""
Unit and integration tests for Graph class and cpg_graph factory.
"""
import pytest

from cpg2py.abc import Storage
from cpg2py.cpg import _Graph
from cpg2py.exceptions import EdgeNotFoundError, NodeNotFoundError, TopFileNotFoundError


@pytest.mark.unit
class TestGraph:
    """Unit tests for Graph class."""

    def test_graph_init_creates_graph_with_storage(self, storage):
        """
        Tests that Graph initialization creates graph with storage.

        Arrange: Storage instance
        Act: Create Graph with storage
        Assert: Graph is created and storage is accessible
        """
        graph = _Graph(storage)
        assert graph is not None
        assert graph.storage == storage

    def test_graph_node_returns_node_when_exists(self, graph, storage):
        """
        Tests that graph.node returns node when it exists.

        Arrange: Storage with a node
        Act: Get node by ID
        Assert: Returns node with correct ID
        """
        storage.add_node("node1")
        storage.set_node_props("node1", {"name": "test", "type": "AST"})
        node = graph.node("node1")
        assert node is not None
        assert node.id == "node1"

    def test_graph_node_raises_error_when_not_found(self, graph):
        """
        Tests that graph.node raises NodeNotFoundError when node not found.

        Arrange: Empty graph
        Act: Get non-existent node
        Assert: Raises NodeNotFoundError with correct node_id
        """
        with pytest.raises(NodeNotFoundError) as exc_info:
            graph.node("nonexistent")
        assert exc_info.value.node_id == "nonexistent"

    def test_graph_edge_returns_edge_when_exists(self, graph, storage):
        """
        Tests that graph.edge returns edge when it exists.

        Arrange: Storage with nodes and edge
        Act: Get edge by IDs
        Assert: Returns edge with correct ID
        """
        storage.add_node("node1")
        storage.add_node("node2")
        edge_id = ("node1", "node2", "TYPE")
        storage.add_edge(edge_id)
        edge = graph.edge("node1", "node2", "TYPE")
        assert edge is not None
        assert edge.id == edge_id

    def test_graph_edge_raises_error_when_not_found(self, graph, storage):
        """
        Tests that graph.edge raises EdgeNotFoundError when edge not found.

        Arrange: Storage with nodes but no edge
        Act: Get non-existent edge
        Assert: Raises EdgeNotFoundError with correct attributes
        """
        storage.add_node("node1")
        storage.add_node("node2")
        with pytest.raises(EdgeNotFoundError) as exc_info:
            graph.edge("node1", "node2", "TYPE")
        assert exc_info.value.from_id == "node1"
        assert exc_info.value.to_id == "node2"
        assert exc_info.value.edge_type == "TYPE"

    def test_graph_succ_returns_successor_nodes(self, graph, storage):
        """
        Tests that graph.succ returns successor nodes.

        Arrange: Storage with nodes and outgoing edges
        Act: Get successors of a node
        Assert: Returns all successor nodes
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        storage.add_edge(("node1", "node2", "TYPE1"))
        storage.add_edge(("node1", "node3", "TYPE2"))
        node1 = graph.node("node1")
        successors = list(graph.succ(node1))
        assert len(successors) == 2
        successor_ids = [n.id for n in successors]
        assert "node2" in successor_ids
        assert "node3" in successor_ids

    def test_graph_prev_returns_predecessor_nodes(self, graph, storage):
        """
        Tests that graph.prev returns predecessor nodes.

        Arrange: Storage with nodes and incoming edges
        Act: Get predecessors of a node
        Assert: Returns all predecessor nodes
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        storage.add_edge(("node1", "node2", "TYPE1"))
        storage.add_edge(("node3", "node2", "TYPE2"))
        node2 = graph.node("node2")
        predecessors = list(graph.prev(node2))
        assert len(predecessors) == 2
        predecessor_ids = [n.id for n in predecessors]
        assert "node1" in predecessor_ids
        assert "node3" in predecessor_ids

    def test_graph_children_returns_child_nodes(self, graph, storage):
        """
        Tests that graph.children returns child nodes.

        Arrange: Storage with parent-child relationships
        Act: Get children of a node
        Assert: Returns all child nodes
        """
        storage.add_node("parent")
        storage.add_node("child1")
        storage.add_node("child2")
        edge1 = ("parent", "child1", "PARENT_OF")
        edge2 = ("parent", "child2", "PARENT_OF")
        storage.add_edge(edge1)
        storage.add_edge(edge2)
        storage.set_edge_props(edge1, {"type": "PARENT_OF"})
        storage.set_edge_props(edge2, {"type": "PARENT_OF"})
        parent = graph.node("parent")
        children = list(graph.children(parent))
        assert len(children) == 2
        child_ids = [c.id for c in children]
        assert "child1" in child_ids
        assert "child2" in child_ids

    def test_graph_parent_returns_parent_nodes(self, graph, storage):
        """
        Tests that graph.parent returns parent nodes.

        Arrange: Storage with parent-child relationship
        Act: Get parent of a node
        Assert: Returns parent node
        """
        storage.add_node("parent")
        storage.add_node("child")
        edge_id = ("parent", "child", "PARENT_OF")
        storage.add_edge(edge_id)
        storage.set_edge_props(edge_id, {"type": "PARENT_OF"})
        child = graph.node("child")
        parents = list(graph.parent(child))
        assert len(parents) == 1
        assert parents[0].id == "parent"

    def test_graph_flow_to_returns_flow_successors(self, graph, storage):
        """
        Tests that graph.flow_to returns flow-to successor nodes.

        Arrange: Storage with FLOWS_TO edges
        Act: Get flow-to successors
        Assert: Returns only FLOWS_TO successors
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        edge1 = ("node1", "node2", "FLOWS_TO")
        edge2 = ("node1", "node3", "PARENT_OF")
        storage.add_edge(edge1)
        storage.add_edge(edge2)
        storage.set_edge_props(edge1, {"type": "FLOWS_TO"})
        storage.set_edge_props(edge2, {"type": "PARENT_OF"})
        node1 = graph.node("node1")
        flow_successors = list(graph.flow_to(node1))
        assert len(flow_successors) == 1
        assert flow_successors[0].id == "node2"

    def test_graph_flow_from_returns_flow_predecessors(self, graph, storage):
        """
        Tests that graph.flow_from returns flow-from predecessor nodes.

        Arrange: Storage with FLOWS_TO edges
        Act: Get flow-from predecessors
        Assert: Returns only FLOWS_TO predecessors
        """
        storage.add_node("node1")
        storage.add_node("node2")
        storage.add_node("node3")
        edge1 = ("node1", "node2", "FLOWS_TO")
        edge2 = ("node3", "node2", "PARENT_OF")
        storage.add_edge(edge1)
        storage.add_edge(edge2)
        storage.set_edge_props(edge1, {"type": "FLOWS_TO"})
        storage.set_edge_props(edge2, {"type": "PARENT_OF"})
        node2 = graph.node("node2")
        flow_predecessors = list(graph.flow_from(node2))
        assert len(flow_predecessors) == 1
        assert flow_predecessors[0].id == "node1"

    def test_graph_topfile_node_returns_file_when_node_is_file(self, graph, storage):
        """
        Tests that topfile_node returns file when node is already a File.

        Arrange: Storage with File node
        Act: Get top file node
        Assert: Returns the File node
        """
        storage.add_node("file1")
        storage.set_node_props("file1", {"type": "File"})
        top_file = graph.topfile_node("file1")
        assert top_file.id == "file1"

    def test_graph_topfile_node_returns_file_with_toplevel_flag(self, graph, storage):
        """
        Tests that topfile_node returns file with TOPLEVEL_FILE flag.

        Arrange: Storage with node having TOPLEVEL_FILE flag
        Act: Get top file node
        Assert: Returns the file node
        """
        storage.add_node("file1")
        storage.set_node_props("file1", {"flags": "TOPLEVEL_FILE"})
        top_file = graph.topfile_node("file1")
        assert top_file.id == "file1"

    def test_graph_topfile_node_returns_file_via_parent(self, graph, storage):
        """
        Tests that topfile_node returns file via parent relationship.

        Arrange: Storage with File node and child node
        Act: Get top file node from child
        Assert: Returns the File node
        """
        storage.add_node("file1")
        storage.add_node("node1")
        storage.set_node_props("file1", {"type": "File"})
        edge_id = ("file1", "node1", "PARENT_OF")
        storage.add_edge(edge_id)
        storage.set_edge_props(edge_id, {"type": "PARENT_OF"})
        top_file = graph.topfile_node("node1")
        assert top_file.id == "file1"

    def test_graph_topfile_node_raises_error_when_not_found(self, graph, storage):
        """
        Tests that topfile_node raises TopFileNotFoundError when not found.

        Arrange: Storage with node without file relationship
        Act: Get top file node
        Assert: Raises TopFileNotFoundError with correct node_id
        """
        storage.add_node("node1")
        storage.set_node_props("node1", {"type": "AST"})
        with pytest.raises(TopFileNotFoundError) as exc_info:
            graph.topfile_node("node1")
        assert exc_info.value.node_id == "node1"


@pytest.mark.integration
class TestCPGGraphFactory:
    """Integration tests for cpg_graph factory function."""

    def test_cpg_graph_from_csv_creates_graph(self, sample_node_csv, sample_edge_csv):
        """
        Tests that cpg_graph creates graph from CSV files.

        Arrange: CSV files with nodes and edges
        Act: Create graph from CSV files
        Assert: Graph is created with correct nodes
        """
        from cpg2py import cpg_graph

        graph = cpg_graph(sample_node_csv, sample_edge_csv)
        assert graph is not None
        node = graph.node("1")
        assert node.id == "1"

    def test_cpg_graph_verbose_logs_warnings(self, temp_dir):
        """
        Tests that cpg_graph with verbose=True logs warnings.

        Arrange: CSV files with duplicate data
        Act: Create graph with verbose=True
        Assert: Graph is created (warnings are logged)
        """
        from cpg2py import cpg_graph

        node_csv = temp_dir / "nodes.csv"
        edge_csv = temp_dir / "edges.csv"

        with open(node_csv, "w", encoding="utf-8") as f:
            f.write("id:int\tname\ttype\n")
            f.write("1\tnode1\tAST\n")

        with open(edge_csv, "w", encoding="utf-8") as f:
            f.write("start\tend\ttype\n")
            f.write("1\t2\tPARENT_OF\n")

        graph = cpg_graph(node_csv, edge_csv, verbose=True)
        assert graph is not None
