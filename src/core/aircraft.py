import math 

class Aircarft:
    def __init__(self, x: int , y: int , heading_degrees: int , speed :int , altitude: int , verticle_speed):
        self.x = x
        self.y = y
        self.heading_degree = heading_degrees
        self.speed = speed
        self.altitude = altitude
        self.verticle_speed = 0

    def turn(self , delta_degree :int ):
        self.heading_degree = (self.heading_degree + delta_degree)% 360 #updates the currents aircraft heading
   
    def set_heading(self, traget_degree :int):
        self.heading_degree = traget_degree % 360 
    
    def verticle_speed(self, vs: int):
        self.verticle_speed = vs
    
    def set_altitude(self, target_altitude:int):
        self.altitude = max(0 , target_altitude)

    def update(self, last_update_time :float):
       
        #calculate movement 
        rad = math.radians(self.heading_degree)   #convert it into radian(for python trig (it cant use degrees) )
        dx = math.cos(rad) * self.speed * last_update_time  # cos - hortizontal
        dy = math.sin(rad) * self.speed * last_update_time  # sin - verticle
        
        #update postion of the aircraft 
        self.x = self.x + dx
        self.y = self.y + dy

    #updates the alititube( example - climb 1000 feet, + 1000 to the orginal altitude)
    def change_altitude(self, delta_altitude:int):
        new_altitude = self.altitude + delta_altitude
        self.altitude = max(0, new_altitude)
    






