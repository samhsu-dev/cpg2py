# Graph Query System Design

## Design Overview

**Classes**: `AbcGraphQuerier`, `AbcNodeQuerier`, `AbcEdgeQuerier`, `Storage`, `_Graph`, `_Node`, `_Edge`

**Relationships**: `AbcGraphQuerier` is abstract and generic, `_Graph` extends `AbcGraphQuerier[_Node, _Edge]`, `AbcNodeQuerier` is abstract, `_Node` extends `AbcNodeQuerier`, `AbcEdgeQuerier` is abstract, `_Edge` extends `AbcEdgeQuerier`, `AbcGraphQuerier` uses `Storage`, `AbcNodeQuerier` uses `Storage`, `AbcEdgeQuerier` uses `Storage`, `_Graph` contains `Storage`, `_Node` contains `Storage`, `_Edge` contains `Storage`

**Abstract**: `AbcGraphQuerier` (implemented by `_Graph`), `AbcNodeQuerier` (implemented by `_Node`), `AbcEdgeQuerier` (implemented by `_Edge`)

**Exceptions**: `CPGError` extends `Exception`, `NodeNotFoundError` extends `CPGError` (raised by `AbcNodeQuerier`, `_Graph`), `EdgeNotFoundError` extends `CPGError` (raised by `AbcEdgeQuerier`, `_Graph`), `TopFileNotFoundError` extends `CPGError` (raised by `_Graph`)

## Class Specifications

### **AbcGraphQuerier Class**
- **Responsibility**: Provides abstract interface for graph query operations with generic type safety
- **Properties**: 
  - `storage: Storage` - Returns the underlying storage instance
- **[__init__(target: Storage, maxdepth: int = -1) -> None]**
  - **Behavior**: Initializes graph querier with storage reference and optional depth limit
  - **Input**: Storage instance, maximum traversal depth (-1 for unlimited)
  - **Output**: None
- **[node(whose_id_is: str) -> Optional[_GenericNode]]**
  - **Behavior**: Returns node querier by identifier (abstract method)
  - **Input**: Node identifier string
  - **Output**: Node querier instance or None
  - **Raises**: Must be implemented by subclass
- **[edge(fid: str, tid: str, eid: str) -> Optional[_GenericEdge]]**
  - **Behavior**: Returns edge querier by source, target, and edge type (abstract method)
  - **Input**: Source node ID, target node ID, edge type
  - **Output**: Edge querier instance or None
  - **Raises**: Must be implemented by subclass
- **[nodes(who_satisifies: Callable[[_NodeType], bool] = always_true) -> Iterable[_GenericNode]]**
  - **Behavior**: Yields all nodes matching the condition
  - **Input**: Node condition predicate function
  - **Output**: Iterable of matching node queriers
- **[first_node(who_satisifies: Callable[[_NodeType], bool] = always_true) -> Optional[_GenericNode]]**
  - **Behavior**: Returns first node matching the condition
  - **Input**: Node condition predicate function
  - **Output**: First matching node querier or None
- **[edges(who_satisifies: Callable[[_EdgeType], bool] = always_true) -> Iterable[_GenericEdge]]**
  - **Behavior**: Yields all edges matching the condition
  - **Input**: Edge condition predicate function
  - **Output**: Iterable of matching edge queriers
- **[succ(of: _GenericNode, who_satisifies: Callable[[_EdgeType], bool] = always_true) -> Iterable[_GenericNode]]**
  - **Behavior**: Yields successor nodes connected via outgoing edges matching condition
  - **Input**: Source node querier, edge condition predicate
  - **Output**: Iterable of successor node queriers
- **[prev(of: _GenericNode, who_satisifies: Callable[[_EdgeType], bool] = always_true) -> Iterable[_GenericNode]]**
  - **Behavior**: Yields predecessor nodes connected via incoming edges matching condition
  - **Input**: Target node querier, edge condition predicate
  - **Output**: Iterable of predecessor node queriers
- **[descendants(src: _GenericNode, condition: Callable[[_EdgeType], bool] = always_true) -> Iterable[_GenericNode]]**
  - **Behavior**: Yields descendant nodes via breadth-first search excluding root
  - **Input**: Source node querier, edge condition predicate
  - **Output**: Iterable of descendant node queriers in BFS order
