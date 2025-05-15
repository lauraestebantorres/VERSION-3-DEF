import unittest
from navSegment import NavSegment
from navPoint import NavPoint

class TestNavSegment(unittest.TestCase):
    def test_initialization(self):
        segment = NavSegment(5129, 8059, 109.63)
        self.assertEqual(segment.origin_number, 5129)
        self.assertEqual(segment.destination_number, 8059)
        self.assertAlmostEqual(segment.distance, 109.63)

    def test_distance_calculation(self):
        origin = NavPoint(5129, 'GODOX', 39.3725, 1.4108333333)
        destination = NavPoint(8059, 'POINT', 40.0, 2.0)
        segment = NavSegment(5129, 8059)
        segment.calculate_distance(origin, destination)
        self.assertGreater(segment.distance, 0)

if __name__ == '__main__':
    unittest.main()
