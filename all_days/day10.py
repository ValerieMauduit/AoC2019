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
# There are simply too many asteroids. The only solution is complete vaporization by giant laser.
# The laser starts by pointing up and always rotates clockwise, vaporizing any asteroid it hits.
# If multiple asteroids are exactly in line with the station, the laser only has enough power to vaporize one of them
# before continuing its rotation. In other words, the same asteroids that can be detected can be vaporized, but if
# vaporizing one asteroid makes another one detectable, the newly-detected asteroid won't be vaporized until the laser
# has returned to the same position by rotating a full 360 degrees.
# The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which
# asteroid that will be; what do you get if you multiply its X coordinate by 100 and then add its Y coordinate?


from math import gcd, sqrt
from numpy import round
from copy import deepcopy
import pandas as pd

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


def rotation(position):
    length = sqrt(position[0] ** 2 + position[1] ** 2)
    if (position[0] >= 0) and (position[1] <= 0):
        return round(position[0] / length, 6)
    elif position[1] > 0:
        return round(2 - position[0] / length, 6)
    elif (position[0] < 0) and (position[1] <= 0):
        return round(4 + position[0] / length, 6)


def vaporization_lazer(asteroids_map, position):
    df = pd.DataFrame(columns=['x', 'y', 'distance', 'rotation'])
    width, height = (len(asteroids_map[0])), (len(asteroids_map))
    n = 0
    for x in range(width):
        for y in range(height):
            if asteroids_map[y][x] == '#':
                dx = x - position[0]
                dy = y - position[1]
                df = df.append(pd.DataFrame(data={
                    'x': x, 'y': y,
                    'distance': abs(dx) + abs(dy),
                    'rotation': rotation((dx, dy))
                }, index=[n]))
                n += 1
    df.sort_values(by=['rotation','distance'], inplace=True)

    asteroids_order = [(0, 0)]
    nb_asteroids = sum([raw.count('#') for raw in asteroids_map])
    while nb_asteroids > 0:
        dfloc = df.copy()
        while dfloc.shape[0] > 0:
            asteroids_order += [(dfloc.iloc[0]['x'], dfloc.iloc[0]['y'])]
            nb_asteroids -= 1
            df.drop([dfloc.index[0]], inplace=True)
            dfloc = dfloc[dfloc['rotation'] > dfloc.iloc[0]['rotation']]
    return asteroids_order


def run(data_dir, star):
    with open(f'{data_dir}/input-day10.txt', 'r') as fic:
        asteroids_map = [[v for v in x] for x in fic.read().strip('\n').split('\n')]
    positionning_laser = find_best_place(asteroids_map)
    if star == 1:
        print(f'Star {star} - detected asteroids: {positionning_laser["value"]}')
        return
    elif star == 2:
        best_position = positionning_laser['position']
        asteroids_map[best_position[1]][best_position[0]] = 'X'
        asteroids_order = vaporization_lazer(asteroids_map, best_position)
        asteroid200 = asteroids_order[200]
        solution = asteroid200[0] * 100 + asteroid200[1]
        print(f'Star {star} - The 200th asteroid is on position {asteroid200}, so the soution is {solution}')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
