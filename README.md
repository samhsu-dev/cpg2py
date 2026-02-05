# cpg2py

Python graph query engine for Code Property Graphs from Joern CSV exports. Directed multi-graph with generic ABCs for custom node/edge/graph types.

**Features**: Load from `nodes.csv` + `rels.csv`; query/update nodes and edges (`get_property`, `set_property`, `set_properties`); traverse succ/prev/children/parent/flow_to/flow_from; JSON persistence (`save_json`, `load_json`, `storage_from_json`). Concrete types: `CpgGraph`, `CpgNode`, `CpgEdge`.

---

## Installation

```bash
pip install cpg2py
```

From source (e.g. with [uv](https://github.com/astral-sh/uv)):

```bash
git clone https://github.com/samhsu-dev/cpg2py.git && cd cpg2py
uv sync --dev
uv run pytest tests/
```

---

## Input format

- **nodes.csv**: tab-delimited; must include node id (e.g. `id:int` or `id`). Other columns become node properties.
- **rels.csv**: tab-delimited; columns `start`, `end`, `type` (or `start:str`, `end:str`, `type:str`).

---

## Usage

**Load from CSV**

```python
from pathlib import Path
from cpg2py import cpg_graph, CpgGraph, CpgNode, CpgEdge

graph: CpgGraph = cpg_graph(Path("nodes.csv"), Path("rels.csv"))
```

**Nodes and edges** (edge identified by `(from_id, to_id, edge_type)`; `edge_type` is string)

```python
node: CpgNode = graph.node("2")
node.name
node.set_property("name", "x")
node.set_properties({"k": "v"})

edge: CpgEdge = graph.edge("2", "3", "ENTRY")
edge.from_nid, edge.to_nid, edge.type
edge.set_property("weight", 0.5)
```

**Traversal**

```python
graph.succ(node)   # successors
graph.prev(node)   # predecessors
graph.children(node)
graph.parent(node)
graph.flow_to(node)
graph.flow_from(node)
graph.topfile_node("5")   # top-level file node for given node ID
```

**Filtered iteration** (optional predicate)

```python
graph.nodes(lambda n: n.type == "Function")
graph.edges(lambda e: e.edge_type == "FLOWS_TO")
graph.succ(node, who_satisifies=lambda e: e.edge_type == "PARENT_OF")
graph.descendants(node, condition=...)
graph.ancestors(node, condition=...)
```

**JSON persistence**

```python
graph.storage.save_json("graph.json")

storage = Storage()
storage.load_json("graph.json")
graph2 = CpgGraph(storage)

# or
storage = storage_from_json(Path("graph.json"))
```

JSON schema: `{"nodes": { "<id>": { "<key>": <value>, ... }, ... }, "edges": [ {"from": str, "to": str, "type": str, "props": {...} }, ... ]}`. See [design.md](docs/design.md).

---

## Extending (ABCs)

Implement `AbcGraphQuerier[MyNode, MyEdge]`, `AbcNodeQuerier`, `AbcEdgeQuerier`; inject `Storage`. Full interface and contracts: [docs/design.md](docs/design.md).

Minimal custom graph:

```python
from cpg2py import AbcGraphQuerier, AbcNodeQuerier, AbcEdgeQuerier, Storage
from typing import Optional

class MyNode(AbcNodeQuerier): pass
class MyEdge(AbcEdgeQuerier): pass

class MyGraph(AbcGraphQuerier[MyNode, MyEdge]):
    def node(self, whose_id_is: str) -> Optional[MyNode]:
        return MyNode(self.storage, whose_id_is)
    def edge(self, fid: str, tid: str, eid: str) -> Optional[MyEdge]:
        return MyEdge(self.storage, fid, tid, eid)

g = MyGraph(Storage())
```

---

Interface specifications (classes, methods, signatures, validation): [docs/design.md](docs/design.md).

---

## License
MIT.
