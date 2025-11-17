import random
from core.aircraft import Aircraft

class TrafficManager:

    def __init__(self):
        self.planes = []
    
    #add aircraft to the list
    def add_aircraft(self, ac):
        self.planes.append(ac)
    
    def update(self, dt):
        for i in self.planes: #update each frame
            i.update(dt)
    
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

      speed = random.randint(120, 200)
      altitude = random.randint(5000, 35000)

      return Aircraft(x, y, heading, speed, altitude)


