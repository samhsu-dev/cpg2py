"""Custom exceptions for cpg2py package."""

from typing import Optional


class CPGError(Exception):
    """Base exception for all CPG-related errors."""


class NodeNotFoundError(CPGError):
    """Raised when node identifier does not exist in storage."""

    def __init__(self, node_id: str, message: Optional[str] = None) -> None:
        self.node_id = node_id
        if message is None:
            message = f"Node with id '{node_id}' not found in graph"
        super().__init__(message)


class EdgeNotFoundError(CPGError):
    """Raised when edge identifier tuple does not exist in storage."""

    def __init__(
        self, from_id: str, to_id: str, edge_type: str, message: Optional[str] = None
    ) -> None:
        self.from_id = from_id
        self.to_id = to_id
        self.edge_type = edge_type
        if message is None:
            message = (
                f"Edge from '{from_id}' to '{to_id}' with type '{edge_type}' not found in graph"
            )
        super().__init__(message)


class TopFileNotFoundError(CPGError):
    """Raised when top file node cannot be found during upward traversal."""

    def __init__(self, node_id: str, message: Optional[str] = None) -> None:
        self.node_id = node_id
        if message is None:
            message = f"Cannot find top file node from node '{node_id}'"
        super().__init__(message)
