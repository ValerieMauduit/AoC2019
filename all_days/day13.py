# --- Day 13: Care Package ---

# First star:
# The arcade cabinet runs Intcode software like the game the Elves sent (your puzzle input). It has a primitive screen
# capable of drawing square tiles on a grid. The software draws tiles to the screen with output instructions: every
# three output instructions specify the x position (distance from the left), y position (distance from the top), and
# tile id. The tile id is interpreted as follows:
# - 0 is an empty tile. No game object appears in this tile.
# - 1 is a wall tile. Walls are indestructible barriers.
# - 2 is a block tile. Blocks can be broken by the ball.
# - 3 is a horizontal paddle tile. The paddle is indestructible.
# - 4 is a ball tile. The ball moves diagonally and bounces off objects.
#
# Start the game. How many block tiles are on the screen when the game exits?

# Second star:

from all_days.intcode import Opcoder
import numpy as np


def create_tiles(instructions):
    xvalues = [instructions[n] for n in range(0, len(instructions), 3)]
    xmin, xmax = min(xvalues), max(xvalues)
    yvalues = [instructions[n] for n in range(1, len(instructions), 3)]
    ymin, ymax = min(yvalues), max(yvalues)
    colors = [instructions[n] for n in range(2, len(instructions), 3)]
    tiles = np.zeros((ymax - ymin + 1, xmax - xmin + 1))
    for x, y, c in zip(xvalues, yvalues, colors):
        tiles[y, x] = c
    return tiles


def run(data_dir, star):
    with open(f'{data_dir}/input-day13.txt', 'r') as fic:
        opcodes = [int(x) for x in fic.read().split(',')]
    if star == 1:
        arcade_cabinet = Opcoder(opcodes)
        arcade_cabinet.run_until_exit()
        draw_instructions = arcade_cabinet.output_values
        arcade_screen = create_tiles(draw_instructions)
        nb_blocks = np.count_nonzero(arcade_screen == 2)
        print(f'Star {star} - There are {nb_blocks} blocks in the screen')
        return nb_blocks

    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
