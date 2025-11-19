import pygame
import math

from core.aircraft import Aircraft
from core.traffic_manager import TrafficManager


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

    # Sweep line angle
    sweep_angle = 0

    running = True
    while running:

        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # dt = seconds per frame
        dt = clock.tick(60) / 1000.0

        #  UPDATE AIRCRAFT 
        traffic.update(dt)
        traffic.remove_aircraft_outside_airspace(WIDTH,HEIGHT) #removes aircrafts outside of the radar space 
        collisions, conflicts = traffic.detect_conflicts()

        # Print distances for conflicts
        for ac in traffic.planes:
             print(f"{ac.id} TCAS: {ac.tcas_alert}")



        #  SPAWN NEW AIRCRAFT 
        spawn_timer += dt
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            new_plane = traffic.spawn_random_plane(WIDTH, HEIGHT)
            traffic.add_aircraft(new_plane)


        screen.fill((0, 0, 0))

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # 1. Grid Lines
        for x in range(0, WIDTH, 100):
            pygame.draw.line(screen, (0, 40, 0), (x, 0), (x, HEIGHT), 1)

        for y in range(0, HEIGHT, 100):
            pygame.draw.line(screen, (0, 40, 0), (0, y), (WIDTH, y), 1)

        # 2. Range Rings
        for r in range(100, 800, 100):
            pygame.draw.circle(screen, (0, 70, 0), (center_x, center_y), r, 1)

        # 3. Radar Sweep Line
        sweep_angle = (sweep_angle + 50 * dt) % 360 #speed 
        rad = math.radians(sweep_angle - 90)
        sx = center_x + 800 * math.cos(rad) 
        sy = center_y + 800 * math.sin(rad)
        pygame.draw.line(screen, (0, 255, 0), (center_x, center_y), (sx, sy), 1)

        # 4. Center Crosshair
        pygame.draw.line(screen, (0, 100, 0), (center_x, 0), (center_x, HEIGHT))
        pygame.draw.line(screen, (0, 100, 0), (0, center_y), (WIDTH, center_y))
      
        for ac in traffic.planes:
            if ac.tcas_alert == "RA":
                pygame.draw.circle(screen, (255, 0, 0), (int(ac.x), int(ac.y)), 80, 2)
            elif ac.tcas_alert == "TA":
                pygame.draw.circle(screen, (255, 255, 0), (int(ac.x), int(ac.y)), 200, 1)
            ac.draw(screen, font)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
