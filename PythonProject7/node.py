import math

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            return True
        return False

    @staticmethod
    def distance(n1, n2):
        return math.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)

    def __repr__(self):
        return f"Node({self.name}, {self.x}, {self.y}, Neighbors: {len(self.neighbors)})"