class ATC_controller:
    # controller airspace 
    def __init__(self, name, x_min, x_max):
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
    
    def space(self, ac):
        return self.x_min <= ac.x < self.x_max
    
    def give_heading(self, ac, heading_degree):
        ac.command_heading(heading_degree)
    
    def give_altitude(self, ac, alt):
        ac.command_altitude(alt)
    
    def give_speed(self, ac, spd):
        ac.command_speed(spd)
