from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport


class AirSpace:
   def __init__(self):
       self.nav_points = []
       self.nav_segments = []
       self.nav_airports = []


   def get_point_by_number(self, number):
       return next((p for p in self.nav_points if p.number == int(number)), None)


   def get_point_by_name(self, name):
       return next((p for p in self.nav_points if p.name == name), None)


   def load_nav_points(self, filename):
       with open(filename, 'r') as f:
           for line in f:
               if line.strip():
                   parts = line.split()
                   number = parts[0]
                   name = parts[1]
                   lat = parts[2]
                   lon = parts[3]
                   self.nav_points.append(NavPoint(number, name, lat, lon))


   def load_nav_segments(self, filename):
       with open(filename, 'r') as f:
           for line in f:
               if line.strip():
                   origin, dest, dist = line.split()
                   self.nav_segments.append(NavSegment(origin, dest, dist))


   def load_nav_airports(self, filename):
       with open(filename, 'r') as f:
           current_airport = None
           for line in f:
               line = line.strip()
               if not line:
                   continue
               if line.startswith('LE'):  # airport code
                   if current_airport:
                       self.nav_airports.append(current_airport)
                   current_airport = NavAirport(line)
               elif line.endswith('.D') and current_airport:
                   point = self.get_point_by_name(line)
                   if point:
                       current_airport.sids.append(point)
               elif line.endswith('.A') and current_airport:
                   point = self.get_point_by_name(line)
                   if point:
                       current_airport.stars.append(point)
           if current_airport:
               self.nav_airports.append(current_airport)


   def load_all(self, nav_file, seg_file, aer_file):
       self.load_nav_points(nav_file)
       self.load_nav_segments(seg_file)
       self.load_nav_airports(aer_file)




   def __repr__(self):
       return f"AirSpace(NavPoints: {len(self.nav_points)}, NavSegments: {len(self.nav_segments)}, NavAirports: {len(self.nav_airports)})"

