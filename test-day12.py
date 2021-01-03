from all_days.day12 import Moon, NBobySystem, lcm


def test_apply_gravity():
    ganymede = Moon('<x=3, y=0, z=0>')
    callisto = Moon('<x=5, y=0, z=0>')
    ganymede.apply_gravity(callisto)
    callisto.apply_gravity(ganymede)
    if ganymede.velocity[0] != 1:
        raise Exception('Ganymede velocity X should become 1')
    if callisto.velocity[0] != -1:
        raise Exception('Callisto velocity X should become -1')
    print('-- Test Apply Gravity OK')


def test_apply_velocity():
    europa = Moon('<x=1, y=2, z=3>')
    europa.set_velocity('<x=-2, y=0, z=3>')
    europa.apply_velocity()
    if europa.printable_position() != '<x=-1, y=2, z=6>':
        raise Exception('Europe should have moved to position <x=-1, y=2, z=6>')
    print('-- Test Apply Velocity OK')


def test_complete_4bodies_problem():
    print('-- Complete 4-body test 1')
    io = Moon('<x=-1, y=0, z=2>')
    europa = Moon('<x=2, y=-10, z=-7>')
    ganymede = Moon('<x=4, y=-8, z=8>')
    callisto = Moon('<x=3, y=5, z=-1>')
    moons = NBobySystem([io, europa, ganymede, callisto])

    expected = [
        [
            'pos=<x=-1, y=0, z=2>, vel=<x=0, y=0, z=0>', 'pos=<x=2, y=-10, z=-7>, vel=<x=0, y=0, z=0>',
            'pos=<x=4, y=-8, z=8>, vel=<x=0, y=0, z=0>', 'pos=<x=3, y=5, z=-1>, vel=<x=0, y=0, z=0>'
        ],
        [
            'pos=<x=2, y=-1, z=1>, vel=<x=3, y=-1, z=-1>', 'pos=<x=3, y=-7, z=-4>, vel=<x=1, y=3, z=3>',
            'pos=<x=1, y=-7, z=5>, vel=<x=-3, y=1, z=-3>', 'pos=<x=2, y=2, z=0>, vel=<x=-1, y=-3, z=1>'
        ],
        [
            'pos=<x=5, y=-3, z=-1>, vel=<x=3, y=-2, z=-2>', 'pos=<x=1, y=-2, z=2>, vel=<x=-2, y=5, z=6>',
            'pos=<x=1, y=-4, z=-1>, vel=<x=0, y=3, z=-6>', 'pos=<x=1, y=-4, z=2>, vel=<x=-1, y=-6, z=2>'
        ],
        [
            'pos=<x=5, y=-6, z=-1>, vel=<x=0, y=-3, z=0>', 'pos=<x=0, y=0, z=6>, vel=<x=-1, y=2, z=4>',
            'pos=<x=2, y=1, z=-5>, vel=<x=1, y=5, z=-4>', 'pos=<x=1, y=-8, z=2>, vel=<x=0, y=-4, z=0>'
        ],
        [
            'pos=<x=2, y=-8, z=0>, vel=<x=-3, y=-2, z=1>', 'pos=<x=2, y=1, z=7>, vel=<x=2, y=1, z=1>',
            'pos=<x=2, y=3, z=-6>, vel=<x=0, y=2, z=-1>', 'pos=<x=2, y=-9, z=1>, vel=<x=1, y=-1, z=-1>'
        ],
        [
            'pos=<x=-1, y=-9, z=2>, vel=<x=-3, y=-1, z=2>', 'pos=<x=4, y=1, z=5>, vel=<x=2, y=0, z=-2>',
            'pos=<x=2, y=2, z=-4>, vel=<x=0, y=-1, z=2>', 'pos=<x=3, y=-7, z=-1>, vel=<x=1, y=2, z=-2>'
        ],
        [
            'pos=<x=-1, y=-7, z=3>, vel=<x=0, y=2, z=1>', 'pos=<x=3, y=0, z=0>, vel=<x=-1, y=-1, z=-5>',
            'pos=<x=3, y=-2, z=1>, vel=<x=1, y=-4, z=5>', 'pos=<x=3, y=-4, z=-2>, vel=<x=0, y=3, z=-1>'
        ],
        [
            'pos=<x=2, y=-2, z=1>, vel=<x=3, y=5, z=-2>', 'pos=<x=1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>',
            'pos=<x=3, y=-7, z=5>, vel=<x=0, y=-5, z=4>', 'pos=<x=2, y=0, z=0>, vel=<x=-1, y=4, z=2>'
        ],
        [
            'pos=<x=5, y=2, z=-2>, vel=<x=3, y=4, z=-3>', 'pos=<x=2, y=-7, z=-5>, vel=<x=1, y=-3, z=-1>',
            'pos=<x=0, y=-9, z=6>, vel=<x=-3, y=-2, z=1>', 'pos=<x=1, y=1, z=3>, vel=<x=-1, y=1, z=3>'
        ],
        [
            'pos=<x=5, y=3, z=-4>, vel=<x=0, y=1, z=-2>', 'pos=<x=2, y=-9, z=-3>, vel=<x=0, y=-2, z=2>',
            'pos=<x=0, y=-8, z=4>, vel=<x=0, y=1, z=-2>', 'pos=<x=1, y=1, z=5>, vel=<x=0, y=0, z=2>'
        ],
        [
            'pos=<x=2, y=1, z=-3>, vel=<x=-3, y=-2, z=1>', 'pos=<x=1, y=-8, z=0>, vel=<x=-1, y=1, z=3>',
            'pos=<x=3, y=-6, z=1>, vel=<x=3, y=2, z=-3>', 'pos=<x=2, y=0, z=4>, vel=<x=1, y=-1, z=-1>'
        ]
    ]
    for step in range(11):
        summary = moons.printable_summary()
        for calc, exp in zip(summary, expected[step]):
            if calc != exp:
                raise Exception(f'Step {step}: Moon summary expected {exp} - found {calc}')
        if step < 10:
            moons.run_step()

    potential_energies = [body.potential_energy() for body in moons.moons_list]
    expected = [6, 9, 10, 6]
    if potential_energies != expected:
        raise Exception(f'Expecting potential energies: {expected}, found: {potential_energies}')
    kinetic_energies = [body.kinetic_energy() for body in moons.moons_list]
    expected = [6, 5, 8, 3]
    if kinetic_energies != expected:
        raise Exception(f'Expecting kinetic energies: {expected}, found: {kinetic_energies}')
    total_energies = [body.total_energy() for body in moons.moons_list]
    expected = [36, 45, 80, 18]
    if total_energies != expected:
        raise Exception(f'Expecting total energies: {expected}, found: {total_energies}')
    total_energy = moons.total_energy()
    if total_energy != 179:
        raise Exception(f'Expecting total energy 179, found: {total_energy}')


