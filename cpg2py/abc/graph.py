from __future__ import annotations

import abc
from collections import deque
from typing import Callable, Deque, Iterable, List, Optional

from .edge import AbcEdgeQuerier
from .node import AbcNodeQuerier
from .storage import Storage


class AbcGraphQuerier(abc.ABC):
    """
    Abstract base class for graph query operations.

    Provides interface for querying nodes, edges, and traversing graph structures.
    """

    __NodeCondition = Callable[[AbcNodeQuerier], bool]
    __EdgeCondition = Callable[[AbcEdgeQuerier], bool]

    __always_true = lambda _: True

    __NodesResult = Iterable[AbcNodeQuerier]
    __EdgesResult = Iterable[AbcEdgeQuerier]

    def __init__(self, target: Storage, maxdepth: int = -1) -> None:
        """
        Initializes a graph querier.

        Args:
            target: Storage instance containing the graph
            maxdepth: Maximum depth for traversal operations (-1 for unlimited)
        """
        self.__graph: Storage = target
        self.__maxdepth: int = maxdepth

    @property
    def storage(self) -> Storage:
        """
        Returns the underlying storage instance.

        Returns:
            Storage instance
        """
        return self.__graph

    @abc.abstractmethod
    def node(self, whose_id_is: str) -> Optional[AbcNodeQuerier]:
        """
        Returns a node by its ID.

        Args:
            whose_id_is: Node ID to look up

        Returns:
            Node instance if found, None otherwise
        """
        raise NotImplementedError

    @abc.abstractmethod
    def edge(self, fid: str, tid: str, eid: str) -> Optional[AbcEdgeQuerier]:
        """
        Returns an edge by its source, target, and edge type.

        Args:
            fid: Source node ID
            tid: Target node ID
            eid: Edge type/ID

        Returns:
            Edge instance if found, None otherwise
        """
        raise NotImplementedError

    def nodes(self, who_satisifies: __NodeCondition = __always_true) -> __NodesResult:
        for nid in self.__graph.get_nodes():
            cur_node = self.node(whose_id_is=nid)
            if cur_node and who_satisifies(cur_node):
                yield cur_node

    def first_node(
        self, who_satisifies: __NodeCondition = __always_true
    ) -> Optional[AbcNodeQuerier]:
        return next(self.nodes(who_satisifies), None)

    def edges(self, who_satisifies: __EdgeCondition = __always_true) -> __EdgesResult:
        for from_id, to_id, edge_id in self.__graph.get_edges():
            cur_edge = self.edge(from_id, to_id, edge_id)
            if cur_edge and who_satisifies(cur_edge):
                yield cur_edge

    def succ(
        self, of: AbcNodeQuerier, who_satisifies: __EdgeCondition = __always_true
    ) -> __NodesResult:
        for src, dst, edge_type in self.__graph.out_edges(of.id):
            if not who_satisifies(self.edge(src, dst, edge_type)):
                continue
            yield self.node(whose_id_is=dst)

    def prev(
        self, of: AbcNodeQuerier, who_satisifies: __EdgeCondition = __always_true
    ) -> __NodesResult:
        for src, dst, edge_type in self.__graph.in_edges(of.id):
            if not who_satisifies(self.edge(src, dst, edge_type)):
                continue
            yield self.node(whose_id_is=src)

    def __bfs_search(
        self, root: AbcNodeQuerier, condition: __EdgeCondition, reverse: bool
    ) -> __NodesResult:
        """
        Returns nodes from src node by BFS order (src node not included).

        Args:
            root: Starting node
            condition: Edge condition filter
            reverse: If True, traverse backwards
        """
        if root is None:
            return
        visited_nids: List[str] = []
        nodes_queue: Deque[AbcNodeQuerier] = deque([root, None])
        depth = self.__maxdepth
        while depth != 0 and len(nodes_queue) > 1:
            cur_node = nodes_queue.popleft()
            if cur_node is None:
                nodes_queue.append(None)
                depth -= 1
            elif cur_node.id not in visited_nids:
                visited_nids.append(cur_node.id)
                if not reverse:
                    n_nodes = self.succ(cur_node, condition)
                else:
                    n_nodes = self.prev(cur_node, condition)
                nodes_queue.extend(n_nodes)
                if root.id != cur_node.id:
                    yield cur_node

    def descendants(
        self, src: AbcNodeQuerier, condition: __EdgeCondition = __always_true
    ) -> __NodesResult:
        """
        Returns descendants from src node by BFS order (src node not included).

        Args:
            src: Source node
            condition: Edge condition filter

        Returns:
            Iterable of descendant nodes
        """
        return self.__bfs_search(src, condition, reverse=False)

    def ancestors(
        self, src: AbcNodeQuerier, condition: __EdgeCondition = __always_true
    ) -> __NodesResult:
        """
        Returns ancestors from src node by BFS order (src node not included).

        Args:
            src: Source node
            condition: Edge condition filter

        Returns:
            Iterable of ancestor nodes
        """
        return self.__bfs_search(src, condition, reverse=True)
