import pygame
from core.aircraft import Aircraft
from core.traffic_manager import TrafficManager
import math

def main():
    pygame.init()

    WIDTH = 1400
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ATCASim Radar")

    clock = pygame.time.Clock()

    # Radar font for aircraft labels
    font = pygame.font.SysFont("Arial", 14)

    # Traffic manager holds ALL aircraft
    traffic = TrafficManager()

    # Spawn 5 aircraft at startup
    for _ in range(5):
        new_plane = traffic.spawn_random_plane(WIDTH, HEIGHT)
        traffic.add_aircraft(new_plane)

    # Timer for continuous traffic spawning
    spawn_timer = 0
    spawn_interval = 3  # seconds

    running = True
    while running:

        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # dt = seconds per frame
        dt = clock.tick(60) / 1000.0

        # UPDATE ALL AIRCRAFT
        traffic.update(dt)

        # SPAWN NEW AIRCRAFT OVER TIME
        spawn_timer += dt
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            new_plane = traffic.spawn_random_plane(WIDTH, HEIGHT)
            traffic.add_aircraft(new_plane)

        # DRAW SCREEN
        screen.fill((0, 0, 0))

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Radar crosshair
        pygame.draw.line(screen, (0,100,0), (center_x, 0), (center_x, HEIGHT))
        pygame.draw.line(screen, (0,100,0), (0, center_y), (WIDTH, center_y))

        # Draw every aircraft in traffic
        for ac in traffic.planes:
            ac.draw(screen, font)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
