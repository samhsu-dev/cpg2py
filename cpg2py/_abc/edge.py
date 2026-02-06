from __future__ import annotations

import abc
from typing import Any, Dict, Optional, Tuple

from .._exceptions import EdgeNotFoundError
from .storage import Storage


class AbcEdgeQuerier(abc.ABC):
    """
    Abstract base class for edge property access, queries, and updates.
    """

    def __init__(self, graph: Storage, f_nid: str, t_nid: str, e_type: str) -> None:
        """
        Initializes edge querier and validates edge existence.

        Args:
            graph: Storage instance containing the graph.
            f_nid: Source node ID.
            t_nid: Target node ID.
            e_type: Edge type string.

        Raises:
            EdgeNotFoundError: If edge does not exist in the graph.
        """
        self.__graph: Storage = graph
        self.__edge_id: Tuple[str, str, str] = (str(f_nid), str(t_nid), str(e_type))
        if not graph.contains_edge(self.__edge_id):
            raise EdgeNotFoundError(f_nid, t_nid, e_type)

    @property
    def edge_id(self) -> Tuple[str, str, str]:
        """
        Returns the edge identifier tuple (from_nid, to_nid, edge_type).
        """
        return self.__edge_id

    @property
    def from_nid(self) -> str:
        """Returns the source node identifier."""
        return self.__edge_id[0]

    @property
    def to_nid(self) -> str:
        """Returns the target node identifier."""
        return self.__edge_id[1]

    @property
    def edge_type(self) -> str:
        """Returns the edge type string."""
        return self.__edge_id[2]

    @property
    def properties(self) -> Optional[Dict[str, Any]]:
        """Returns all edge properties dictionary, or None if not found."""
        return self.__graph.get_edge_props(self.__edge_id)

    def get_property(self, *prop_names: str) -> Optional[Any]:
        """
        Returns first found property value trying multiple name alternatives.

        Args:
            prop_names: Property name alternatives to try.

        Returns:
            First found value, or None if none found.
        """
        prop_values = (self.__graph.get_edge_prop(self.__edge_id, p_name) for p_name in prop_names)
        return next((value for value in prop_values if value is not None), None)

    def set_property(self, key: str, value: Any) -> bool:
        """
        Sets single edge property value.

        Args:
            key: Property key.
            value: Property value.

        Returns:
            True if property was set, False if edge does not exist.
        """
        return self.__graph.set_edge_prop(self.__edge_id, key, value)

    def set_properties(self, props: Dict[str, Any]) -> bool:
        """
        Updates multiple edge properties at once.

        Args:
            props: Dictionary of property key-value pairs.

        Returns:
            True if properties were updated, False if edge does not exist.
        """
        return self.__graph.set_edge_props(self.__edge_id, props)
