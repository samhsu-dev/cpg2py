# Graph Query System

## 1. Context

**Problem Statement**
Code Property Graphs extracted from Joern contain complex relationships between code elements that require efficient querying mechanisms. Developers need a flexible interface to traverse AST structures, control flow, and data flow graphs without being tied to specific storage implementations. The system must support extensible query patterns while maintaining type safety and performance.

**System Role**
The Graph Query System serves as the primary interface layer between graph storage and application logic, providing abstract query operations that can be implemented with different storage backends and query strategies.

**Data Flow**
- **Inputs:** Storage instances containing node and edge data, node identifiers, edge identifiers, query conditions
- **Outputs:** Node queriers, edge queriers, iterable query results
- **Connections:** Storage → Graph Querier → Node/Edge Queriers → Application Code

**Scope Boundaries**
- **Owned:** Query interface definitions, traversal algorithms, condition-based filtering, generic type safety
- **Not Owned:** Storage implementation details, CSV parsing, concrete node/edge property access, serialization

## 2. Concepts

**Conceptual Diagram**
```
┌─────────────────┐
│  Storage        │
│  (Graph Data)   │
└────────┬────────┘
         │
         │ provides data
         │
┌────────▼─────────────────┐
│  AbcGraphQuerier         │
│  (Query Interface)       │
└────────┬─────────────────┘
         │
         │ creates
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│ Node  │ │ Edge  │
│Query  │ │Query  │
└───────┘ └───────┘
```

**Core Concepts**

**Graph Querier**
A Graph Querier provides the primary interface for querying graph structures. It abstracts over storage implementations and defines operations for retrieving nodes, edges, and traversing relationships. The querier maintains a reference to storage and delegates structural queries to it while providing higher-level query operations. Graph Queriers are generic, parameterized by concrete node and edge types to ensure type safety throughout query operations. They support conditional filtering on both nodes and edges, enabling complex query patterns without exposing storage internals.

**Node Querier**
A Node Querier represents a single node in the graph and provides access to its properties. It encapsulates the node identifier and storage reference, validating node existence upon creation. Node Queriers abstract property access patterns, supporting multiple property name alternatives to handle schema variations. They serve as the primary interface for accessing node data without exposing storage implementation details.

**Edge Querier**
An Edge Querier represents a single edge connecting two nodes. It encapsulates the edge identifier tuple containing source node, target node, and edge type. Edge Queriers validate edge existence and provide property access similar to Node Queriers. They enable type-safe edge traversal and property queries while maintaining separation from storage internals.

**Query Conditions**
Query conditions are predicate functions that filter nodes or edges during traversal operations. They enable selective querying by allowing callers to specify which relationships to follow or which nodes to include in results. Conditions operate on querier instances, providing access to properties for filtering decisions. The system provides a default always-true condition for unconditional queries.

**Traversal Operations**
Traversal operations navigate graph structures following relationships defined by edges. Successor and predecessor queries follow outgoing and incoming edges respectively, optionally filtered by edge conditions. Breadth-first search operations traverse multiple levels, supporting depth limits and reverse traversal. These operations yield querier instances, maintaining type safety and abstraction throughout traversal.

## 3. Contracts & Flow

**Data Contracts**

**With Storage Module:**
Storage provides node and edge identifiers, structural relationships, and property data. The Graph Query System requests node existence checks, edge existence checks, outgoing edges, incoming edges, and property values. Storage returns identifiers and property dictionaries, maintaining no knowledge of querier types or query semantics.

**With Node Querier:**
Graph Queriers create Node Querier instances given node identifiers. Node Queriers request property data from storage through the Graph Querier's storage reference. Node Queriers expose node identifiers for use in graph traversal operations.

**With Edge Querier:**
Graph Queriers create Edge Querier instances given edge identifier tuples. Edge Queriers request property data from storage and expose edge components for traversal filtering. Edge Queriers enable condition-based filtering during graph navigation.

**Internal Processing Flow**

1. **Initialization** - Graph Querier receives storage instance and optional depth limit, storing references for later use
2. **Node Retrieval** - Application requests node by identifier, Graph Querier validates existence and creates Node Querier instance
3. **Edge Retrieval** - Application requests edge by identifiers, Graph Querier validates existence and creates Edge Querier instance
4. **Condition Evaluation** - Traversal operations evaluate edge conditions on each edge, filtering relationships based on edge properties
5. **Successor Traversal** - Graph Querier retrieves outgoing edges from storage, filters by condition, creates Node Queriers for target nodes
6. **Predecessor Traversal** - Graph Querier retrieves incoming edges from storage, filters by condition, creates Node Queriers for source nodes
7. **Breadth-First Search** - Graph Querier maintains queue of nodes, processes each level, applies depth limits, yields nodes excluding root
8. **Property Access** - Node or Edge Querier requests property from storage, handles multiple property name alternatives, returns first match

## 4. Scenarios

**Typical**
A developer loads a CPG graph from CSV files and queries for all function nodes. The Graph Querier iterates through storage node identifiers, creates Node Queriers, filters by node type property, and yields matching nodes. The developer then traverses AST relationships by querying successors filtered to PARENT_OF edges, navigating the abstract syntax tree structure.

**Boundary**
When querying a non-existent node, the Graph Querier attempts to create a Node Querier which validates existence against storage. Storage reports the node missing, and the Node Querier raises an exception. The Graph Querier propagates this exception, allowing the application to handle the error case appropriately.

**Interaction**
An application performs data flow analysis by starting from a variable node and following FLOWS_TO edges. The Graph Querier's flow_to method filters successor edges by type, creating Node Queriers for each data flow target. The application recursively queries flow successors, building a complete data flow path. The Graph Querier coordinates between storage edge retrieval and Node Querier creation, maintaining type safety throughout the traversal.
