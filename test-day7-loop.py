# Here are some example programs:
#
# Max thruster signal 139629729 (from phase setting sequence 9, 8, 7, 6, 5):
# 3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
# 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5
#
# Max thruster signal 18216 (from phase setting sequence 9, 7, 8, 5, 6):
# 3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
# -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
# 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10

from itertools import permutations
from all_days.intcode import Opcoder


def test_day7_star2_example1(opcodes, expected_phase_setting, expected_max_thruster):
    max_thruster, best_phase_setting = 0, None
    for phase_setting in permutations(range(5, 10)):
        # Initialize each amplifier
        amplifiers = [Opcoder(opcodes) for _ in range(5)]
        for amplifier, init_value in zip(amplifiers, phase_setting):
            amplifier.inputs(init_value)
            amplifier.run_until_no_input()

        # Then run the loop until an exit
        input_from_previous = 0
        exit_loop = False
        end_value = 0
        while not exit_loop:
            for amplifier in amplifiers:
                amplifier.inputs(input_from_previous)
                amplifier.run_until_next_output()
                input_from_previous = amplifier.output_value
            amplifiers[4].run_until_no_input()
            if amplifiers[4].output_value is not None:
                end_value = amplifiers[4].output_value
            # Then test if amplifiers[4] can continue to exit
            exit_loop = amplifiers[4].exit

        if end_value > max_thruster:
            best_phase_setting = phase_setting
            max_thruster = end_value

    if max_thruster != expected_max_thruster:
        raise Exception(f'Max thruster value should be {expected_max_thruster}')
    if best_phase_setting != expected_phase_setting:
        raise Exception(f'Phase setting for solution should be {expected_phase_setting}')
    return


def main():
    test_day7_star2_example1(
        [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
         27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5],
        (9, 8, 7, 6, 5),
        139629729
    )
    test_day7_star2_example1(
        [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
         -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
         53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10],
        (9, 7, 8, 5, 6),
        18216
    )


if __name__ == "__main__":
    main()