import unittest
from segment import Segment
from node import Node

class TestSegment(unittest.TestCase):
    def test_initialization(self):
        node1 = Node('A', 0, 0)
        node2 = Node('B', 3, 4)
        segment = Segment('AB', node1, node2)
        self.assertEqual(segment.name, 'AB')
        self.assertEqual(segment.origin, node1)
        self.assertEqual(segment.destination, node2)
        self.assertAlmostEqual(segment.cost, 5.0)

if __name__ == '__main__':
    unittest.main()