- **[ancestors(src: _GenericNode, condition: Callable[[_EdgeType], bool] = always_true) -> Iterable[_GenericNode]]**
  - **Behavior**: Yields ancestor nodes via reverse breadth-first search excluding root
  - **Input**: Source node querier, edge condition predicate
  - **Output**: Iterable of ancestor node queriers in BFS order
- **Example Usage**:
```python
class MyGraph(AbcGraphQuerier[MyNode, MyEdge]):
    def node(self, whose_id_is: str) -> Optional[MyNode]:
        return MyNode(self.storage, whose_id_is)
    
    def edge(self, fid: str, tid: str, eid: str) -> Optional[MyEdge]:
        return MyEdge(self.storage, fid, tid, eid)

graph = MyGraph(storage)
for node in graph.nodes(lambda n: n.type == "Function"):
    print(node.id)
```

### **AbcNodeQuerier Class**
- **Responsibility**: Provides abstract interface for node property access, queries, and updates
- **Properties**: 
  - `node_id: str` - Returns the node identifier
  - `properties: Optional[Dict[str, Any]]` - Returns all node properties dictionary
- **[__init__(graph: Storage, nid: str) -> None]**
  - **Behavior**: Initializes node querier and validates node existence
  - **Input**: Storage instance, node identifier
  - **Output**: None
  - **Raises**: `NodeNotFoundError` if node does not exist
- **[get_property(*prop_names: str) -> Optional[Any]]**
  - **Behavior**: Returns first found property value trying multiple name alternatives
  - **Input**: Variable number of property name alternatives
  - **Output**: Property value or None if not found
- **[set_property(key: str, value: Any) -> bool]**
  - **Behavior**: Sets single node property value
  - **Input**: Property key, property value
  - **Output**: True if property was set, False if node does not exist
- **[set_properties(props: Dict[str, Any]) -> bool]**
  - **Behavior**: Updates multiple node properties at once
  - **Input**: Dictionary of property key-value pairs
  - **Output**: True if properties were updated, False if node does not exist
- **Example Usage**:
```python
class MyNode(AbcNodeQuerier):
    @property
    def name(self):
        return self.get_property("name", "name:str")

node = MyNode(storage, "123")
print(node.node_id, node.name)
node.set_property("name", "new_name")
node.set_properties({"age": 25, "city": "NYC"})
```

### **AbcEdgeQuerier Class**
- **Responsibility**: Provides abstract interface for edge property access, queries, and updates
- **Properties**: 
  - `edge_id: Tuple[str, str, str]` - Returns edge identifier tuple
  - `from_nid: str` - Returns source node identifier
  - `to_nid: str` - Returns target node identifier
  - `edge_type: str` - Returns edge type string
  - `properties: Optional[Dict[str, Any]]` - Returns all edge properties dictionary
- **[__init__(graph: Storage, f_nid: str, t_nid: str, e_type: str) -> None]**
  - **Behavior**: Initializes edge querier and validates edge existence
  - **Input**: Storage instance, source node ID, target node ID, edge type string
  - **Output**: None
  - **Raises**: `EdgeNotFoundError` if edge does not exist
- **[get_property(*prop_names: str) -> Optional[Any]]**
  - **Behavior**: Returns first found property value trying multiple name alternatives
  - **Input**: Variable number of property name alternatives
  - **Output**: Property value or None if not found
- **[set_property(key: str, value: Any) -> bool]**
  - **Behavior**: Sets single edge property value
  - **Input**: Property key, property value
  - **Output**: True if property was set, False if edge does not exist
- **[set_properties(props: Dict[str, Any]) -> bool]**
  - **Behavior**: Updates multiple edge properties at once
  - **Input**: Dictionary of property key-value pairs
  - **Output**: True if properties were updated, False if edge does not exist
- **Example Usage**:
```python
class MyEdge(AbcEdgeQuerier):
    @property
    def weight(self):
        return self.get_property("weight", "weight:float")

edge = MyEdge(storage, "1", "2", "CONNECTS")
print(edge.from_nid, edge.to_nid, edge.edge_type)
edge.set_property("weight", 0.5)
edge.set_properties({"color": "red", "style": "dashed"})
```

### **Storage Class**
- **Responsibility**: Implements directed multi-graph data structure with node and edge storage
- **Properties**: None (internal state only)
- **[__init__() -> None]**
  - **Behavior**: Initializes empty graph with node, edge, and structure dictionaries
  - **Input**: None
  - **Output**: None
- **[add_node(nid: str) -> bool]**
  - **Behavior**: Adds node to graph if not already present
  - **Input**: Node identifier
  - **Output**: True if added, False if already exists
