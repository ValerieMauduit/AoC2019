# --- Day 9: Sensor Boost ---

# First star:
# Your existing Intcode computer is missing one key feature: it needs support for parameters in relative mode.
# Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: the parameter is
# interpreted as a position. Like position mode, parameters in relative mode can be read from or written to.
# The important difference is that relative mode parameters don't count from address 0. Instead, they count from a value
# called the relative base. The relative base starts at 0.
# The address a relative mode parameter refers to is itself plus the current relative base. When the relative base is 0,
# relative mode parameters and position mode parameters with the same value refer to the same address.
# The relative base is modified with the relative base offset instruction:
# Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if
# the value is negative) by the value of the parameter.
# Your Intcode computer will also need a few other capabilities:
# The computer's available memory should be much larger than the initial program. Memory beyond the initial program
# starts with the value 0 and can be read or written like any other memory. (It is invalid to try to access memory at a
# negative address, though.)
# The computer should have support for large numbers. Some instructions near the beginning of the BOOST program will
# verify this capability.
# The BOOST program will ask for a single input; run it in test mode by providing it the value 1. It will perform a
# series of checks on each opcode, output any opcodes (and the associated parameter modes) that seem to be functioning
# incorrectly, and finally output a BOOST keycode.
# Once your Intcode computer is fully functional, the BOOST program should report no malfunctioning opcodes when run in
# test mode; it should only output a single value, the BOOST keycode. What BOOST keycode does it produce?

# Second star:
# You now have a complete Intcode computer.
# The program runs in sensor boost mode by providing the input instruction the value 2. Once run, it will boost the
# sensors automatically, but it might take a few seconds to complete the operation on slower hardware. In sensor boost
# mode, the program will output a single value: the coordinates of the distress signal.
# Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?

from all_days.intcode import Opcoder

def run(data_dir, star):
    with open(f'{data_dir}/input-day09.txt', 'r') as fic:
        opcodes = [int(x) for x in fic.read().split(',')]
    boost = Opcoder(opcodes)

    if star == 1:
        boost.inputs([1])
        signification = 'BOOST keycode'
    elif star == 2:
        boost.inputs(2)
        signification = 'coordinates of the distress signal'
    else:
        raise Exception('Star number must be either 1 or 2.')

    boost.run_until_exit()
    print(f'Star {star} - the {signification} is {boost.output_values[0]}')
    return boost.output_values[0]

