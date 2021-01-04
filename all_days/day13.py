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
# Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.
# The arcade cabinet has a joystick that can move left and right. The software reads the position of the joystick with
# input instructions:
# - If the joystick is in the neutral position, provide 0.
# - If the joystick is tilted to the left, provide -1.
# - If the joystick is tilted to the right, provide 1.
# The arcade cabinet also has a segment display capable of showing a single number that represents the player's current
# score. When three output instructions specify X=-1, Y=0, the third output instruction is not a tile; the value instead
# specifies the new score to show in the segment display. For example, a sequence of output values like -1,0,12345 would
# show 12345 as the player's current score.
# Beat the game by breaking all the blocks. What is your score after the last block is broken?

from all_days.intcode import Opcoder
import numpy as np


def create_tiles(instructions):
    xvalues = [instructions[n] for n in range(0, len(instructions), 3)]
    xmax = max(xvalues)
    yvalues = [instructions[n] for n in range(1, len(instructions), 3)]
    ymax = max(yvalues)
    colors = [instructions[n] for n in range(2, len(instructions), 3)]
    tiles = np.zeros((ymax + 1, xmax + 1))
    for x, y, c in zip(xvalues, yvalues, colors):
        if x >= 0:
            tiles[y, x] = c
    return tiles


def get_score(instructions):
    score = [
        instructions[n + 2]
        for n in range(0, len(instructions), 3)
        if instructions[n] == -1 and instructions[n + 1] == 0
    ]
    return score[-1]


def print_screen(screen):
    block_type = {0: ' ', 1: '+', 2: '#', 3: '_', 4: 'O'}
    printable_screen = [''.join([block_type[x] for x in raw]) for raw in screen]
    for raw in printable_screen:
        print(raw)


def run_arcade(arcade_game):
    step = 0
    nb_blocks = 1
    while nb_blocks > 0:
        step += 1
        arcade_game.run_step()
        arcade_game.run_until_next_input()
        draw_instructions = arcade_game.output_values
        arcade_screen = create_tiles(draw_instructions)
        get_score(draw_instructions)

        _, xball = np.where(arcade_screen == 4)
        _, xpaddle = np.where(arcade_screen == 3)
        arcade_game.inputs(np.sign(xball[0] - xpaddle[0]))
        nb_blocks = np.count_nonzero(arcade_screen == 2)
        if step % 500 == 0:
            print(step)
            print_screen(arcade_screen)
            print(f'=== {get_score(draw_instructions)}')

    print(step)
    print_screen(arcade_screen)
    print(f'=== {get_score(draw_instructions)}')
    return get_score(draw_instructions)


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
        opcodes[0] = 2
        arcade_cabinet = Opcoder(opcodes)
        final_score = run_arcade(arcade_cabinet)
        print(f'Star {star} - Final score is {final_score}')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
