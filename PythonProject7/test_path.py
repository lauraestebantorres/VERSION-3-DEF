# Import necessary functions and classes
from node import Node, Distance
from graph import Graph, AddNode as GraphAddNode, AddSegment
from path import Path
import path


# Create a more complex test graph
G = Graph()


# Add more nodes to the graph
GraphAddNode(G, Node("A", 1, 5))
GraphAddNode(G, Node("B", 5, 8))
GraphAddNode(G, Node("C", 8, 5))
GraphAddNode(G, Node("D", 5, 2))
GraphAddNode(G, Node("E", 10, 3))
GraphAddNode(G, Node("F", 7, 10))
GraphAddNode(G, Node("G", 12, 6))
GraphAddNode(G, Node("H", 3, 3))


# Add more segments (connections between nodes)
AddSegment(G, "AB", "A", "B")
AddSegment(G, "BC", "B", "C")
AddSegment(G, "CE", "C", "E")
AddSegment(G, "CD", "C", "D")
AddSegment(G, "DA", "D", "A")
AddSegment(G, "EF", "E", "F")
AddSegment(G, "FG", "F", "G")
AddSegment(G, "GH", "G", "H")
AddSegment(G, "HA", "H", "A")
AddSegment(G, "BG", "B", "G")
AddSegment(G, "CF", "C", "F")


# Print graph info
print("=== Graph Created ===")
print(f"Graph nodes: {[node.name for node in G.nodes]}")
print(f"Graph segments: {[segment.id for segment in G.segments]}")


# Test Path creation
print("\n=== Test Path Creation ===")
P = Path()
print(f"Empty path created: {P.nodes}, {P.costs}, {P.total_cost}")


# Test AddNodeToPath - using the module.function format to avoid conflicts
print("\n=== Test AddNode to Path ===")
print(f"Add node A: {path.AddNode(G, P, 'A')}")
print(f"Path nodes: {[node.name for node in P.nodes]}")
print(f"Path costs: {P.costs}")
print(f"Total cost: {P.total_cost}")


print(f"Add node B: {path.AddNode(G, P, 'B')}")
print(f"Path nodes: {[node.name for node in P.nodes]}")
print(f"Path costs: {P.costs}")
print(f"Total cost: {P.total_cost}")


print(f"Add node E (should fail - not connected): {path.AddNode(G, P, 'E')}")
print(f"Path nodes: {[node.name for node in P.nodes]}")


print(f"Add node A again (should fail - already in path): {path.AddNode(G, P, 'A')}")
print(f"Path nodes: {[node.name for node in P.nodes]}")


print(f"Add node C: {path.AddNode(G, P, 'C')}")
print(f"Path nodes: {[node.name for node in P.nodes]}")
print(f"Path costs: {P.costs}")
print(f"Total cost: {P.total_cost}")


# Test ContainsNode
print("\n=== Test ContainsNode ===")
path.ContainsNode(P, "A")  # Should be in path
path.ContainsNode(P, "E")  # Should not be in path


# Test CostToNode
print("\n=== Test CostToNode ===")
print(f"Cost to node A: {path.CostToNode(P, 'A')}")
print(f"Cost to node B: {path.CostToNode(P, 'B')}")
print(f"Cost to node C: {path.CostToNode(P, 'C')}")
print(f"Cost to node E (not in path): {path.CostToNode(P, 'E')}")


# Test PlotPath
print("\n=== Test PlotPath ===")
# Assuming PlotPath method is implemented correctly, this would show the path on a graph
path.PlotPath(G, P)


print("\n=== All tests completed ===")











