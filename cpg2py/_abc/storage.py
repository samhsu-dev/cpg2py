import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from .._logger import get_logger

logger = get_logger(__name__)


class Storage:
    """A directed multi-graph implementation supporting multiple edges between nodes."""

    __NodeID = str
    __EdgeID = Tuple[str, str, str]
    __Property = Dict[str, Any]

    def __init__(self):
        """Initializes an empty directed graph."""
        self.__nodes: Dict[str, Dict[str, Any]] = {}
        self.__edges: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        self.__struct: Dict[str, List[Tuple[str, str, str]]] = {}

    ################################ GRAPH STRUCTURE APIs ################################

    def add_node(self, nid: __NodeID) -> bool:
        """
        Adds a node to the graph.

        Args:
            nid: Node ID to add

        Returns:
            True if node was added, False if it already exists
        """
        nid = str(nid)
        if nid in self.__nodes:
            return False
        self.__nodes[nid] = {}
        self.__struct[nid] = []
        return True

    def contains_node(self, nid: __NodeID) -> bool:
        """
        Checks if a node exists in the graph.

        Args:
            nid: Node ID to check

        Returns:
            True if node exists, False otherwise
        """
        nid = str(nid)
        return nid in self.__nodes

    def add_edge(self, eid: __EdgeID) -> bool:
        """
        Adds a directed edge to the graph.

        Args:
            eid: Edge ID tuple (from_node, to_node, edge_type)

        Returns:
            True if edge was added, False if it already exists or nodes are missing
        """
        eid = (str(eid[0]), str(eid[1]), str(eid[2]))
        if eid in self.__edges:
            return False
        if eid[0] not in self.__nodes:
            return False
        if eid[1] not in self.__nodes:
            return False
        self.__edges[eid] = {}
        self.__struct[eid[0]].append(eid)
        self.__struct[eid[1]].append(eid)
        return True

    def contains_edge(self, eid: __EdgeID) -> bool:
        """Checks if an edge exists in the graph."""
        eid = (str(eid[0]), str(eid[1]), str(eid[2]))
        return eid in self.__edges

    def out_edges(self, nid: __NodeID) -> Iterable[__EdgeID]:
        """Returns a list of outgoing edges from a given node."""
        nid = str(nid)
        return (eid for eid in self.__struct.get(nid, []) if eid[0] == nid)

    def in_edges(self, nid: __NodeID) -> Iterable[__EdgeID]:
        """Returns a list of incoming edges to a given node."""
        nid = str(nid)
        return (eid for eid in self.__struct.get(nid, []) if eid[1] == nid)

    def successors(self, nid: __NodeID) -> Iterable[__NodeID]:
        """Returns all successor nodes of a given node."""
        nid = str(nid)
        return (eid[1] for eid in self.__struct.get(nid, []) if eid[0] == nid)

    def predecessors(self, nid: __NodeID) -> Iterable[__NodeID]:
        """Returns all predecessor nodes of a given node."""
        nid = str(nid)
        return (eid[0] for eid in self.__struct.get(nid, []) if eid[1] == nid)

    ################################ GRAPH PROPERTIES APIs ################################

    def set_node_props(self, node: __NodeID, props: __Property) -> bool:
        """Sets the properties of a node."""
        node = str(node)
        if node not in self.__nodes:
            return False
        prev_data: dict = self.__nodes[node]
        prev_data.update({str(k): v for k, v in props.items()})
        return True

    def get_node_props(self, node: __NodeID) -> Optional[__Property]:
        """Returns the properties of a node."""
        node = str(node)
        return self.__nodes.get(node, None)

    def set_node_prop(self, node: __NodeID, key: str, value: Any) -> bool:
        """Sets the properties of a node."""
        node, key = str(node), str(key)
        if node not in self.__nodes:
            return False
        self.__nodes[node][key] = value
        return True

    def get_node_prop(self, node: __NodeID, key: str) -> Optional[Any]:
        """Returns the properties of a node."""
        node, key = str(node), str(key)
        return self.__nodes.get(node, {}).get(key, None)

    def set_edge_props(self, eid: __EdgeID, props: __Property) -> bool:
        """Sets the properties of an edge."""
        eid = (str(eid[0]), str(eid[1]), str(eid[2]))
        if eid not in self.__edges:
            return False
        prev_data: dict = self.__edges[eid]
        prev_data.update({str(k): v for k, v in props.items()})
        return True

    def get_edge_props(self, eid: __EdgeID) -> Optional[__Property]:
        """Returns the properties of an edge."""
        eid = (str(eid[0]), str(eid[1]), str(eid[2]))
        return self.__edges.get(eid)

    def set_edge_prop(self, eid: __EdgeID, key: str, value: Any) -> bool:
        """Sets the properties of an edge."""
        eid = (str(eid[0]), str(eid[1]), str(eid[2]))
        key = str(key)
        if eid not in self.__edges:
            return False
        self.__edges[eid][key] = value
        return True

    def get_edge_prop(self, eid: __EdgeID, key: str) -> Optional[__Property]:
        """Returns the properties of an edge."""
        eid = (str(eid[0]), str(eid[1]), str(eid[2]))
        key = str(key)
        return self.__edges.get(eid, {}).get(key, None)

    def __repr__(self):
        """Returns a string representation of the graph."""
        return f"MultiDiGraph(nodes={len(list(self.__nodes))}, edges={len(list(self.__edges))})"

    ################################ GRAPH COMMON APIs ################################

    def get_nodes(self) -> Iterable[__NodeID]:
        """Returns a list of all nodes in the graph."""
        return self.__nodes.keys()

    def get_edges(self) -> Iterable[__EdgeID]:
        """Returns a list of all edges in the graph."""
        return self.__edges.keys()

    def remove_node(self, nid: __NodeID) -> bool:
        """Removes a node from the graph."""
        nid = str(nid)
        if nid not in self.__nodes:
            return False
        self.__nodes.pop(nid)
        for eid in self.__struct.pop(nid, []):
            self.__edges.pop(eid, None)
        return True

    def remove_edge(self, eid: __EdgeID) -> bool:
        """Removes an edge from the graph."""
        eid = (str(eid[0]), str(eid[1]), str(eid[2]))
        if eid not in self.__edges:
            return False
        self.__struct[eid[0]].remove(eid)
        self.__struct[eid[1]].remove(eid)
        self.__edges.pop(eid)
        return True

    def save_json(self, path: Union[Path, str]) -> None:
        """
        Serializes the graph (nodes and edges with properties) to a UTF-8 JSON file.

        Args:
            path: File path (Path or str).

        Raises:
            OSError: If the file cannot be written.
            TypeError: If a property value is not JSON-serializable.
        """
        payload: Dict[str, Any] = {
            "nodes": dict(self.__nodes),
            "edges": [
                {"from": eid[0], "to": eid[1], "type": eid[2], "props": props}
                for eid, props in self.__edges.items()
            ],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load_json(self, path: Union[Path, str]) -> None:
        """
        Replaces the current graph with the contents of the JSON file.

        Clears existing nodes and edges, then loads nodes, edges, and their
        properties. Expects top-level keys "nodes" and "edges".

        Args:
            path: File path (Path or str).

        Raises:
            OSError: If the file cannot be read.
            ValueError: If JSON structure is invalid (missing "nodes" or "edges").
            KeyError: If an edge object is missing "from", "to", or "type".
        """
        with open(path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
        if "nodes" not in data or "edges" not in data:
            raise ValueError("JSON must contain top-level 'nodes' and 'edges'")
        self.__nodes = {}
        self.__edges = {}
        self.__struct = {}
        nodes_data: Dict[str, Dict[str, Any]] = data["nodes"]
        for nid, props in nodes_data.items():
            nid_str = str(nid)
            self.__nodes[nid_str] = dict(props) if props else {}
            self.__struct[nid_str] = []
        for edge_obj in data["edges"]:
            from_nid = str(edge_obj["from"])
            to_nid = str(edge_obj["to"])
            etype = str(edge_obj["type"])
            props = edge_obj.get("props")
            if props is None:
                props = {}
            eid = (from_nid, to_nid, etype)
            if from_nid not in self.__nodes:
                self.__nodes[from_nid] = {}
                self.__struct[from_nid] = []
            if to_nid not in self.__nodes:
                self.__nodes[to_nid] = {}
                self.__struct[to_nid] = []
            self.__edges[eid] = dict(props)
            self.__struct[from_nid].append(eid)
            self.__struct[to_nid].append(eid)
