class NavSegment:
   def __init__(self, origin_number, destination_number, distance):
       self.origin_number = int(origin_number)
       self.destination_number = int(destination_number)
       self.distance = float(distance)


   def __repr__(self):
       return f"NavSegment({self.origin_number} -> {self.destination_number}, {self.distance} km)"

