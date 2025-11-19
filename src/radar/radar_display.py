# radar/radar_display.py

import pygame
import math

class RadarDisplay:

    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.center = (width // 2, height // 2)

    # GRID
    def draw_grid(self, screen):
        for x in range(0, self.width, 100):
            pygame.draw.line(screen, (0, 40, 0), (x, 0), (x, self.height), 1)

        for y in range(0, self.height, 100):
            pygame.draw.line(screen, (0, 40, 0), (0, y), (self.width, y), 1)

    #RANGE RINGS
    def draw_rings(self, screen):
        for r in range(100, 800, 100):
            pygame.draw.circle(screen, (0, 70, 0), self.center, r, 1)

    # SWEEP
    def draw_sweep(self, screen, sweep_angle):
        rad = math.radians(sweep_angle - 90)
        sx = self.center[0] + 800 * math.cos(rad)
        sy = self.center[1] + 800 * math.sin(rad)
        pygame.draw.line(screen, (0, 255, 0), self.center, (sx, sy), 1)

    # CROSSHAIR
    def draw_crosshair(self, screen):
        pygame.draw.line(screen, (0, 100, 0), (self.center[0], 0), 
                         (self.center[0], self.height))
        pygame.draw.line(screen, (0, 100, 0), (0, self.center[1]), 
                         (self.width, self.center[1]))

    # SECTOR BOUNDARY (WEST / EAST SPLIT)
    def draw_sector_boundary(self, screen):
        pygame.draw.line(screen, (80, 80, 80),
                         (self.width // 2, 0),
                         (self.width // 2, self.height), 2)

    #  TCAS BUBBLES 
    def draw_tcas(self, screen, ac):
        if ac.tcas_alert == "RA":
            pygame.draw.circle(screen, (255, 0, 0), (int(ac.x), int(ac.y)), 80, 2)
        elif ac.tcas_alert == "TA":
            pygame.draw.circle(screen, (255, 255, 0), (int(ac.x), int(ac.y)), 200, 1)

    #  SELECTION HIGHLIGHT
    def draw_selection(self, screen, ac):
        pygame.draw.circle(screen, (255, 255, 0), (int(ac.x), int(ac.y)), 12, 2)

    # SELECTED AIRCRAFT HUD 
    def draw_selected_info(self, screen, selected_ac):
        info = (
            f"{selected_ac.id}  "
            f"HDG:{int(selected_ac.heading_degree)}  "
            f"ALT:{int(selected_ac.altitude)}  "
            f"SPD:{int(selected_ac.speed)}"
        )
        label = self.font.render(info, True, (255, 255, 0))
        screen.blit(label, (20, 20))

    # AIRPORT + AIRPORT SECTOR 
    def draw_airport(self, screen, airport):
        airport.draw(screen, self.font)

    def draw_airport_sector(self, screen, airport, radius):
        pygame.draw.circle(
            screen,
            (60, 60, 120),
            (int(airport.x), int(airport.y)),
            radius,
            2,
        )
