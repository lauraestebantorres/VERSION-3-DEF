import unittest
from node import Node

class TestNode(unittest.TestCase):
    def test_initialization(self):
        node = Node('A', 0, 0)
        self.assertEqual(node.name, 'A')
        self.assertEqual(node.x, 0)
        self.assertEqual(node.y, 0)

    def test_add_neighbor(self):
        node1 = Node('A', 0, 0)
        node2 = Node('B', 1, 1)
        self.assertTrue(node1.add_neighbor(node2))
        self.assertFalse(node1.add_neighbor(node2))  # Adding the same neighbor again

    def test_distance(self):
        node1 = Node('A', 0, 0)
        node2 = Node('B', 3, 4)
        self.assertEqual(Node.distance(node1, node2), 5.0)

if __name__ == '__main__':
    unittest.main()
