# --- Day 6: Universal Orbit Map ---

# First star:
# You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring
# between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You
# download a map of the local orbits (your puzzle input).
# Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object.
# Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To
# verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits and
# indirect orbits.
# Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A
# orbits B, B orbits C, and C orbits D, then A indirectly orbits D.
# What is the total number of direct and indirect orbits in your map data?

# Second star:

def run(data_dir, star):
    with open(f'{data_dir}/input-day06.txt', 'r') as fic:
        tempo = [x.split(',') for x in fic.read().strip('\n').split('\n')]
    if star == 1:
        print(f'Star {star} - ')
        return
    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
