import pygame
from core.aircraft import Aircraft
import math

def main():
    pygame.init()

    WIDTH = 1400
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ATCASim Radar")

    clock = pygame.time.Clock()

    # Create ONE test aircraft
    plane = Aircraft(
        x = WIDTH // 2,     # start in the middle
        y = HEIGHT // 2,
        heading_degrees = 0,   # 0 = North (UP)
        speed = 150,           # pixels per second
        altitude = 10000
    )

    running = True
    while running:

        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # dt = seconds per frame
        dt = clock.tick(60) / 1000.0

        # UPDATE AIRCRAFT PHYSICS
        plane.update(dt)

        print("x:", plane.x, "y:", plane.y, "dt:", dt)

        # DRAW SCREEN
        screen.fill((0, 0, 0))

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Radar crosshair
        pygame.draw.line(screen, (0,100,0), (center_x, 0), (center_x, HEIGHT))
        pygame.draw.line(screen, (0,100,0), (0, center_y), (WIDTH, center_y))

        # Draw aircraft dot
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (int(plane.x), int(plane.y)),
            5
        )
        print("x:", plane.x, "y:", plane.y, "heading:", plane.heading_degree)

        pygame.display.flip()

    pygame.quit()


