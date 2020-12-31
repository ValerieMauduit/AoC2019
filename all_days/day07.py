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
# 95757

# Second star:
# The Elves quickly talk you through rewiring the amplifiers into a feedback loop.
# Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input,
# and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback
# loop: the signal will be sent through the amplifiers many times.
# In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used
# exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce output
# many times before halting. Provide each amplifier its phase setting at its first input instruction; all further
# input/output instructions are for signals.
# Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue
# receiving and sending signals until it halts.
# All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the
# very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.
# Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens, the
# last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal that can
# be sent to the thrusters using the new phase settings and feedback loop arrangement.

# Here are some example programs:
#
# Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
#
# 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

# Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
#
# 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
# -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
# 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10

# Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be
# sent to the thrusters?

from copy import deepcopy
from all_days.intcode import Opcoder
from itertools import permutations


def run(data_dir, star):
    with open(f'{data_dir}/input-day07.txt', 'r') as fic:
        opcodes = [int(x) for x in fic.read().split(',')]

    if star == 1:    # Answer is 95757
        max_thruster = 0
        for permutation in permutations(range(5)):
            amplifiers = [Opcoder(opcodes) for n in range(5)]
            input_from_previous = 0
            for amplifier, init_value in zip(amplifiers, permutation):
                amplifier.inputs([init_value, input_from_previous])
                amplifier.run_until_exit()
                input_from_previous = amplifier.output_value
            max_thruster = max(max_thruster, input_from_previous)

        print(f'Star {star} - The largest output signal is {max_thruster}')
        return max_thruster
#
    elif star == 2:
        phase_settings = permutations(range(5, 10))
        max_thruster = 0
        for phase_setting in phase_settings:
            print(f'=== Phase setting {phase_setting} ===')
            # Initialize each amplifier
            amplifiers = [Opcoder(opcodes) for n in range(5)]
            for amplifier, init_value in zip(amplifiers, phase_setting):
                amplifier.inputs(init_value)
                amplifier.run_until_next_input()
            # Then run the loop until an exit
            input_from_previous = 0
            exit_loop = False
            nloop = 0
            while not exit_loop:
                nloop += 1
                print(f'Loop {nloop}')
                for amplifier in amplifiers:
                    print(amplifier)
                    amplifier.inputs(input_from_previous)
                    amplifier.run_until_next_input()
                    input_from_previous = amplifier.output_value
                    print(amplifier.output_value)
                exit_loop = amplifiers[4]._exit
            max_thruster = max(max_thruster, input_from_previous)

        print(f'Star {star} - The largest output signal is {max_thruster}')
        return max_thruster
    else:
        raise Exception('Star number must be either 1 or 2.')
