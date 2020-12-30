# --- Day 7: Amplification Circuit ---

# First star:
# There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They
# are connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's
# output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last
# amplifier's output leads to your ship's thrusters.
# The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that should run on your
# existing Intcode computer. Each amplifier will need to run a copy of the program.
# When a copy of the program starts running on an amplifier, it will first use an input instruction to ask the amplifier
# for its current phase setting (an integer from 0 to 4). Each phase setting is used exactly once, but the Elves can't
# remember which amplifier needs which phase setting.
# The program will then call another input instruction to get the amplifier's input signal, compute the correct output
# signal, and supply it back to the amplifier with an output instruction. (If the amplifier has not yet received an
# input signal, it waits until one arrives.)
# Your job is to find the largest output signal that can be sent to the thrusters by trying every possible combination
# of phase settings on the amplifiers. Make sure that memory is not shared or reused between copies of the program.

# Second star:

from copy import deepcopy
from all_days.intcode import run_intcoder


def run(data_dir, star):
    with open(f'{data_dir}/input-day07.txt', 'r') as fic:
        opcodes = [int(x) for x in fic.read().split(',')]

    if star == 1:
        opcodesA = deepcopy(opcodes)
        opcodesB = deepcopy(opcodes)
        opcodesC = deepcopy(opcodes)
        opcodesD = deepcopy(opcodes)
        opcodesE = deepcopy(opcodes)

        max_thruster = 0
        for A0 in range(5):
            settingsB = [n for n in range(5) if n != A0]
            outputA = run_intcoder(opcodesA, [A0, 0])
            for B0 in settingsB:
                settingsC = [n for n in settingsB if n != B0]
                outputB = run_intcoder(opcodesB, [B0, outputA])
                for C0 in settingsC:
                    settingsD = [n for n in settingsC if n != C0]
                    outputC = run_intcoder(opcodesC, [C0, outputB])
                    for D0 in settingsD:
                        E0 = [n for n in settingsD if n != D0][0]
                        outputD = run_intcoder(opcodesD, [D0, outputC])
                        thruster = run_intcoder(opcodesE, [E0, outputD])
                        max_thruster = max(max_thruster, thruster)
        print(f'Star {star} - The largest output signal is {max_thruster}')
        return max_thruster

    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