def test_complete_4bodies_problem2():
    print('-- Complete 4-body test 2')
    io = Moon('<x=-8, y=-10, z=0>')
    europa = Moon('<x=5, y=5, z=10>')
    ganymede = Moon('<x=2, y=-7, z=3>')
    callisto = Moon('<x=9, y=-8, z=-3>')
    moons = NBobySystem([io, europa, ganymede, callisto])

    expected = [
        [
            'pos=<x=-8, y=-10, z=0>, vel=<x=0, y=0, z=0>', 'pos=<x=5, y=5, z=10>, vel=<x=0, y=0, z=0>',
            'pos=<x=2, y=-7, z=3>, vel=<x=0, y=0, z=0>', 'pos=<x=9, y=-8, z=-3>, vel=<x=0, y=0, z=0>'
        ],
        [
            'pos=<x=-9, y=-10, z=1>, vel=<x=-2, y=-2, z=-1>', 'pos=<x=4, y=10, z=9>, vel=<x=-3, y=7, z=-2>',
            'pos=<x=8, y=-10, z=-3>, vel=<x=5, y=-1, z=-2>', 'pos=<x=5, y=-10, z=3>, vel=<x=0, y=-4, z=5>'
        ],
        [
            'pos=<x=-10, y=3, z=-4>, vel=<x=-5, y=2, z=0>', 'pos=<x=5, y=-25, z=6>, vel=<x=1, y=1, z=-4>',
            'pos=<x=13, y=1, z=1>, vel=<x=5, y=-2, z=2>', 'pos=<x=0, y=1, z=7>, vel=<x=-1, y=-1, z=2>'
        ],
        [
            'pos=<x=15, y=-6, z=-9>, vel=<x=-5, y=4, z=0>', 'pos=<x=-4, y=-11, z=3>, vel=<x=-3, y=-10, z=0>',
            'pos=<x=0, y=-1, z=11>, vel=<x=7, y=4, z=3>', 'pos=<x=-3, y=-2, z=5>, vel=<x=1, y=2, z=-3>'
        ],
        [
            'pos=<x=14, y=-12, z=-4>, vel=<x=11, y=3, z=0>', 'pos=<x=-1, y=18, z=8>, vel=<x=-5, y=2, z=3>',
            'pos=<x=-5, y=-14, z=8>, vel=<x=1, y=-2, z=0>', 'pos=<x=0, y=-12, z=-2>, vel=<x=-7, y=-3, z=-3>'
        ],
        [
            'pos=<x=-23, y=4, z=1>, vel=<x=-7, y=-1, z=2>', 'pos=<x=20, y=-31, z=13>, vel=<x=5, y=3, z=4>',
            'pos=<x=-4, y=6, z=1>, vel=<x=-1, y=1, z=-3>', 'pos=<x=15, y=1, z=-5>, vel=<x=3, y=-3, z=-3>'
        ],
        [
            'pos=<x=36, y=-10, z=6>, vel=<x=5, y=0, z=3>', 'pos=<x=-18, y=10, z=9>, vel=<x=-3, y=-7, z=5>',
            'pos=<x=8, y=-12, z=-3>, vel=<x=-2, y=1, z=-7>', 'pos=<x=-18, y=-8, z=-2>, vel=<x=0, y=6, z=-1>'
        ],
        [
            'pos=<x=-33, y=-6, z=5>, vel=<x=-5, y=-4, z=7>', 'pos=<x=13, y=-9, z=2>, vel=<x=-2, y=11, z=3>',
            'pos=<x=11, y=-8, z=2>, vel=<x=8, y=-6, z=-7>', 'pos=<x=17, y=3, z=1>, vel=<x=-1, y=-1, z=-3>'
        ],
        [
            'pos=<x=30, y=-8, z=3>, vel=<x=3, y=3, z=0>', 'pos=<x=-2, y=-4, z=0>, vel=<x=4, y=-13, z=2>',
            'pos=<x=-18, y=-7, z=15>, vel=<x=-8, y=2, z=-2>', 'pos=<x=-2, y=-1, z=-8>, vel=<x=1, y=8, z=0>'
        ],
        [
            'pos=<x=-25, y=-1, z=4>, vel=<x=1, y=-3, z=4>', 'pos=<x=2, y=-9, z=0>, vel=<x=-3, y=13, z=-1>',
            'pos=<x=32, y=-8, z=14>, vel=<x=5, y=-4, z=6>', 'pos=<x=-1, y=-2, z=-8>, vel=<x=-3, y=-6, z=-9>'
        ],
        [
            'pos=<x=8, y=-12, z=-9>, vel=<x=-7, y=3, z=0>', 'pos=<x=13, y=16, z=-3>, vel=<x=3, y=-11, z=-5>',
            'pos=<x=-29, y=-11, z=-1>, vel=<x=-3, y=7, z=4>', 'pos=<x=16, y=-13, z=23>, vel=<x=7, y=1, z=1>'
        ],
    ]
    summary = moons.printable_summary()
    for calc, exp in zip(summary, expected[0]):
        if calc != exp:
            raise Exception(f'Moon summary expected {exp} - found {calc}')

    for step in range(10):
        moons.run_steps(10)
        summary = moons.printable_summary()
        for calc, exp in zip(summary, expected[step + 1]):
            if calc != exp:
                raise Exception(f'Step {(step + 1) * 10}: Moon summary expected {exp} - found {calc}')

    potential_energies = [body.potential_energy() for body in moons.moons_list]
    expected = [29, 32, 41, 52]
    if potential_energies != expected:
        raise Exception(f'Expecting potential energies: {expected}, found: {potential_energies}')
    kinetic_energies = [body.kinetic_energy() for body in moons.moons_list]
    expected = [10, 19, 14, 9]
    if kinetic_energies != expected:
        raise Exception(f'Expecting kinetic energies: {expected}, found: {kinetic_energies}')
    total_energies = [body.total_energy() for body in moons.moons_list]
    expected = [290, 608, 574, 468]
    if total_energies != expected:
        raise Exception(f'Expecting total energies: {expected}, found: {total_energies}')
    total_energy = moons.total_energy()
    if total_energy != 1940:
        raise Exception(f'Expecting total energy 179, found: {total_energy}')


