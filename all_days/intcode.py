def param_value(opcodes, param, mode):
    if mode == 0:    # position mode
        if param < len(opcodes):
            return opcodes[param]
    elif mode == 1:  # immediate mode
        return param
    else:
        raise ValueError(f'Mode {mode} not accepted')


class Opcoder():
    def __init__(self, intcodes):
        self.intcodes = intcodes
        self.input_values = None
        self.output_value = None
        self._pointer = 0
        self._exit = False

    def inputs(self, inputs):
        self.input_values = inputs

    def param(self, rank):
        code = f'{self.intcodes[self._pointer]:05.0f}'
        return param_value(self.intcodes, self.intcodes[self._pointer + rank], int(code[- 2 - rank]))

    def print(self):
        print([f'({self.intcodes[n]})' if n == self._pointer else self.intcodes[n] for n in range(len(self.intcodes))])
        return None

    def run_step(self):
        command_code = self.intcodes[self._pointer] % 100
        if command_code == 1:     # Addition
            self.intcodes[self.intcodes[self._pointer + 3]] = self.param(1) + self.param(2)
            self._pointer += 4
        elif command_code == 2:   # Multiplication
            self.intcodes[self.intcodes[self._pointer + 3]] = self.param(1) * self.param(2)
            self._pointer += 4
        elif command_code == 3:   # Take input
            if type(self.input_values) == list:
                input_value = self.input_values[0]
                self.input_values = self.input_values[1:]
                if len(self.input_values) == 0:
                    self.input_values = None
            elif type(self.input_values) == int:
                input_value = self.input_values
                self.input_values = None
            else:
                raise Exception('No input value provided - at least one is needed')
            self.intcodes[self.intcodes[self._pointer + 1]] = input_value # TODO: à revoir
            self._pointer += 2
        elif command_code == 4:   # Provide output
            self.output_value = self.param(1)
            self._pointer += 2
        elif command_code == 5:   # Jump if true
            if self.param(1) != 0:
                self._pointer = self.param(2)
            else:
                self._pointer += 3
        elif command_code == 6:   # Jump if false
            if self.param(1) == 0:
                self._pointer = self.param(2)
            else:
                self._pointer += 3
        elif command_code == 7:   # Less than
            self.intcodes[self.intcodes[self._pointer + 3]] = (self.param(1) < self.param(2)) * 1
            self._pointer += 4
        elif command_code == 8:   # Equals
            self.intcodes[self.intcodes[self._pointer + 3]] = (self.param(1) == self.param(2)) * 1
            self._pointer += 4
        elif command_code == 99:  # Exit the program
            self._pointer = len(self.intcodes) + 1
            self._exit = True
        else:
            raise ValueError(f'Opcode digit command {command_code} does not exist.')

    def run_until_exit(self):
        while not self._exit:
            self.run_step()