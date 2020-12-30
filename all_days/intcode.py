def param_value(opcodes, param, mode):
    if mode == 0:    # position mode
        if param < len(opcodes):
            return opcodes[param]
    elif mode == 1:  # immediate mode
        return param
    else:
        raise ValueError(f'Mode {mode} not accepted')


def run_intcoder(opcodes, inputs=[]):
    pointer = 0
    output_value = None
    param1, param2 = 0, 0
    n = 0
    while pointer <= len(opcodes):
        code = f'{opcodes[pointer]:05.0f}'
        command = int(code[-2:])
        if pointer < (len(opcodes) - 1): # Set parameters in case of needed for the instruction
            param1 = param_value(opcodes, opcodes[pointer + 1], int(code[-3]))
            if pointer < (len(opcodes) - 2):
                param2 = param_value(opcodes, opcodes[pointer + 2], int(code[-4]))
        if command == 1:           # Addition
            opcodes[opcodes[pointer + 3]] = param1 + param2
            pointer += 4
        elif command == 2:         # Multiplication
            opcodes[opcodes[pointer + 3]] = param1 * param2
            pointer += 4
        elif command == 3:         # Take input
            if len(inputs) < (n + 1):
                inputs += [int(input('What is the entry?  '))]
            opcodes[opcodes[pointer + 1]] = inputs[n]
            n += 1
            pointer += 2
        elif command == 4:         # Provide output
            output_value = param1
            pointer += 2
        elif command == 5:         # Jump if true
            if param1 != 0:
                pointer = param2
            else:
                pointer += 3
        elif command == 6:         # Jump if false
            if param1 == 0:
                pointer = param2
            else:
                pointer += 3
        elif command == 7:         # Less than
            opcodes[opcodes[pointer + 3]] = (param1 < param2) * 1
            pointer += 4
        elif command == 8:         # Equals
            opcodes[opcodes[pointer + 3]] = (param1 == param2) * 1
            pointer += 4
        elif command == 99:        # Exit the program
            pointer = len(opcodes) + 1
        else:                      # Error
            raise ValueError(f'Opcode digit {command} does not exist.')

    return {'opcodes': opcodes, 'output': output_value}
