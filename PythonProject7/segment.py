from node import Node

class Segment:
    def __init__(self, name, origin: Node, destination: Node):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Node.distance(origin, destination)

    def __repr__(self):
        return f"Segment({self.name}, {self.origin.name} -> {self.destination.name}, Cost: {self.cost:.2f})"