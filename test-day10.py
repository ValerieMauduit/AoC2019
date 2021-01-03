from all_days.day10 import count_asteroids, find_best_place


# .#..#
# .....
# #####
# ....#
# ...##
# The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can detect
# 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its view of this
# asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or fewer other
# asteroids. Here is the number of other asteroids a monitoring station on each asteroid could detect:
# .7..7
# .....
# 67775
# ....7
# ...87

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

# Best is 5,8 with 33 other asteroids detected:
# ......#.#.
# #..#.#....
# ..#######.
# .#.#.###..
# .#..#.....
# ..#....#.#
# #..#....#.
# .##.#..###
# ##...#..#.
# .#....####

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

# Best is 1,2 with 35 other asteroids detected:
# #.#...#.#.
# .###....#.
# .#....#...
# ##.#.#.#.#
# ....#.#.#.
# .##..###.#
# ..#...##..
# ..##....##
# ......#...
# .####.###.

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

# Best is 6,3 with 41 other asteroids detected:
# .#..#..###
# ####.###.#
# ....###.#.
# ..###.##.#
# ##.##.#.#.
# ....###..#
# ..#.#..#.#
# #..#.#.###
# .##...##.#
# .....#.#..

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

# Best is 11,13 with 210 other asteroids detected:
# .#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##

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
    print('-- Test example 5 OK')

def main():
    test_example1()
    test_example2()
    test_example3()
    test_example4()
    test_example5()

if __name__ == '__main__':
    main()
