import random
from core.aircraft import Aircraft
import core.tcas as tcas


class TrafficManager:

    def __init__(self):
        self.planes = []
    
    #add aircraft to the list
    def add_aircraft(self, ac):
        self.planes.append(ac)
    
    def update(self, dt):
        for i in self.planes: #update each frame
            i.update(dt)
        
        for i in self.planes:
           i.update_tcas(self.planes)
    
    def spawn_random_plane(self, WIDTH, HEIGHT):
    
      side = random.choice(["top", "bottom", "left", "right"])

      if side == "top":
        x = random.randint(0, WIDTH)
        y = 0
        heading = random.randint(170, 190)   # coming DOWN

      elif side == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT
        # coming UP (wrap-around heading)
        heading = random.choice([
            random.randint(350, 359),
            random.randint(0, 10)
        ])

      elif side == "left":
        x = 0
        y = random.randint(0, HEIGHT)
        heading = random.randint(80, 100)    # going RIGHT

      else:  # right
        x = WIDTH
        y = random.randint(0, HEIGHT)
        heading = random.randint(260, 280)   # going LEFT

      speed = random.randint(20, 100)
      altitude = random.randint(5000, 6000)

      return Aircraft(x, y, heading, speed, altitude)
    
    def remove_aircraft_outside_airspace(self, WIDTH, HEIGHT):

     removing_aircraft_list = []

     for ac in self.planes:
        if -50 <= ac.x <= WIDTH + 50 and -50 <= ac.y <= HEIGHT + 50:
            removing_aircraft_list.append(ac)

     self.planes = removing_aircraft_list

    
    def detect_conflicts(self):
        return tcas.scan_all(self.planes)

    

    
        
          



