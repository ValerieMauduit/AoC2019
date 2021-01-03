# --- Day 12: The N-Body Problem ---

# First star:
# You decide to start by tracking the four largest moons: Io, Europa, Ganymede, and Callisto.
# After a brief scan, you calculate the position of each moon (your puzzle input). You just need to simulate their
# motion so you can avoid them.
# Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional velocity. The position of each moon is given
# in your scan; the x, y, and z velocity of each moon starts at 0.
# Simulate the motion of the moons in time steps. Within each time step, first update the velocity of every moon by
# applying gravity. Then, once all moons' velocities have been updated, update the position of every moon by applying
# velocity. Time progresses by one step once all of the positions are updated.
# To apply gravity, consider every pair of moons. On each axis (x, y, and z), the velocity of each moon changes by
# exactly +1 or -1 to pull the moons together. However, if the positions on a given axis are the same, the velocity on
# that axis does not change for that pair of moons.
# Once all gravity has been applied, apply velocity: simply add the velocity of each moon to its own position.
# This process does not modify the velocity of any moon.
# Then, it might help to calculate the total energy in the system. The total energy for a single moon is its potential
# energy multiplied by its kinetic energy. A moon's potential energy is the sum of the absolute values of its x, y, and
# z position coordinates. A moon's kinetic energy is the sum of the absolute values of its velocity coordinates.
# What is the total energy in the system after simulating the moons given in your scan for 1000 steps?

# Second star:

class Moon():
    def __init__(self, scan):
        coords = scan[1:-1].split(', ')
        self.position = (int(coords[0].split('=')[1]), int(coords[1].split('=')[1]), int(coords[2].split('=')[1]))
        self.velocity = (0, 0, 0)

    def printable_position(self):
        return '<' + ', '.join([c + str(x) for x, c in zip(self.position, ['x=', 'y=', 'z='])]) + '>'

    def printable_velocity(self):
        return '<' + ', '.join([c + str(x) for x, c in zip(self.velocity, ['x=', 'y=', 'z='])]) + '>'

    def printable_summary(self):
        return 'pos=' + self.printable_position() + ', vel=' + self.printable_velocity()

    def apply_gravity(self, other):
        deltax = (self.position[0] < other.position[0]) - (self.position[0] > other.position[0])
        deltay = (self.position[1] < other.position[1]) - (self.position[1] > other.position[1])
        deltaz = (self.position[2] < other.position[2]) - (self.position[2] > other.position[2])
        self.velocity = (self.velocity[0] + deltax, self.velocity[1] + deltay, self.velocity[2] + deltaz)
        return None

    def set_velocity(self, velocity_description):
        coords = velocity_description[1:-1].split(', ')
        self.velocity = (int(coords[0].split('=')[1]), int(coords[1].split('=')[1]), int(coords[2].split('=')[1]))

    def apply_velocity(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
            self.position[2] + self.velocity[2]
        )

    def potential_energy(self):
        return abs(self.position[0]) + abs(self.position[1]) + abs(self.position[2])

    def kinetic_energy(self):
        return abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()


class NBobySystem():
    def __init__(self, moons_list):
        self.moons_list = moons_list
        self.n = len(moons_list)

    def apply_gravity(self):
        for body0 in self.moons_list:
            for body1 in self.moons_list:
                body0.apply_gravity(body1)
        return None

    def apply_velocities(self):
        for body in self.moons_list:
            body.apply_velocity()
        return None

    def run_step(self):
        self.apply_gravity()
        self.apply_velocities()

    def total_energy(self):
        return sum([body.total_energy() for body in self.moons_list])

    def printable_summary(self):
        return [body.printable_summary() for body in self.moons_list]


def run(data_dir, star):
    with open(f'{data_dir}/input-day12.txt', 'r') as fic:
        moons = fic.read().strip('\n').split('\n')
    if star == 1:
        system = NBobySystem([Moon(moon) for moon in moons])
        for n in range(1000):
            system.run_step()
        print(f'Star {star} - Total energy is {system.total_energy()}')
        return system.total_energy()
    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
