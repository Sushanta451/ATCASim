# simulation/airports.py

import pygame

class Airport:
    """
    Simple airport object located at (x, y).
    Draws an icon + label on the radar.
    """

    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y

    def draw(self, screen, font):
        # Outer circle (airport area)
        pygame.draw.circle(screen, (160, 160, 160), (int(self.x), int(self.y)), 10)
        # Inner dot (runway/center)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), 4)

        # Label
        label = font.render(self.name, True, (200, 200, 200))
        screen.blit(label, (self.x + 14, self.y - 10))
