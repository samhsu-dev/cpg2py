import abc
from typing import Any, Dict, Optional

from .._exceptions import NodeNotFoundError
from .storage import Storage


class AbcNodeQuerier(abc.ABC):
    """
    Abstract base class for node property access, queries, and updates.
    """

    def __init__(self, graph: Storage, nid: str) -> None:
        """
        Initializes node querier and validates node existence.

        Args:
            graph: Storage instance containing the graph.
            nid: Node identifier.

        Raises:
            NodeNotFoundError: If node does not exist in the graph.
        """
        self.__nid: str = str(nid)
        self.__graph: Storage = graph
        if not graph.contains_node(self.__nid):
            raise NodeNotFoundError(str(nid))

    @property
    def node_id(self) -> str:
        """Returns the node identifier."""
        return self.__nid

    @property
    def properties(self) -> Optional[Dict[str, Any]]:
        """Returns all node properties dictionary, or None if not found."""
        return self.__graph.get_node_props(self.__nid)

    def get_property(self, *prop_names: str) -> Optional[Any]:
        """
        Returns first found property value trying multiple name alternatives.

        Args:
            prop_names: Property name alternatives to try.

        Returns:
            First found value, or None if none found.
        """
        prop_values = (self.__graph.get_node_prop(self.__nid, p_name) for p_name in prop_names)
        return next((value for value in prop_values if value is not None), None)

    def set_property(self, key: str, value: Any) -> bool:
        """
        Sets single node property value.

        Args:
            key: Property key.
            value: Property value.

        Returns:
            True if property was set, False if node does not exist.
        """
        return self.__graph.set_node_prop(self.__nid, key, value)

    def set_properties(self, props: Dict[str, Any]) -> bool:
        """
        Updates multiple node properties at once.

        Args:
            props: Dictionary of property key-value pairs.

        Returns:
            True if properties were updated, False if node does not exist.
        """
        return self.__graph.set_node_props(self.__nid, props)
