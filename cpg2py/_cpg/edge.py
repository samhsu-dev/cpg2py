from __future__ import annotations

from typing import Optional, Tuple

from .._abc import AbcEdgeQuerier


class CpgEdge(AbcEdgeQuerier):
    """Concrete edge implementation with CPG-specific property accessors."""

    @property
    def id(self) -> Tuple[str, str, str]:
        return self.edge_id

    @property
    def start(self) -> Optional[int]:
        start_str = str(self.get_property("start", "start:START_ID"))
        return int(start_str) if start_str.isnumeric() else int(self.from_nid)

    @property
    def end(self) -> Optional[int]:
        end_str = str(self.get_property("end", "end:END_ID"))
        return int(end_str) if end_str.isnumeric() else int(self.to_nid)

    @property
    def type(self) -> Optional[str]:
        return self.get_property("type", "type:TYPE")

    @property
    def var(self) -> Optional[str]:
        return self.get_property("var")
