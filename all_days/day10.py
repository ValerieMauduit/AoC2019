# --- Day 10: Monitoring Station ---

# First star:
# The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller than
# they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids can be
# described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the top edge
# (so the top-left corner is 0,0 and the position immediately to its right is 1,0).
# Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring
# station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid
# exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally. The
# best location is the asteroid that can detect the largest number of other asteroids.
# Find the best location for a new monitoring station. How many other asteroids can be detected from that location?

# Second star:

from math import gcd
from copy import deepcopy

def count_asteroids(asteroids_map, position):
    counting_map = deepcopy(asteroids_map)
    counting_map[position[1]][position[0]] = 'o'
    nb_asteroids = 0
    width, height = len(counting_map[0]), len(counting_map)
    for y in range(height):
        for x in range(width):
            if counting_map[y][x] == '#':
                nb_asteroids += 1
                dx, dy = (position[0] - x), (position[1] - y)
                alpha = gcd(dx, dy)
                dx = int(dx / alpha)
                dy = int(dy / alpha)
                (x0, y0) = position
                while (x0 >= 0) and (y0 >= 0) and (x0 < width) and (y0 < height):
                    counting_map[y0][x0] = 'o'
                    x0 -= dx
                    y0 -= dy
    return nb_asteroids


def find_best_place(asteroids_map):
    counts_map = [[0 for _ in raw] for raw in asteroids_map]
    for x in range(len(asteroids_map[0])):
        for y in range(len(asteroids_map)):
            if asteroids_map[y][x] == '#':
                counts_map[y][x] = count_asteroids(asteroids_map, (x, y))
    best_value = max([max(raw) for raw in counts_map])
    ymax = [n for n in range(len(counts_map)) if best_value in counts_map[n]][0]
    xmax = counts_map[ymax].index(best_value)
    return {'value': best_value, 'position': (xmax, ymax), 'map': counts_map}


def run(data_dir, star):
    with open(f'{data_dir}/input-day10.txt', 'r') as fic:
        asteroids_map = [[v for v in x] for x in fic.read().strip('\n').split('\n')]
    if star == 1:
        solution = find_best_place(asteroids_map)
        print(f'Star {star} - detected asteroids: {solution["value"]}')
        return
    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
