import math

COLLISION_RADIUS = 8
CONFLICT_RADIUS = 400
COLLISION_ALTITUDE_DIFF = 200
CONFLICT_ALTITUDE_DIFF = 1000

# Horizontal distance in pixels
def horizontal_distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

# Vertical separation in feet
def vertical_distance(a, b):
    return abs(a.altitude - b.altitude)

# Decision for a pair of aircraft
def check_pair(a, b):
    d = horizontal_distance(a, b)
    alt = vertical_distance(a, b)

    # Collision (very close)
    if d < COLLISION_RADIUS and alt < COLLISION_ALTITUDE_DIFF:
        return "COLLISION"

    # Conflict (loss of separation)
    if d < CONFLICT_RADIUS and alt < CONFLICT_ALTITUDE_DIFF:
        return "CONFLICT"

    return "SAFE"

# Scan all aircraft pairs
def scan_all(aircraft_list):
    print("[TCAS] scan_all is running… plane count:", len(aircraft_list))
    collisions = []
    conflicts = []

    for i in range(len(aircraft_list)):
        for j in range(i + 1, len(aircraft_list)):

            a = aircraft_list[i]
            b = aircraft_list[j]

            status = check_pair(a, b)

            if status == "COLLISION":
                collisions.append((a, b))
            elif status == "CONFLICT":
                conflicts.append((a, b))

    return collisions, conflicts

