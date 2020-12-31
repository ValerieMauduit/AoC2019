# --- Day 2: 1202 Program Alarm ---

# First star:
# An Intcode program is a list of integers separated by commas (like 1,0,0,3,99). To run one, start by looking at the
# first integer (called position 0). Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to
# do.
# - 99 means that the program is finished and should immediately halt. Encountering an unknown opcode means something
# went wrong.
# - Opcode 1 adds together numbers read from two positions and stores the result in a third position. The three integers
# immediately after the opcode tell you these three positions - the first two indicate the positions from which you
# should read the input values, and the third indicates the position at which the output should be stored.
# - Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the three
# integers after the opcode indicate where the inputs and outputs are, not their values.
# - Once you're done processing an opcode, move to the next one by stepping forward 4 positions.
# Once you have a working computer, the first step is to restore the gravity assist program (your puzzle input) to the
# "1202 program alarm" state it had just before the last computer caught fire. To do this, before running the program,
# replace position 1 with the value 12 and replace position 2 with the value 2. What value is left at position 0 after
# the program halts?

# Second star:
# Intcode programs are given as a list of integers; these values are used as the initial state for the computer's
# memory. When you run an Intcode program, make sure to start by initializing memory to the program's values. A position
# in memory is called an address (for example, the first value in memory is at "address 0").
# Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values used immediately after an opcode, if any,
# are called the instruction's parameters. For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3, and 4 are the
# parameters. The instruction 99 contains only an opcode and has no parameters.
# The address of the current instruction is called the instruction pointer; it starts at 0. After an instruction
# finishes, the instruction pointer increases by the number of values in the instruction; until you add more
# instructions to the computer, this is always 4 (1 opcode + 3 parameters) for the add and multiply instructions. (The
# halt instruction would increase the instruction pointer by 1, but it halts the program instead.)
# "With terminology out of the way, we're ready to proceed. To complete the gravity assist, you need to determine what
# pair of inputs produces the output 19690720."
# The inputs should still be provided to the program by replacing the values at addresses 1 and 2, just like before.
# In this program, the value placed in address 1 is called the noun, and the value placed in address 2 is called the
# verb. Each of the two input values will be between 0 and 99, inclusive.
# Once the program has halted, its output is available at address 0, also just like before. Each time you try a pair of
# inputs, make sure you first reset the computer's memory to the values in the program (your puzzle input) - in other
# words, don't reuse memory from a previous attempt.
# Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb?

from all_days.intcode import Opcoder


def run(data_dir, star):
    with open(f'{data_dir}/input-day02.txt', 'r') as fic:
        opcodes = [int(x) for x in fic.read().split(',')]

    if star == 1:    # Answer is 3409710
        opcodes[1] = 12
        opcodes[2] = 2
        computer = Opcoder(opcodes)
        computer.run_until_exit()
        result = computer.intcodes[0]

        print(f'Star {star} - Value at position 0 is now {result}')
        return result

    elif star == 2:  # Alswer is 7912
        noun = 0
        solution = None
        while noun < 100:
            verb = 0
            while verb < 100:
                opcode_test = opcodes.copy()
                opcode_test[1] = noun
                opcode_test[2] = verb
                computer = Opcoder(opcode_test)
                computer.run_until_exit()
                if computer.intcodes[0] == 19690720:
                    solution = (noun, verb, noun * 100 + verb)
                    noun, verb = 100, 100
                verb += 1
            noun += 1
        print(f'Star {star} - Noun + verb producing 19690720 is {solution[2]}')
        return solution

    else:
        raise Exception('Star number must be either 1 or 2.')