- **[contains_node(nid: str) -> bool]**
  - **Behavior**: Checks if node exists in graph
  - **Input**: Node identifier
  - **Output**: True if exists, False otherwise
- **[add_edge(eid: Tuple[str, str, str]) -> bool]**
  - **Behavior**: Adds directed edge to graph if nodes exist and edge not present
  - **Input**: Edge identifier tuple (from_node, to_node, edge_type)
  - **Output**: True if added, False if exists or nodes missing
- **[contains_edge(eid: Tuple[str, str, str]) -> bool]**
  - **Behavior**: Checks if edge exists in graph
  - **Input**: Edge identifier tuple
  - **Output**: True if exists, False otherwise
- **[out_edges(nid: str) -> Iterable[Tuple[str, str, str]]]**
  - **Behavior**: Yields all outgoing edges from node
  - **Input**: Node identifier
  - **Output**: Iterable of edge identifier tuples
- **[in_edges(nid: str) -> Iterable[Tuple[str, str, str]]]**
  - **Behavior**: Yields all incoming edges to node
  - **Input**: Node identifier
  - **Output**: Iterable of edge identifier tuples
- **[successors(nid: str) -> Iterable[str]]**
  - **Behavior**: Yields all successor node identifiers
  - **Input**: Node identifier
  - **Output**: Iterable of node identifiers
- **[predecessors(nid: str) -> Iterable[str]]**
  - **Behavior**: Yields all predecessor node identifiers
  - **Input**: Node identifier
  - **Output**: Iterable of node identifiers
- **[set_node_props(node: str, props: Dict[str, Any]) -> bool]**
  - **Behavior**: Updates node properties dictionary
  - **Input**: Node identifier, properties dictionary
  - **Output**: True if node exists, False otherwise
- **[get_node_props(node: str) -> Optional[Dict[str, Any]]]**
  - **Behavior**: Returns all node properties
  - **Input**: Node identifier
  - **Output**: Properties dictionary or None
- **[set_node_prop(node: str, key: str, value: Any) -> bool]**
  - **Behavior**: Sets single node property
  - **Input**: Node identifier, property key, property value
  - **Output**: True if node exists, False otherwise
- **[get_node_prop(node: str, key: str) -> Optional[Any]]**
  - **Behavior**: Returns single node property value
  - **Input**: Node identifier, property key
  - **Output**: Property value or None
- **[set_edge_props(eid: Tuple[str, str, str], props: Dict[str, Any]) -> bool]**
  - **Behavior**: Updates edge properties dictionary
  - **Input**: Edge identifier tuple, properties dictionary
  - **Output**: True if edge exists, False otherwise
- **[get_edge_props(eid: Tuple[str, str, str]) -> Optional[Dict[str, Any]]]**
  - **Behavior**: Returns all edge properties
  - **Input**: Edge identifier tuple
  - **Output**: Properties dictionary or None
- **[set_edge_prop(eid: Tuple[str, str, str], key: str, value: Any) -> bool]**
  - **Behavior**: Sets single edge property
  - **Input**: Edge identifier tuple, property key, property value
  - **Output**: True if edge exists, False otherwise
- **[get_edge_prop(eid: Tuple[str, str, str], key: str) -> Optional[Any]]**
  - **Behavior**: Returns single edge property value
  - **Input**: Edge identifier tuple, property key
  - **Output**: Property value or None
- **[get_nodes() -> Iterable[str]]**
  - **Behavior**: Yields all node identifiers
  - **Input**: None
  - **Output**: Iterable of node identifiers
- **[get_edges() -> Iterable[Tuple[str, str, str]]]**
  - **Behavior**: Yields all edge identifier tuples
  - **Input**: None
  - **Output**: Iterable of edge identifier tuples
- **[remove_node(nid: str) -> bool]**
  - **Behavior**: Removes node and all connected edges
  - **Input**: Node identifier
  - **Output**: True if removed, False if not found
- **[remove_edge(eid: Tuple[str, str, str]) -> bool]**
  - **Behavior**: Removes edge from graph
  - **Input**: Edge identifier tuple
  - **Output**: True if removed, False if not found
- **[save_json(path: Union[Path, str]) -> None]**
  - **Behavior**: Serializes the graph (nodes and edges with properties) to a JSON file at the given path
  - **Input**: File path (Path or str)
  - **Output**: None
  - **Raises**: File I/O errors if the file cannot be written
