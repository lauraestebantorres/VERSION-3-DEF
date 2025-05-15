class NavAirport:
   def __init__(self, name):
       self.name = name
       self.sids = []  # list of NavPoint
       self.stars = []  # list of NavPoint


   def __repr__(self):
       return f"NavAirport({self.name}, SIDs: {[p.name for p in self.sids]}, STARs: {[p.name for p in self.stars]})"