def test_system_loops_small():
    print('-- 4-body system: time to return to initial state')
    io = Moon('<x= -1, y=  0, z=  2>')
    europa = Moon('<x=  2, y=-10, z= -7>')
    ganymede = Moon('<x=  4, y= -8, z=  8>')
    callisto = Moon('<x=  3, y=  5, z= -1>')
    moons = NBobySystem([io, europa, ganymede, callisto])

    expected = {
        0: [
           'pos=<x=-1, y=0, z=2>, vel=<x=0, y=0, z=0>', 'pos=<x=2, y=-10, z=-7>, vel=<x=0, y=0, z=0>',
            'pos=<x=4, y=-8, z=8>, vel=<x=0, y=0, z=0>', 'pos=<x=3, y=5, z=-1>, vel=<x=0, y=0, z=0>'
        ],
        2770: [
            'pos=<x=2, y=-1, z=1>, vel=<x=-3, y=2, z=2>', 'pos=<x=3, y=-7, z=-4>, vel=<x=2, y=-5, z=-6>',
            'pos=<x=1, y=-7, z=5>, vel=<x=0, y=-3, z=6>', 'pos=<x=2, y=2, z=0>, vel=<x=1, y=6, z=-2>'
        ],
        2771: [
            'pos=<x=-1, y=0, z=2>, vel=<x=-3, y=1, z=1>', 'pos=<x=2, y=-10, z=-7>, vel=<x=-1, y=-3, z=-3>',
            'pos=<x=4, y=-8, z=8>, vel=<x=3, y=-1, z=3>', 'pos=<x=3, y=5, z=-1>, vel=<x=1, y=3, z=-1>'
        ],
        2772: [
            'pos=<x=-1, y=0, z=2>, vel=<x=0, y=0, z=0>', 'pos=<x=2, y=-10, z=-7>, vel=<x=0, y=0, z=0>',
            'pos=<x=4, y=-8, z=8>, vel=<x=0, y=0, z=0>', 'pos=<x=3, y=5, z=-1>, vel=<x=0, y=0, z=0>'
        ],
    }
    summary = moons.printable_summary()
    for calc, exp in zip(summary, expected[0]):
        if calc != exp:
            raise Exception(f'Moon summary expected {exp} - found {calc}')
    moons.run_steps(2770, verbose=False)

    summary = moons.printable_summary()
    for calc, exp in zip(summary, expected[2770]):
        if calc != exp:
            raise Exception(f'Moon summary expected {exp} - found {calc}')
    moons.run_step()
    summary = moons.printable_summary()
    for calc, exp in zip(summary, expected[2771]):
        if calc != exp:
            raise Exception(f'Moon summary expected {exp} - found {calc}')
    moons.run_step()
    summary = moons.printable_summary()
    for calc, exp in zip(summary, expected[2772]):
        if calc != exp:
            raise Exception(f'Moon summary expected {exp} - found {calc}')

    io = Moon('<x= -1, y=  0, z=  2>')
    europa = Moon('<x=  2, y=-10, z= -7>')
    ganymede = Moon('<x=  4, y= -8, z=  8>')
    callisto = Moon('<x=  3, y=  5, z= -1>')
    moons = NBobySystem([io, europa, ganymede, callisto])
    if moons.loop_to_initial_state() != 2772:
        raise Exception('Computation of number of steps to return initial state should provide 2772')

    moonsX = NBobySystem([
        Moon('<x=-1, y=0, z=2>'), Moon('<x=2, y=-10, z=-7>'), Moon('<x=4, y=-8, z=8>'), Moon('<x=3, y=5, z=-1>')
    ])
    valX = moonsX.loop_to_initial_state_1D(0)
    moonsY = NBobySystem([
        Moon('<x=-1, y=0, z=2>'), Moon('<x=2, y=-10, z=-7>'), Moon('<x=4, y=-8, z=8>'), Moon('<x=3, y=5, z=-1>')
    ])
    valY = moonsY.loop_to_initial_state_1D(1)
    moonsZ = NBobySystem([
        Moon('<x=-1, y=0, z=2>'), Moon('<x=2, y=-10, z=-7>'), Moon('<x=4, y=-8, z=8>'), Moon('<x=3, y=5, z=-1>')
    ])
    valZ = moonsZ.loop_to_initial_state_1D(2)
    if lcm([valX, valY, valZ]) != 2772:
        raise Exception('Smart computation of number of steps to return initial state should provide 2772')


