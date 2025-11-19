import pygame
import math
from core.controller import ATC_controller
from core.aircraft import Aircraft
from core.traffic_manager import TrafficManager
from radar.radar_display import RadarDisplay
from simulation.airports import Airport

selected_ac = None  

# Tower radius (pixels) around the airport
TOWER_RADIUS = 250

def main():
    pygame.init()

    WIDTH = 1400
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ATCASim Radar")

    clock = pygame.time.Clock()

    # Radar font for aircraft labels
    font = pygame.font.SysFont("Arial", 14)

    # Radar display helper
    display = RadarDisplay(WIDTH, HEIGHT, font)

    # Traffic manager holds ALL aircraft
    traffic = TrafficManager()

    # Spawn 5 aircraft at startup
    for _ in range(5):
        new_plane = traffic.spawn_random_plane(WIDTH, HEIGHT)
        traffic.add_aircraft(new_plane)

    # Airport at the center of the radar
    airport = Airport("ATC-HUB", WIDTH // 2, HEIGHT // 2)

    # --- ATC CONTROLLERS ---
    west_atc  = ATC_controller("WEST Controller", 0, WIDTH // 2)
    east_atc  = ATC_controller("EAST Controller", WIDTH // 2, WIDTH)
    tower_atc = ATC_controller("TOWER", airport.x - TOWER_RADIUS, airport.x + TOWER_RADIUS)

    def get_controller(ac):
        """Return which ATC currently controls this aircraft."""
        # Check if inside tower bubble (distance from airport)
        dx = ac.x - airport.x
        dy = ac.y - airport.y
        if dx*dx + dy*dy <= TOWER_RADIUS * TOWER_RADIUS:
            return tower_atc

        # Otherwise west/east based on x
        if west_atc.space(ac):
            return west_atc
        else:
            return east_atc

    # Timer for continuous traffic spawning
    spawn_timer = 0
    spawn_interval = 3  # seconds

    # Sweep line angle
    sweep_angle = 0

    running = True
    while running:

        # Handle quit events + MOUSE CLICKS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detect aircraft selection
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                global selected_ac
                selected_ac = None  # reset

                for ac in traffic.planes:
                    dx = ac.x - mx
                    dy = ac.y - my
                    dist = (dx*dx + dy*dy)**0.5

                    if dist <= 10:  # clicked near plane dot
                        selected_ac = ac
                        print("Selected aircraft:", ac.id)
                        break

        # dt = seconds per frame
        dt = clock.tick(60) / 1000.0

        # UPDATE AIRCRAFT 
        traffic.update(dt)
        traffic.remove_aircraft_outside_airspace(WIDTH, HEIGHT)
        collisions, conflicts = traffic.detect_conflicts()

        # SPAWN NEW AIRCRAFT
        spawn_timer += dt
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            new_plane = traffic.spawn_random_plane(WIDTH, HEIGHT)
            traffic.add_aircraft(new_plane)

        # ---------------- DRAW EVERYTHING ----------------
        screen.fill((0, 0, 0))

        # Radar components
        display.draw_grid(screen)
        display.draw_rings(screen)
        display.draw_sweep(screen, sweep_angle)
        display.draw_crosshair(screen)
        display.draw_sector_boundary(screen)        # west/east split line
        display.draw_airport_sector(screen, airport, TOWER_RADIUS)  # tower bubble
        display.draw_airport(screen, airport)       # airport symbol

        sweep_angle = (sweep_angle + 50 * dt) % 360

        # Draw planes
        for ac in traffic.planes:

            display.draw_tcas(screen, ac)

            if ac is selected_ac:
                display.draw_selection(screen, ac)

            ac.draw(screen, font)

        # Draw selected aircraft HUD + controlling ATC
        if selected_ac:
            display.draw_selected_info(screen, selected_ac)

            controller = get_controller(selected_ac)
            sector_text = f"Controlled by: {controller.name}"
            label = font.render(sector_text, True, (0, 200, 255))
            screen.blit(label, (20, 40))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
