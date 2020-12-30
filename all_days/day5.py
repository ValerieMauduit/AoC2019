# --- Day 5: Sunny with a Chance of Asteroids ---

# First star:
# The Thermal Environment Supervision Terminal (TEST) starts by running a diagnostic program (your puzzle input). The
# TEST diagnostic program will run on your existing Intcode computer after a few modifications:
# - First, you'll need to add two new instructions:
#    - Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example,
#      the instruction 3,50 would take an input value and store it at address 50.
#    - Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at
#      address 50.
# Programs that use these instructions will come with documentation that explains what should be connected to the input
# and output. The program 3,0,4,0,99 outputs whatever it gets as input, then halts.
# - Second, you'll need to add support for parameter modes:
#   - Each parameter of an instruction is handled based on its parameter mode.
#   - Right now, your ship computer already understands parameter mode 0, position mode, which causes the parameter to
#     be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory.
#     Until now, all parameters have been in position mode.
#   - Now, your ship computer will also need to handle parameters in mode 1, immediate mode. In immediate mode, a
#   parameter is interpreted as a value - if the parameter is 50, its value is simply 50.
# Parameter modes are stored in the same value as the instruction's opcode. The opcode is a two-digit number based only
# on the ones and tens digit of the value, that is, the opcode is the rightmost two digits of the first value in an
# instruction. Parameter modes are single digits, one per parameter, read right-to-left from the opcode: the first
# parameter's mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third
# parameter's mode is in the ten-thousands digit, and so on. Any missing modes are 0.
# Parameters that an instruction writes to will never be in immediate mode.
# Finally, some notes:
# - It is important to remember that the instruction pointer should increase by the number of values in the instruction
#   after the instruction finishes. Because of the new instructions, this amount is no longer always 4.
# - Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1, store the result in position 4).
# - The TEST diagnostic program will start by requesting from the user the ID of the system to test by running an input
#   instruction - provide it 1, the ID for the ship's air conditioner unit.
# It will then perform a series of diagnostic tests confirming that various parts of the Intcode computer, like
# parameter modes, function correctly. For each test, it will run an output instruction indicating how far the result of
# the test was from the expected value, where 0 means the test was successful. Non-zero outputs mean that a function is
# not working correctly; check the instructions that were run before the output instruction to see which one failed.
# Finally, the program will output a diagnostic code and immediately halt. This final output isn't an error; an output
# followed immediately by a halt means the program finished. If all outputs were zero except the diagnostic code, the
# diagnostic program ran successfully.
# After providing 1 to the only input instruction and passing all the tests, what diagnostic code does the program
# produce?

# Second star:
# Your computer is only missing a few opcodes:
# - Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the
#   second parameter. Otherwise, it does nothing.
# - Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the
#   second parameter. Otherwise, it does nothing.
# - Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given
#   by the third parameter. Otherwise, it stores 0.
# - Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by
#   the third parameter. Otherwise, it stores 0.
# Like all instructions, these instructions need to support parameter modes as described above.
# Normally, after an instruction is finished, the instruction pointer increases by the number of values in that
# instruction. However, if the instruction modifies the instruction pointer, that value is used and the instruction
# pointer is not automatically increased.
# This time, when the TEST diagnostic program runs its input instruction to get the ID of the system to test, provide it
# 5, the ID for the ship's thermal radiator controller. This diagnostic test suite only outputs one number, the
# diagnostic code.
# What is the diagnostic code for system ID 5?

from all_days.intcode import run_intcoder


def run(data_dir, star):
    if star in [1, 2]:
        with open(f'{data_dir}/input-day05.txt', 'r') as fic:
            opcodes = [int(x) for x in fic.read().split(',')]
        diagnostic_code = run_intcoder(opcodes)
        print(f'Star {star} - Your diagnostic code is {diagnostic_code}')
        return diagnostic_code
    else:
        raise Exception('Star number must be either 1 or 2.')
