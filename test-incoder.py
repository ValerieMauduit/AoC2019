from all_days.intcode import Command, param_value


def test_param_values():
    opcodes = [12, 2, 42]
    position_param = param_value(opcodes, 1, 0)
    value_param = param_value(opcodes, 0, 1)
    if position_param != 42:
        raise Exception(f'Param value {position_param} is not expected value 42')
    if value_param != 12:
        raise Exception(f'Param value {value_param} is not expected value 12')
    print('-- test_param_values went ok --')


def test_command(opcodes, input_value, expected):
    command = Command(opcodes, 0, input_value)

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
    if command.intcodes != expected['opcodes']:
        raise Exception(
            f'Command opcodes after execution {command.intcodes} is not expected value {expected["opcodes"]}'
        )


def test_command_addition():
    print('Testing Addition command')
    opcodes = [1001, 4, 3, 2, 12]
    expected = {
        'code': '01001', 'type': 1,
        'nb_params': 2, 'params': [12, 3], 'input_v': None, 'opcodes': [1001, 4, 15, 2, 12], 'output_v': None,
        'write_v': 15, 'write_p': 2, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_addition went ok --')


def test_command_multiplication():
    print('Testing Multiplication command')
    opcodes = [1002, 4, 3, 1, 12]
    expected = {
        'code': '01002', 'type': 2,
        'nb_params': 2, 'params': [12, 3], 'input_v': None, 'opcodes': [1002, 36, 3, 1, 12], 'output_v': None,
        'write_v': 36, 'write_p': 1, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_multiplication went ok --')


def test_command_take_input():
    print('Testing Take Input command')
    opcodes = [1003, 0, 3, 4, 12]
    input_v = 73
    expected = {
        'code': '01003', 'type': 3,
        'nb_params': 0, 'params': [], 'input_v': 73, 'opcodes': [73, 0, 3, 4, 12], 'output_v': None,
        'write_v': 73, 'write_p': 0, 'next_p': 2, 'exit': False,
    }
    test_command(opcodes, input_v, expected)
    print('-- test_command_take_input went ok --')


def test_command_provide_output():
    print('Testing Provide Output command')
    opcodes = [1004, 0, 3, 4, 12]
    expected = {
        'code': '01004', 'type': 4,
        'nb_params': 1, 'params': [1004], 'input_v': None, 'opcodes': opcodes, 'output_v': 1004,
        'write_v': None, 'write_p': None, 'next_p': 2, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_provide_output went ok --')


def test_command_jump_if_true():
    print('Testing Jump If True command')
    opcodes = [5, 0, 3, 4, 12]
    expected = {
        'code': '00005', 'type': 5,
        'nb_params': 2, 'params': [5, 4], 'input_v': None, 'opcodes': opcodes, 'output_v': None,
        'write_v': None, 'write_p': None, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_jump_if_true went ok --')


def test_command_jump_if_false():
    print('Testing Jump If False command')
    opcodes = [6, 0, 3, 4, 12]
    expected = {
        'code': '00006', 'type': 6,
        'nb_params': 2, 'params': [6, 4], 'input_v': None, 'opcodes': opcodes, 'output_v': None,
        'write_v': None, 'write_p': None, 'next_p': 3, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_jump_if_false went ok --')


def test_command_less_than():
    print('Testing Less Than command')
    opcodes = [7, 0, 3, 5, 12, 42]
    expected = {
        'code': '00007', 'type': 7,
        'nb_params': 2, 'params': [7, 5], 'input_v': None, 'opcodes': [7, 0, 3, 5, 12, 0], 'output_v': None,
        'write_v': 0, 'write_p': 5, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_less_than went ok --')


def test_command_equals():
    print('Testing Equals command')
    opcodes = [8, 0, 4, 5, 8, 42]
    expected = {
        'code': '00008', 'type': 8,
        'nb_params': 2, 'params': [8, 8], 'input_v': None, 'opcodes': [8, 0, 4, 5, 8, 1], 'output_v': None,
        'write_v': 1, 'write_p': 5, 'next_p': 4, 'exit': False,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_equals went ok --')


def test_command_exit():
    print('Testing Exit command')
    opcodes = [99, 0, 4, 5, 8, 42]
    expected = {
        'code': '00099', 'type': 99,
        'nb_params': 0, 'params': [], 'input_v': None, 'opcodes': opcodes, 'output_v': None,
        'write_v': None, 'write_p': None, 'next_p': None, 'exit': True,
    }
    test_command(opcodes, None, expected)
    print('-- test_command_equals went ok --')


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
    test_command_exit()


if __name__ == "__main__":
    main()