from copy import deepcopy

def param_value(opcodes, param, mode):
    if mode == 0:    # position mode
        if param < len(opcodes):
            return opcodes[param]
    elif mode == 1:  # immediate mode
        return param
    else:
        raise ValueError(f'Mode {mode} not accepted')


class Command():
    def __init__(self, intcodes, position, input_value=None):
        self.intcodes = intcodes
        self.input_value = input_value
        self.position = position

    def type(self):
        command_type = self.intcodes[self.position] % 100
        if command_type not in [1, 2, 3, 4, 5, 6, 7, 8, 99]:
            raise ValueError(f'Opcode digit command {command_type} does not exist.')
        return command_type

    def exit(self):
        return self.type() == 99

    def code(self):
        return f'{self.intcodes[self.position]:05.0f}'

    def nb_params(self):
        if self.type() in [3, 4, 99]:
            return 0
        elif self.type() in [1, 2, 5, 6, 7, 8]:
            return 2

    def params(self):
        return [
            param_value(self.intcodes, self.position + rank, int(self.code()[-2 - rank]))
            for rank in range(self.nb_params())
        ]

    def next_position(self):
        if self.type() in [1, 2, 7, 8]:
            return self.position + 4
        elif self.type() in [3, 4]:
            return self.position + 2
        elif self.type() == 5:  # Jump if True
            if self.param()[0] != 0:
                return self.param()[1]
            else:
                return self.position + 3
        elif self.type() == 6:  # Jump if False
            if self.param()[0] == 0:
                return self.param()[1]
            else:
                return self.position + 3
        elif self.type() == 99:
            return self.position

    def write_position(self):
        if self.type() in [4, 99]:
            return None
        return self.intcodes[self.position + self.nb_params() + 1]

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
        if self.write_position() is not None:
            self.intcodes[self.write_position()] = self.write_value()

    def print(self, pointer=False):
        types_dict = {
            1: 'Addition', 2: 'Multiplication',
            3: 'Take input', 4: 'Provides output',
            5: 'Jump if True', 6: 'Jump if False',
            7: 'Less than', 8: 'Equals',
            99: 'Exit'
        }
        next = self.next_position()
        if self.next_position() == self.position:
            next = self.position +1
        sequence = ', '.join([str(n) for n in self.intcodes[self.position:next]])
        if pointer:
            sequence += '    *******'
        print(f'({self.position:5.0f}) {types_dict[self.type()]:<16} | ' + sequence)


class Opcoder():
    def __init__(self, intcodes):
        self.intcodes = deepcopy(intcodes)
        self.input_values = None
        self.output_value = None
        self.pointer = 0
        self.exit = False

    def inputs(self, inputs):
        self.input_values = inputs

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
            pos = command.next_position()
            if command.exit():
                pos = len(self.intcodes) + 1
        print('  ')
        return None

    def run_step(self):
        input_value = None
        if type(self.input_values) == list:
            input_value = self.input_values[0]
            self.input_values = self.input_values[1:]
            if len(self.input_values) == 0:
                self.input_values = None
        elif type(self.input_values) == int:
            input_value = self.input_values
            self.input_values = None

        command = Command(self.intcodes, self.pointer, input_value)
        self.output_value = command.output_value()
        self.exit = command.exit()
        command.execute_command()
        self.intcodes = command.intcodes
        self.pointer = command.next_position()


    def run_until_exit(self):
        while not self.exit:
            self.run_step()

    def run_until_no_input(self):
        while (not self.exit) and (self.input_values is not None):
            self.run_step()

    def run_until_next_output(self):
        while (not self.exit) and (self.output_value is None):
            self.run_step()
