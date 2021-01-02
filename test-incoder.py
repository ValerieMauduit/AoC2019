from all_days.intcode import Command, Opcoder, param_value

# For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address 50 + -7 = 43.
def test_param_values():
    opcodes = [12, 2, 42, -7] + [0 for _ in range(50)]
    opcodes[50] = 73
    opcodes[43] = 11
    position_param = param_value(opcodes, 1, 0)
    value_param = param_value(opcodes, 0, 1)
    relative_param = param_value(opcodes, 3, 2, 50)

    if position_param != 42:
        raise Exception(f'Param value {position_param} is not expected value 42')
    if value_param != 12:
        raise Exception(f'Param value {value_param} is not expected value 12')
    if relative_param != 11:
        raise Exception(f'Param value {relative_param} is not expected value 11')
    print('-- test_param_values went ok --')


def test_command(opcodes, input_value, expected, position=0, base=0):
    command = Command(opcodes, position, input_value, base)

    if command.code() != expected['code']:
        raise Exception(f'Command code {command.code()} is not expected value {expected["code"]}')
    if command.type() != expected['type']:
        raise Exception(f'Command type {command.type()} is not expected value {expected["type"]}')
    if command.nb_params() != expected['nb_params']:
        raise Exception(f'Command nb params {command.nb_params()} is not expected value {expected["nb_params"]}')
    if command.params() != expected['params']:
        raise Exception(f'Command params {command.params()} is not expected value {expected["params"]}')
    if command.input_value != expected['input_v']:
        raise Exception(f'Command input value {command.input_value} is not expected value {expected["input_v"]}')
    if command.write_value() != expected['write_v']:
        raise Exception(f'Command write value {command.write_value()} is not expected value {expected["write_v"]}')
    if command.write_position() != expected['write_p']:
        raise Exception(
            f'Command write position {command.write_position()} is not expected value {expected["write_p"]}'
        )
    if command.next_position() != expected['next_p']:
        raise Exception(f'Command next position {command.next_position()} is not expected value {expected["next_p"]}')
    if command.exit() is expected['next_p']:
        raise Exception(f'Command exit {command.exit()} is not expected value {expected["exit"]}')
    if command.output_value() != expected['output_v']:
        raise Exception(f'Command output value {command.output_value()} is not expected value {expected["output_v"]}')
    command.execute_command()
    if command.relative_basis != expected['rel_base']:
        raise Exception(f'Command relative basis {command.relative_basis} is not expected value {expected["rel_base"]}')

    if command.intcodes != expected['opcodes']:
        raise Exception(
            f'Command opcodes after execution {command.intcodes} is not expected value {expected["opcodes"]}'
        )
    return command