- **[load_json(path: Union[Path, str]) -> None]**
  - **Behavior**: Replaces the current graph with the contents of the given JSON file; clears existing nodes and edges then loads nodes, edges, and their properties
  - **Input**: File path (Path or str)
  - **Output**: None
  - **Raises**: File I/O errors if the file cannot be read; ValueError or KeyError if JSON format is invalid
- **Example Usage**:
```python
storage = Storage()
storage.add_node("1")
storage.set_node_prop("1", "name", "test")
storage.add_edge(("1", "2", "CONNECTS"))
edges = list(storage.out_edges("1"))
storage.save_json("graph.json")
storage.load_json("graph.json")
```

### **_Graph Class**
- **Responsibility**: Concrete graph implementation for CPG data with domain-specific query methods
- **Properties**: Inherits `storage: Storage` from `AbcGraphQuerier`
- **[__init__(target: Storage) -> None]**
  - **Behavior**: Initializes CPG graph with storage instance
  - **Input**: Storage instance
  - **Output**: None
- **[node(whose_id_is: str) -> Optional[_Node]]**
  - **Behavior**: Returns CPG node by identifier with error handling
  - **Input**: Node identifier
  - **Output**: Node instance
  - **Raises**: `NodeNotFoundError` if node not found
- **[edge(fid: str, tid: str, eid: str) -> Optional[_Edge]]**
  - **Behavior**: Returns CPG edge by identifiers with error handling
  - **Input**: Source node ID, target node ID, edge type
  - **Output**: Edge instance
  - **Raises**: `EdgeNotFoundError` if edge not found
- **[topfile_node(of_nid: str) -> _Node]**
  - **Behavior**: Finds top-level file node by traversing PARENT_OF, ENTRY, EXIT edges upward
  - **Input**: Starting node identifier
  - **Output**: Top file node instance
  - **Raises**: `TopFileNotFoundError` if top file cannot be found, `NodeNotFoundError` if starting node not found
- **[children(of: _Node, extra: Callable[[_Edge], bool] = always_true) -> Iterable[_Node]]**
  - **Behavior**: Yields child nodes connected via PARENT_OF edges
  - **Input**: Parent node, additional edge condition
  - **Output**: Iterable of child nodes
- **[parent(of: _Node, extra: Callable[[_Edge], bool] = always_true) -> Iterable[_Node]]**
  - **Behavior**: Yields parent nodes connected via PARENT_OF edges
  - **Input**: Child node, additional edge condition
  - **Output**: Iterable of parent nodes
- **[flow_to(of: _Node, extra: Callable[[_Edge], bool] = always_true) -> Iterable[_Node]]**
  - **Behavior**: Yields successor nodes connected via FLOWS_TO edges
  - **Input**: Source node, additional edge condition
  - **Output**: Iterable of flow successor nodes
- **[flow_from(of: _Node, extra: Callable[[_Edge], bool] = always_true) -> Iterable[_Node]]**
  - **Behavior**: Yields predecessor nodes connected via FLOWS_TO edges
  - **Input**: Target node, additional edge condition
  - **Output**: Iterable of flow predecessor nodes
- **Example Usage**:
```python
graph = _Graph(storage)
node = graph.node("123")
children = list(graph.children(node))
flow_targets = list(graph.flow_to(node))
```

### **_Node Class**
- **Responsibility**: Concrete node implementation with CPG-specific property accessors
- **Properties**: 
  - `id: str` - Node identifier
  - `code: Optional[str]` - Source code string
  - `label: Optional[str]` - Node label
  - `flags: List[str]` - Node flags as list
  - `line_num: Optional[int]` - Source line number
  - `children_num: Optional[int]` - Number of children
  - `func_id: Optional[int]` - Function identifier
  - `class_name: Optional[str]` - Class name
  - `namespace: Optional[str]` - Namespace
  - `name: Optional[str]` - Node name
  - `end_num: Optional[int]` - End line number
  - `comment: Optional[str]` - Documentation comment
  - `type: Optional[str]` - Node type
- **[__init__(graph: Storage, nid: str) -> None]**
  - **Behavior**: Initializes CPG node with storage and identifier
  - **Input**: Storage instance (via AbcGraphQuerier), node identifier
  - **Output**: None
  - **Raises**: `NodeNotFoundError` if node does not exist
- **Example Usage**:
```python
node = _Node(storage, "123")
print(node.id, node.name, node.type, node.line_num)
```

