import unittest
from navAirport import NavAirport
from navPoint import NavPoint

class TestNavAirport(unittest.TestCase):
    def test_initialization(self):
        airport = NavAirport("LEBL")
        self.assertEqual(airport.name, "LEBL")
        self.assertEqual(len(airport.sids), 0)
        self.assertEqual(len(airport.stars), 0)

    def test_add_sid_and_star(self):
        airport = NavAirport("LEBL")
        sid = NavPoint(6063, "IZA.D", 38.877, 1.369)
        star = NavPoint(6062, "IZA.A", 38.873, 1.372)
        airport.add_sid(sid)
        airport.add_star(star)
        self.assertIn(sid, airport.sids)
        self.assertIn(star, airport.stars)

if __name__ == '__main__':
    unittest.main()