def test_command_addition():
    opcodes = [1001, 4, 3, 2, 12]
    expected = {
        'code': '01001', 'type': 1,
        'nb_params': 2, 'params': [12, 3], 'input_v': None, 'opcodes': [1001, 4, 15, 2, 12], 'output_v': None,
        'rel_base': 0,
        'write_v': 15, 'write_p': 2, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_addition went ok --')


def test_command_multiplication():
    opcodes = [1002, 4, 3, 1, 12]
    expected = {
        'code': '01002', 'type': 2,
        'nb_params': 2, 'params': [12, 3], 'input_v': None, 'opcodes': [1002, 36, 3, 1, 12], 'output_v': None,
        'rel_base': 0,
        'write_v': 36, 'write_p': 1, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_multiplication went ok --')


def test_command_take_input():
    opcodes = [1003, 0, 3, 4, 12]
    input_v = 73
    expected = {
        'code': '01003', 'type': 3,
        'nb_params': 0, 'params': [], 'input_v': 73, 'opcodes': [73, 0, 3, 4, 12], 'output_v': None,
        'rel_base': 0,
        'write_v': 73, 'write_p': 0, 'next_p': 2, 'exit': False,
    }
    test_command(opcodes, input_v, expected)
    print('-- test_command_take_input went ok --')


def test_command_provide_output():
    opcodes = [1004, 0, 3, 4, 12]
    expected = {
        'code': '01004', 'type': 4,
        'nb_params': 1, 'params': [1004], 'input_v': None, 'opcodes': opcodes, 'output_v': 1004,
        'rel_base': 0,
        'write_v': None, 'write_p': None, 'next_p': 2, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_provide_output went ok --')


def test_command_jump_if_true():
    opcodes = [5, 0, 3, 4, 12]
    expected = {
        'code': '00005', 'type': 5,
        'nb_params': 2, 'params': [5, 4], 'input_v': None, 'opcodes': opcodes, 'output_v': None,
        'rel_base': 0,
        'write_v': None, 'write_p': None, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_jump_if_true went ok --')


def test_command_jump_if_false():
    opcodes = [6, 0, 3, 4, 12]
    expected = {
        'code': '00006', 'type': 6,
        'nb_params': 2, 'params': [6, 4], 'input_v': None, 'opcodes': opcodes, 'output_v': None,
        'rel_base': 0,
        'write_v': None, 'write_p': None, 'next_p': 3, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_jump_if_false went ok --')


def test_command_less_than():
    opcodes = [7, 0, 3, 5, 12, 42]
    expected = {
        'code': '00007', 'type': 7,
        'nb_params': 2, 'params': [7, 5], 'input_v': None, 'opcodes': [7, 0, 3, 5, 12, 0], 'output_v': None,
        'rel_base': 0,
        'write_v': 0, 'write_p': 5, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_less_than went ok --')


def test_command_equals():
    opcodes = [8, 0, 4, 5, 8, 42]
    expected = {
        'code': '00008', 'type': 8,
        'nb_params': 2, 'params': [8, 8], 'input_v': None, 'opcodes': [8, 0, 4, 5, 8, 1], 'output_v': None,
        'rel_base': 0,
        'write_v': 1, 'write_p': 5, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_equals went ok --')

# For example, if the relative base is 2000, then after the instruction 109,19, the relative base would be 2019. If
# the next instruction were 204,-34, then the value at address 1985 would be output.
def test_command_offset():
    opcodes = [109, 19, 204, -34] + [0 for _ in range(2000)]
    opcodes[1985] = 42
    base = 2000

    expected1 = {
        'code': '00109', 'type': 9,
        'nb_params': 1, 'params': [19], 'input_v': None, 'opcodes': opcodes, 'output_v': None,
        'rel_base': 2019,
        'write_v': None, 'write_p': None, 'next_p': 2, 'exit': False,
    }
    expected2 = {
        'code': '00204', 'type': 4,
        'nb_params': 1, 'params': [42], 'input_v': None, 'opcodes': opcodes, 'output_v': 42,
        'rel_base': 2019,
        'write_v': None, 'write_p': None, 'next_p': 4, 'exit': False,
    }
    first_command = test_command(opcodes, None, expected1, position=0, base=base)
    test_command(opcodes, None, expected2, first_command.next_position(), first_command.relative_basis)

    print('-- test_command_offset went ok --')


def test_command_exit():
    opcodes = [99, 0, 4, 5, 8, 42]
    expected = {
        'code': '00099', 'type': 99,
        'nb_params': 0, 'params': [], 'input_v': None, 'opcodes': opcodes, 'output_v': None, 'rel_base': 0,
        'write_v': None, 'write_p': None, 'next_p': None, 'exit': True,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_exit went ok --')


def day09_examples():
    # This opcoder should take no input and produce a copy of itself as output.
    opcodes = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    opcoder1 = Opcoder(opcodes)
    opcoder1.run_until_exit()
    if opcoder1.output_values != opcodes:
        raise Exception('Output values should be exactly the input opcodes list')

    # This opcoder should output a 16-digit number.
    opcodes = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    opcoder2 =Opcoder(opcodes)
    opcoder2.run_until_exit()
    if len(opcoder2.output_values) != 1:
        raise Exception('Output values should be a list of 1 digit exactly')
    if len(str(opcoder2.output_values[0])) != 16:
        raise Exception('Output value should be a 16-digit number')

    # This opcoder should output the large number in the middle.
    opcodes = [104, 1125899906842624, 99]
    opcoder3 = Opcoder(opcodes)
    opcoder3.run_until_exit()
    if len(opcoder3.output_values) != 1:
        raise Exception('Output values should be a list of 1 digit exactly')
    if opcoder3.output_values[0] != opcodes[1]:
        raise Exception(f'Output value should be the value {opcodes[1]}')
    print('--- Day 9 examples went ok ---')


def main():
    test_param_values()
    test_command_addition()
    test_command_multiplication()
    test_command_take_input()
    test_command_provide_output()
    test_command_jump_if_true()
    test_command_jump_if_false()
    test_command_less_than()
    test_command_equals()
    test_command_offset()
    test_command_exit()
    day09_examples()


if __name__ == "__main__":
    main()