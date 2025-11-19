import math
import random
import pygame

class Aircraft:

    Airline_company = [
        "AAL", "DAL",
        "UAL", "SWA",
        "JBU", "UPS",
    ]

    # max/min altitude limits 
    MAX_ALTITUDE = 45000
    MIN_ALTITUDE = 0
    
    # max/min vertical speed limits 
    MAX_VERTICAL_SPEED = 3000     # climb max ft/min
    MIN_VERTICAL_SPEED = -3000    # descent max ft/min

    def __init__(self, x: int, y: int, heading_degrees: int, speed, altitude: int):
        self.x = x
        self.y = y
        self.heading_degree = heading_degrees
        self.speed = speed
        self.altitude = altitude
        self.vertical_speed = 0   # starting VS is level flight (0 ft/min)
        self.tcas_alert = None

        # ATC command targets
        self.target_heading = self.heading_degree
        self.target_altitude = self.altitude
        self.target_speed = self.speed

        # random airline callsign
        self.id = random.choice(self.Airline_company) + str(random.randint(100, 999))

    def turn(self, delta_degree: int):
        # updates the current aircraft heading
        self.heading_degree = (self.heading_degree + delta_degree) % 360 
   
    def set_heading(self, target_degree: int):
        # sets heading exactly (ATC command like "fly heading 260")
        self.heading_degree = target_degree % 360 
    
    def set_vertical_speed(self, vs: int):
        # clamp vertical speed between max climb and max descent
        vs = max(self.MIN_VERTICAL_SPEED, min(vs, self.MAX_VERTICAL_SPEED))
        self.vertical_speed = vs
    
    def set_altitude(self, target_altitude: int):
        # clamp the altitude between 0 and MAX altitude
        self.altitude = max(self.MIN_ALTITUDE, min(target_altitude, self.MAX_ALTITUDE))

    
    def command_heading(self, heading_degree):
        self.target_heading = heading_degree % 360

    def command_altitude(self, target_alti):
        self.target_altitude = max(self.MIN_ALTITUDE, min(target_alti, self.MAX_ALTITUDE))

    def command_speed(self, target_spd):
        self.target_speed = max(50, min(target_spd, 600))  # realistic speed clamp


    def update(self, dt: float):
        # Convert aviation heading to math heading (aviation 0° = North)
        rad = math.radians(self.heading_degree - 90)

        # Movement (correct Y direction)
        dx = math.cos(rad) * self.speed * dt
        dy = math.sin(rad) * self.speed * dt

        self.x += dx
        self.y += dy

        # Vertical speed ft/min → ft/sec
        altitude_change_persec = self.vertical_speed / 60
        self.altitude += altitude_change_persec * dt

        # Clamp altitude
        self.altitude = max(self.MIN_ALTITUDE, min(self.altitude, self.MAX_ALTITUDE))

       
        # shortest turn direction (-180 to +180)
        heading_diff = (self.target_heading - self.heading_degree + 540) % 360 - 180
        turn_rate = 2.0  # degrees per second (realistic)
        self.heading_degree += max(-turn_rate * dt, min(turn_rate * dt, heading_diff))

       
        altitude_diff = (self.target_altitude - self.altitude)
        climb_rate = 1500  # ft/min
        climb_rate_per_sec = climb_rate / 60

        self.altitude += max(-climb_rate_per_sec * dt,
                             min(climb_rate_per_sec * dt, altitude_diff))

       
        speed_diff = (self.target_speed - self.speed)
        speed_rate = 5  # knots per second
        self.speed += max(-speed_rate * dt, min(speed_rate * dt, speed_diff))

   
    def update_tcas(self, all_aircraft):
        self.tcas_alert = None  # reset every frame
      
        for i in all_aircraft:
            if i is self:
                continue  

            alert = self.compute_tcas_alert(i)

            if alert == "RA":
                self.tcas_alert = "RA"
                return   # RA overrides all
            elif alert == "TA" and self.tcas_alert is None:
                self.tcas_alert = "TA"

    def change_altitude(self, delta_altitude: int):
        # updates the altitude (example - climb 1000 feet, +1000 to original altitude)
        new_altitude = self.altitude + delta_altitude
        
        # clamp altitude
        self.altitude = max(self.MIN_ALTITUDE, min(new_altitude, self.MAX_ALTITUDE))

    def draw(self, screen, font):
        # 1. Aircraft dot (green)
        pygame.draw.circle(screen, (0,255,0), (int(self.x), int(self.y)), 4)

        # 2. Heading line (12px long)
        rad = math.radians(self.heading_degree - 90)
        hx = self.x + 12 * math.cos(rad)
        hy = self.y + 12 * math.sin(rad)
        pygame.draw.line(screen, (0,255,0), (self.x, self.y), (hx, hy), 2)

        # 3. Callsign and flight level label
        text = f"{self.id} FL{int(self.altitude // 100)}"
        label = font.render(text, True, (0,255,0))
        screen.blit(label, (self.x + 10, self.y - 15))

    def compute_tcas_alert(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        horizontal = math.sqrt(dx*dx + dy*dy)  # calculates the distance 
        alt_diff = abs(self.altitude - other.altitude) 

        if horizontal <= 80 and alt_diff <= 400:
            return "RA"
        
        if horizontal <= 200 and alt_diff <= 800:
            return "TA"

        return None

    def __str__(self):
        return (
            f"Aircraft {self.id}: "
            f"Pos=({self.x:.1f}, {self.y:.1f}), "
            f"Heading={self.heading_degree}°, "
            f"Speed={self.speed}, "
            f"Altitude={self.altitude:.1f} ft, "
            f"VS={self.vertical_speed} ft/min"
        )
