from node import Distance
import matplotlib.pyplot as plt

class Path:
    def __init__(self, nodes=None):
        self.nodes = nodes if nodes is not None else []
        self.costs = []
        self.total_cost = 0.0
        if len(self.nodes) > 1:
            for i in range(len(self.nodes) - 1):
                dist = Distance(self.nodes[i], self.nodes[i + 1])
                self.costs.append(dist)
                self.total_cost += dist

    def TotalCost(self):
        return self.total_cost

    def LastNode(self):
        return self.nodes[-1] if self.nodes else None

def AddNode(G, P, name):
    if not P.nodes:
        for node in G.nodes:
            if node.name == name:
                P.nodes.append(node)
                P.costs.append(0)
                return True
        return False
    last_node = P.nodes[-1]
    for node in G.nodes:
        if node.name == name:
            if ContainsNode(P, name):
                return False
            for segment in G.segments:
                if (segment.origin == last_node and segment.destination == node):
                    P.nodes.append(node)
                    dist = Distance(last_node, node)
                    P.costs.append(dist)
                    P.total_cost += dist
                    return True
    return False

def ContainsNode(P, name):
    for node in P.nodes:
        if node.name == name:
            print(f"The Node {name} belongs to the path")
            return True
    print(f"The Node {name} does not belong to the path")
    return False

def CostToNode(P, name):
    if not P.nodes:
        return -1
    total = 0
    for i, node in enumerate(P.nodes):
        if node.name == name:
            return total
        if i < len(P.costs):
            total += P.costs[i + 1]
    return -1

def PlotPath(G, P):
    plt.clf()
    for segment in G.segments:
        x = [segment.origin.x, segment.destination.x]
        y = [segment.origin.y, segment.destination.y]
        plt.plot(x, y, 'k-')
        plt.text((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, f'{segment.cost:.2f}', color='black')
    for node in G.nodes:
        plt.plot(node.x, node.y, 'ko')
        plt.text(node.x, node.y, node.name)
    if P.nodes:
        for i in range(len(P.nodes) - 1):
            x = [P.nodes[i].x, P.nodes[i + 1].x]
            y = [P.nodes[i].y, P.nodes[i + 1].y]
            plt.plot(x, y, 'r-', linewidth=2)
            plt.text((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, f'{P.costs[i + 1]:.2f}', color='red')
        for node in P.nodes:
            plt.plot(node.x, node.y, 'ro')
            plt.text(node.x, node.y, node.name, color='red')
    plt.title("Graph with Highlighted Path")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()