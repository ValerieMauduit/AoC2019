# --- Day 3: Crossed Wires ---

# First star:
# The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back
# on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.
# Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend
# outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text.
# The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the
# intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this
# measurement. While the wires do technically cross right at the central port where they both start, this point does not
# count, nor does a wire count as crossing with itself.
# For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5,
# left 5, and finally down 3.
# What is the Manhattan distance from the central port to the closest intersection?

# Second star:
# It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.
# To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where
# the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value
# from the first time it visits that position when calculating the total value of a specific intersection.
# What is the fewest combined steps the wires must take to reach an intersection?

import pandas as pd


def deplacement(position, action):
    direction = action[0]
    if direction == 'R':
        LR, UD = 1, 0
    elif direction == 'L':
        LR, UD = -1, 0
    elif direction == 'U':
        LR, UD = 0, 1
    elif direction == 'D':
        LR, UD = 0, -1

    distance = int(action[1:])
    return [(position[0] + LR * d, position[1] + UD * d) for d in range(1, distance + 1)]


def run(data_dir, star):
    with open(f'{data_dir}/input-day03.txt', 'r') as fic:
        wires = [x.split(',') for x in fic.read().strip('\n').split('\n')]
    wire1 = [(0, 0)]
    for action in wires[0]:
        wire1 += deplacement(wire1[-1], action)
    wire2 = [(0, 0)]
    for action in wires[1]:
        wire2 += deplacement(wire2[-1], action)

    w1 = pd.DataFrame({
        'x': [p[0] for p in wire1], 'y': [p[1] for p in wire1], 'd': [abs(p[0]) + abs(p[1]) for p in wire1]})
    w2 = pd.DataFrame({
        'x': [p[0] for p in wire2], 'y': [p[1] for p in wire2], 'd': [abs(p[0]) + abs(p[1]) for p in wire2]})

    if star == 1:    # Answer is 225
        w1 = w1.sort_values(by='d')
        w2 = w2.sort_values(by='d')
        ww = pd.merge(w1, w2, how='inner', on='d', suffixes=('1', '2'))
        closest_intersection = ww.loc[(ww['x1'] == ww['x2']) & (ww['y1'] == ww['y2'])].iloc[1, 2]

        print(f'Star {star} - Closest intersection Manhattan distance is {closest_intersection}')
        return closest_intersection

    elif star == 2:  # Answer is 35194
        w1['l'] = w1.index.astype(int)
        w2['l'] = w2.index.astype(int)
        ww = pd.merge(w1, w2, how='inner', on='d', suffixes=('1', '2'))

        ww['l_total'] = ww['l1'] + ww['l2']
        ww = ww.sort_values(by='l_total')
        best_intersection = ww.loc[(ww['x1'] == ww['x2']) & (ww['y1'] == ww['y2'])].iloc[1, -1]

        print(f'Star {star} - Best intersection Manhattan distance is {best_intersection}')
        return best_intersection

    else:
        raise Exception('Star number must be either 1 or 2.')
