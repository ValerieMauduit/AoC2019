from all_days.day10 import find_best_place, vaporization_lazer, rotation


def test_example1():
    asteroids_map = [[x for x in raw] for raw in ['_#__#', '_____', '#####', '____#', '___##']]
    expected = [[0, 7, 0, 0, 7], [0, 0, 0, 0, 0], [6, 7, 7, 7, 5], [0, 0, 0, 0, 7], [0, 0, 0, 8, 7]]

    solution = find_best_place(asteroids_map)
    best_value = solution['value']
    best_position = solution['position']
    counts_map = solution['map']
    if best_position != (3, 4):
        raise Exception(f'Best location should be (3, 4) - encountered {best_position}')
    if best_value != 8:
        raise Exception(f'Best number of asteroids should be 8 - encountered {best_value}')
    if counts_map != expected:
        raise Exception('Full counts map have errors')
    print('-- Test example 1 OK')


def test_example2():
    asteroids_map = [[x for x in raw] for raw in [
        '......#.#.', '#..#.#....', '..#######.', '.#.#.###..', '.#..#.....',
        '..#....#.#', '#..#....#.', '.##.#..###', '##...#..#.', '.#....####'
    ]]
    solution = find_best_place(asteroids_map)
    best_value = solution['value']
    best_position = solution['position']
    if best_position != (5, 8):
        raise Exception(f'Best location should be (5, 8) - encountered {best_position}')
    if best_value != 33:
        raise Exception(f'Best number of asteroids should be 33 - encountered {best_value}')
    print('-- Test example 2 OK')


def test_example3():
    asteroids_map = [[x for x in raw] for raw in [
        '#.#...#.#.', '.###....#.', '.#....#...', '##.#.#.#.#', '....#.#.#.',
        '.##..###.#', '..#...##..', '..##....##', '......#...', '.####.###.'
    ]]
    solution = find_best_place(asteroids_map)
    best_value = solution['value']
    best_position = solution['position']
    if best_position != (1, 2):
        raise Exception(f'Best location should be (1, 2) - encountered {best_position}')
    if best_value != 35:
        raise Exception(f'Best number of asteroids should be 35 - encountered {best_value}')
    print('-- Test example 3 OK')


def test_example4():
    asteroids_map = [[x for x in raw] for raw in [
        '.#..#..###', '####.###.#', '....###.#.', '..###.##.#', '##.##.#.#.',
        '....###..#', '..#.#..#.#', '#..#.#.###', '.##...##.#', '.....#.#..'
    ]]
    solution = find_best_place(asteroids_map)
    best_value = solution['value']
    best_position = solution['position']
    if best_position != (6, 3):
        raise Exception(f'Best location should be (6, 3) - encountered {best_position}')
    if best_value != 41:
        raise Exception(f'Best number of asteroids should be 41 - encountered {best_value}')
    print('-- Test example 4 OK')


def test_example5():
    asteroids_map = [[x for x in raw] for raw in [
        '.#..##.###...#######', '##.############..##.', '.#.######.########.#', '.###.#######.####.#.',
        '#####.##.#.##.###.##', '..#####..#.#########', '####################', '#.####....###.#.#.##',
        '##.#################', '#####.##.###..####..', '..######..##.#######', '####.##.####...##..#',
        '.#####..#.######.###', '##...#.##########...', '#.##########.#######', '.####.#.###.###.#.##',
        '....##.##.###..#####', '.#.#.###########.###', '#.#.#.#####.####.###', '###.##.####.##.#..##'
    ]]
    solution = find_best_place(asteroids_map)
    best_value = solution['value']
    best_position = solution['position']
    if best_position != (11,13):
        raise Exception(f'Best location should be (11, 13) - encountered {best_position}')
    if best_value != 210:
        raise Exception(f'Best number of asteroids should be 210 - encountered {best_value}')

    asteroids_map[best_position[1]][best_position[0]] = 'X'
    asteroids_order = vaporization_lazer(asteroids_map, best_position)
    expected = {
        1: (11, 12), 2: (12, 1), 3: (12, 2), 10: (12, 8), 20: (16, 0), 50: (16, 9),
        100: (10, 16), 199: (9, 6), 200: (8, 2), 201: (10, 9), 299: (11, 1)
    }
    if len(asteroids_order) != 300:
        raise Exception(f'Length of asteroids shoots order should be 300, not {len(asteroids_order)}')
    for k in expected:
        if asteroids_order[k] != expected[k]:
            raise Exception(f'{k}th asteroid computation value is {asteroids_order[k]}, expected is {expected[k]}')
    print('-- Test example 5 OK')


def test_example6():
    asteroids_map = [[x for x in raw] for raw in [
        '.#....#####...#..', '##...##.#####..##', '##...#...#.#####.', '..#.....X...###..', '..#.#.....#....##'
    ]]
    position = (8, 3)
    expected = [
        (0, 0), (8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2), (15, 1), (12, 2), (13, 2), (14, 2),
        (15, 2), (12, 3), (16, 4), (15, 4), (10, 4), (4, 4), (2, 4), (2, 3), (0, 2), (1, 2), (0, 1), (1, 1), (5, 2),
        (1, 0), (5, 1), (6, 1), (6, 0), (7, 0), (8, 0), (10, 1), (14, 0), (16, 1), (13, 3), (14, 3)
     ]
    asteroids_order = vaporization_lazer(asteroids_map, position)
    for n in range(len(expected)):
        if asteroids_order[n] != expected[n]:
            raise Exception(f'{n}th astéroid computation value is {asteroids_order[n]}, expected is {expected[n]}')
    print('-- Test example 6 OK')


def main():
    test_example1()
    test_example2()
    test_example3()
    test_example4()
    test_example5()
    test_example6()


if __name__ == '__main__':
    main()