### **_Edge Class**
- **Responsibility**: Concrete edge implementation with CPG-specific property accessors
- **Properties**: 
  - `id: Tuple[str, str, str]` - Edge identifier tuple
  - `start: Optional[int]` - Start node ID as integer
  - `end: Optional[int]` - End node ID as integer
  - `type: Optional[str]` - Edge type string
  - `var: Optional[str]` - Variable name
- **[__init__(graph: Storage, f_nid: str, t_nid: str, e_type: str) -> None]**
  - **Behavior**: Initializes CPG edge with storage and identifiers
  - **Input**: Storage instance (via AbcGraphQuerier), source node ID, target node ID, edge type
  - **Output**: None
  - **Raises**: `EdgeNotFoundError` if edge does not exist
- **Example Usage**:
```python
edge = _Edge(storage, "1", "2", "FLOWS_TO")
print(edge.from_nid, edge.to_nid, edge.type)
```

## Function Specifications

### **[storage_from_json(path: Union[Path, str]) -> Storage]**
- **Responsibility**: Creates a Storage instance populated from a JSON file
- **Behavior**: Reads the JSON file, parses nodes and edges with properties, returns a new Storage containing that graph
- **Input**: Path to JSON file (Path or str)
- **Output**: New Storage instance
- **Raises**: File I/O errors if the file cannot be read; ValueError or KeyError if JSON format is invalid
- **Example Usage**:
```python
from pathlib import Path
storage = storage_from_json(Path("graph.json"))
graph = _Graph(storage)
```

### **[cpg_graph(node_csv: Path, edge_csv: Path, verbose: bool = False) -> _Graph]**
- **Responsibility**: Creates CPG graph instance from Joern CSV files
- **Behavior**: Reads tab-delimited CSV files, parses nodes and edges, populates storage, returns graph instance
- **Input**: Path to nodes CSV file, path to edges CSV file, optional verbose logging flag
- **Output**: Graph instance loaded from CSV data
- **Raises**: File I/O errors if files cannot be read
- **Example Usage**:
```python
from pathlib import Path
graph = cpg_graph(Path("nodes.csv"), Path("rels.csv"))
node = graph.node("123")
```

## Exception Classes

**CPGError**: Base exception for all CPG-related errors

**NodeNotFoundError**: Raised when node identifier does not exist in storage, contains `node_id` attribute

**EdgeNotFoundError**: Raised when edge identifier tuple does not exist in storage, contains `from_id`, `to_id`, `edge_type` attributes

**TopFileNotFoundError**: Raised when top file node cannot be found during upward traversal, contains `node_id` attribute

## Validation Rules

**Storage Validation**:
- Node identifiers are converted to strings before operations
- Edge identifiers are converted to tuples of strings
- Edge addition requires both source and target nodes to exist
- Property keys are converted to strings before storage

**JSON persistence format** (for save_json / load_json and storage_from_json):
- File is UTF-8 encoded JSON with two top-level keys: `"nodes"` and `"edges"`.
- `"nodes"`: object mapping node ID (string) to a properties object (string keys, JSON-serializable values).
- `"edges"`: array of edge objects; each has string keys `"from"`, `"to"`, `"type"` and optionally `"props"` (object). Property values must be JSON-serializable.
- Example: `{"nodes": {"1": {"name": "a"}, "2": {}}, "edges": [{"from": "1", "to": "2", "type": "CONNECTS", "props": {}}]}`
- save_json writes this format; load_json and storage_from_json expect it and reject missing or malformed structure.

**Node Querier Validation**:
- Node existence is validated during initialization
- Node identifier is converted to string
- Property access returns None for missing properties
- Property updates return False if node does not exist

**Edge Querier Validation**:
- Edge existence is validated during initialization
- Edge identifier components are converted to strings
- Edge type must be provided as string (not integer)
- Property access returns None for missing properties
- Property updates return False if edge does not exist

**Graph Querier Validation**:
- Storage instance must be provided during initialization
- Maximum depth of -1 indicates unlimited traversal
- Node and edge creation delegates validation to querier classes
- Traversal operations skip None results from node/edge creation

**CPG Graph Validation**:
- CSV parsing handles missing node IDs by skipping rows
- Edge parsing handles multiple column name formats (start/start:str, end/end:str, type/type:str)
- Missing nodes referenced in edges are automatically created with warnings
- Duplicate nodes and edges are handled gracefully with optional warnings
