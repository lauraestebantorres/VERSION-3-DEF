
# navPoint.py
class NavPoint:
   def __init__(self, number, name, latitude, longitude):
       self.number = int(number)
       self.name = name
       self.latitude = float(latitude)
       self.longitude = float(longitude)


   def __repr__(self):
       return f"NavPoint({self.number}, {self.name}, {self.latitude}, {self.longitude})"

