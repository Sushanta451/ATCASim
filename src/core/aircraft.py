import math 

class Aircraft:
    # max/min altitude limits (added)
    MAX_ALTITUDE = 45000
    MIN_ALTITUDE = 0
    
    # max/min vertical speed limits (added)
    MAX_VERTICAL_SPEED = 3000     # climb max ft/min
    MIN_VERTICAL_SPEED = -3000    # descent max ft/min

    def __init__(self, x: int , y: int , heading_degrees: int , speed: int , altitude: int):
        self.x = x
        self.y = y
        self.heading_degree = heading_degrees
        self.speed = speed
        self.altitude = altitude
        self.vertical_speed = 0   # starting VS is level flight (0 ft/min)

    def turn(self , delta_degree :int ):
        # updates the currents aircraft heading
        self.heading_degree = (self.heading_degree + delta_degree) % 360 
   
    def set_heading(self, target_degree :int):
        # sets heading exactly (ATC command like "fly heading 260")
        self.heading_degree = target_degree % 360 
    
    def set_vertical_speed(self, vs: int):
        # clamp vertical speed between max climb and max descent
        vs = max(self.MIN_VERTICAL_SPEED, min(vs, self.MAX_VERTICAL_SPEED))
        self.vertical_speed = vs
    
    def set_altitude(self, target_altitude:int):
        # clamp the altitude between 0 and MAX altitude
        self.altitude = max(self.MIN_ALTITUDE, 
                            min(target_altitude, self.MAX_ALTITUDE))

    def update(self, last_update_time :float):
        # calculate movement 
        rad = math.radians(self.heading_degree)   # convert it into radian(for python trig (it cant use degrees) )
        dx = math.cos(rad) * self.speed * last_update_time  # cos - hortizontal
        dy = math.sin(rad) * self.speed * last_update_time  # sin - vertical

        # update postion of the aircraft 
        self.x = self.x + dx
        self.y = self.y + dy

        # convert vertical speed (ft/min) into ft/sec
        altitude_change_persec = self.vertical_speed / 60

        # apply dt correctly (your original code added dt incorrectly — fixed)
        self.altitude += altitude_change_persec * last_update_time
        
        # clamp altitude so it never below 0 or above max altitude
        self.altitude = max(self.MIN_ALTITUDE, 
                            min(self.altitude, self.MAX_ALTITUDE))

    # updates the alititube( example - climb 1000 feet, + 1000 to the orginal altitude)
    def change_altitude(self, delta_altitude:int):
        new_altitude = self.altitude + delta_altitude
        
        # clamp the altitude so it doesn't go below 0 or above max
        self.altitude = max(self.MIN_ALTITUDE, 
                            min(new_altitude, self.MAX_ALTITUDE))