def test_system_loops_large():
    print('-- 4-body system: time to return to initial state')

    moonsX = NBobySystem([
        Moon('<x=-8, y=-10, z=0>'), Moon('<x=5, y=5, z=10>'), Moon('<x=2, y=-7, z=3>'), Moon('<x=9, y=-8, z=-3>')
    ])
    valX = moonsX.loop_to_initial_state_1D(0)
    moonsY = NBobySystem([
        Moon('<x=-8, y=-10, z=0>'), Moon('<x=5, y=5, z=10>'), Moon('<x=2, y=-7, z=3>'), Moon('<x=9, y=-8, z=-3>')
    ])
    valY = moonsY.loop_to_initial_state_1D(1)
    moonsZ = NBobySystem([
        Moon('<x=-8, y=-10, z=0>'), Moon('<x=5, y=5, z=10>'), Moon('<x=2, y=-7, z=3>'), Moon('<x=9, y=-8, z=-3>')
    ])
    valZ = moonsZ.loop_to_initial_state_1D(2)
    nb_steps = 4686774924
    if lcm([valX, valY, valZ]) != nb_steps:
        raise Exception(f'Smart computation of number of steps to return initial state should provide {nb_steps}')


def main():
    test_apply_gravity()
    test_apply_velocity()
    test_complete_4bodies_problem()
    test_complete_4bodies_problem2()
    test_system_loops_small()
    test_system_loops_large()


if __name__ == '__main__':
    main()
