import pygame
from core.aircraft import Aircraft
import math

pygame.init()

WIDTH = 1400
HEIGHT = 800 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ATCASim Radar")

clock = pygame.time.Clock()

# Create ONE test aircraft (center)
plane = Aircraft(
    x = WIDTH // 2,         # start in the middle of screen
    y = HEIGHT // 2,
    heading_degrees = 0,    # 0° = NORTH (UP)
    speed = 150,            # pixels per second (temp)
    altitude = 10000
)

running = True
while running:

    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # dt = time between frames (seconds)
    dt = clock.tick(60) / 1000.0   # 60 FPS

    screen.fill((0, 0, 0))

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Draw crosshair (vertical + horizontal)
    pygame.draw.line(screen,( 0 ,100 , 0),(center_x ,0),(center_x,HEIGHT))
    pygame.draw.line(screen, (0 , 100, 0), (0, center_y), (WIDTH,center_y))

    rad = math.radians(plane.heading_degree - 90)

    dx = math.cos(rad) * plane.speed * dt
    dy = math.sin(rad) * plane.speed * dt

    plane.x += dx
    plane.y -= dy   # pygame y-axis is inverted (up = negative)

   
    pygame.draw.circle(
        screen,
        (0, 255, 0),                 # dot color
        (int(plane.x), int(plane.y)),# dot position
        5                            # radius
    )

    # Refresh the display
    pygame.display.flip()

    # Limit update to 60 FPS
    clock.tick(60)

pygame.quit()
