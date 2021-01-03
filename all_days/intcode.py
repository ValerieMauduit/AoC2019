from copy import deepcopy


def param_value(opcodes, position, mode, base=0):
    if mode == 1:         # immediate mode
        return opcodes[position]
    elif mode in [0, 2]:  # position modes
        new_position = param_position(opcodes, position, mode, base)
        if new_position < len(opcodes):
            return opcodes[new_position]
        else:
            return 0
    else:
        raise ValueError(f'Mode {mode} not accepted')


def param_position(opcodes, position, mode, base=0):
    if mode == 0:    # position mode
        return opcodes[position]
    elif mode == 2:  # relative mode
        return opcodes[position] + base


# Command types summary:
# 1 - addition - takes 3 parameters: param1 + param2 stored in param3
# 2 - multiplication mode - takes 3 parameters: param1 * param2 stored in param3
# 3 - take input - takes 1 parameter: stores input in param1
# 4 - provide output - takes 1 parameter: takes param1 and put value in output
# 5 - jump if true - takes 2 parameters: if param1 != 0, go to param2
# 6 - jump if false - takes 2 parameters: if param1 == 0, go to param2
# 7 - less than - takes 3 parameters: if param1 < param2, param3 stores 1, else param3 stores 0
# 8 - equals - takes 3 parameters: if param1 == param2, param3 stores 1, else param3 stores 0
# 9 - offset - takes 1 parameter: relative basis incremented by param1
# 99 - exit - no parameter
class Command():
    def __init__(self, intcodes, position, input_value=None, relative_basis=0):
        self.intcodes = intcodes
        self.input_value = input_value
        self.position = position
        self.relative_basis = relative_basis

    def type(self, debug=True):
        command_type = self.intcodes[self.position] % 100
        if debug and (command_type not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]):
            raise ValueError(f'Opcode digit command {command_type} does not exist.')
        return command_type

    def exit(self):
        return self.type() == 99

    def code(self):
        return f'{self.intcodes[self.position]:05.0f}'

    def nb_params(self):
        if self.type() in [99]:
            return 0
        elif self.type() in [3, 4, 9]:
            return 1
        elif self.type() in [5, 6]:
            return 2
        elif self.type() in [1, 2, 7, 8]:
            return 3

    def params(self):
        return [
            param_value(self.intcodes, self.position + rank + 1, int(self.code()[-3 - rank]), self.relative_basis)
            for rank in range(self.nb_params())
        ]

    def next_position(self):
        if self.type() in [1, 2, 3, 4, 7, 8, 9]:  # Commands with parameters
            return self.position + self.nb_params() + 1
        elif self.type() == 5:                    # Jump if True
            if self.params()[0] != 0:
                return self.params()[1]
            else:
                return self.position + 3
        elif self.type() == 6:                    # Jump if False
            if self.params()[0] == 0:
                return self.params()[1]
            else:
                return self.position + 3
        elif self.type() == 99:                   # Exit
            return None

    def write_position(self):
        if self.type() in [4, 5, 6, 9, 99]:
            return None
        elif self.type() in [1, 2, 7, 8]:
            rank = 3
        else:
            rank = 1
        return param_position(self.intcodes, self.position + rank, int(self.code()[-2 - rank]), self.relative_basis)

    def write_value(self):
        if self.type() == 1:    # Addition
            return self.params()[0] + self.params()[1]
        elif self.type() == 2:  # Multiplication
            return self.params()[0] * self.params()[1]
        elif self.type() == 3:  # Take input
            if self.input_value is None:
                raise Exception('No input value provided - at least one is needed')
            return self.input_value
        elif self.type() == 7:  # Less than
            return (self.params()[0] < self.params()[1]) * 1
        elif self.type() == 8:  # Equals
            return (self.params()[0] == self.params()[1]) * 1
        else:
            return None

    def output_value(self):
        if self.type() == 4:
            return self.params()[0]
        return None

    def execute_command(self):
        if self.write_position() is not None:   # Write in memory commands
            if self.write_position() >= len(self.intcodes):
                temp = [0 for _ in range(self.write_position() + 1)]
                temp[:len(self.intcodes)] = self.intcodes
                self.intcodes = deepcopy(temp)
            self.intcodes[self.write_position()] = self.write_value()
        elif self.type() == 9:                   # Update relative basis command
            self.relative_basis += self.params()[0]

    def print(self, pointer=False):
        types_dict = {
            1: 'Addition', 2: 'Multiplication', 3: 'Take input', 4: 'Provides output',
            5: 'Jump if True', 6: 'Jump if False', 7: 'Less than', 8: 'Equals', 9: 'Offset',
            99: 'Exit'
        }
        if self.type(debug=False) in types_dict.keys():
            right_position = self.position + self.nb_params() + 1
            if self.type() in [1, 2, 3, 7, 8]: # Need extra parameter
                right_position += 1
            sequence = ', '.join([str(n) for n in self.intcodes[self.position:right_position]])
            if pointer:
                sequence += '    *******'
            print(f'({self.position:5.0f}) {types_dict[self.type()]:<20} | ' + sequence)
        else:
            sequence = ', '.join([str(n) for n in self.intcodes[self.position:]])
            print(f'({self.position:5.0f}) UNKNOWN COMMAND TYPE | ' + sequence)


class Opcoder():
    def __init__(self, intcodes):
        self.intcodes = deepcopy(intcodes)
        self.input_values = None
        self.output_values = []
        self.pointer = 0
        self.exit = False
        self.relative_basis = 0

    def inputs(self, inputs):
        self.input_values = inputs
        return None

    def set_pointer(self, position):
        self.pointer = position
        self.exit = False
        return None

    def initialize_outputs(self):
        self.output_values = []
        return None

    def print(self):
        print([f'({self.intcodes[n]})' if n == self.pointer else self.intcodes[n] for n in range(len(self.intcodes))])
        return None

    def pretty_print(self):
        pos = 0
        while pos < len(self.intcodes):
            command = Command(self.intcodes, pos)
            print_pointer = False
            if pos == self.pointer:
                print_pointer = True
            command.print(print_pointer)
            if command.type(debug=False) in [5, 6, 99]:               # Jump/Exit commands
                pos += command.nb_params() + 1
            elif command.type(debug=False) in [1, 2, 3, 4, 7, 8, 9]:  # Normal reading commands
                pos = command.next_position()
            else:
                pos = len(self.intcodes) + 1                          # End of opcodes list
        print('  ')
        return None

    def run_step(self):
        input_value = None
        if type(self.input_values) == list:
            input_value = self.input_values[0]
        elif type(self.input_values) == int:
            input_value = self.input_values

        command = Command(self.intcodes, self.pointer, input_value, self.relative_basis)
        command.execute_command()

        if command.output_value() is not None:
            self.output_values += [command.output_value()]
        self.exit = command.exit()
        self.intcodes = command.intcodes
        self.pointer = command.next_position()
        self.relative_basis = command.relative_basis
        if command.type() == 3:
            if type(self.input_values) == list:
                self.input_values = self.input_values[1:]
                if len(self.input_values) == 0:
                    self.input_values = None
            elif type(self.input_values) == int:
                self.input_values = None

    def run_until_exit(self):
        while not self.exit:
            self.run_step()

    def run_until_no_input(self):
        while (not self.exit) and (self.input_values is not None):
            self.run_step()

    def run_until_next_output(self):
        nb_outputs = len(self.output_values)
        while (not self.exit) and (len(self.output_values) == nb_outputs):
            self.run_step()
