class Aircarft:
    def __init__(self, x: int , y: int , heading_degrees: int , speed :int):
        self.x = x
        self.y = y
        self.heading_degree = heading_degrees
        self.speed = speed
    
    def turn(self , delta_degree :int ):
        self.heading_degree = (self.heading_degree + delta_degree)% 360
    def set_heading(self, traget_degree :int):
        self.heading_degree = traget_degree % 360
    