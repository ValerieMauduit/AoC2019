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
# Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).
# You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you
# move from any object to an object orbiting or orbited by that object.
# What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is
# orbiting? (Between the objects they are orbiting - not between YOU and SAN.)

import pandas as pd


def run(data_dir, star):
    with open(f'{data_dir}/input-day06.txt', 'r') as fic:
        orbits = fic.read().strip('\n').split('\n')
    df = pd.DataFrame({'rule': orbits})
    df[['center', 'satellite']] = df['rule'].str.split(')', expand=True)
    df['orbits'] = None
    counts = pd.DataFrame(columns=df.columns)
    level = 1
    while df.shape[0] > 0:
        condition = (df['center'].isin(list(df['satellite'])))
        counts = pd.concat([counts, df.loc[~condition]], ignore_index=True)
        counts['orbits'].fillna(level, inplace=True)
        df = df.loc[condition]
        level += 1

    if star == 1:
        total_orbits = counts['orbits'].sum()
        print(f'Star {star} - the total number of direct and indirect orbits is {total_orbits}')
        return total_orbits

    elif star == 2:
        me = 'YOU'
        san = 'SAN'
        if (counts.loc[counts['satellite'] == san, 'orbits'].values[0] >
                counts.loc[counts['satellite'] == me, 'orbits'].values[0]):
            me = 'SAN'
            san = 'YOU'

        transfers = 0
        while (counts.loc[counts['satellite'] == me, 'orbits'].values[0] >
               counts.loc[counts['satellite'] == san, 'orbits'].values[0]):
            center = counts.loc[counts['satellite'] == me, 'center'].values[0]
            transfers += 1
            counts = counts.loc[counts['satellite'] != me]
            counts.loc[counts['satellite'] == center, 'satellite'] = me

        while (counts.loc[counts['satellite'] == me, 'center'].values[0] !=
               counts.loc[counts['satellite'] == san, 'center'].values[0]):
            Ycenter = counts.loc[counts['satellite'] == me, 'center'].values[0]
            Scenter = counts.loc[counts['satellite'] == san, 'center'].values[0]
            transfers += 2
            counts = counts.loc[~counts['satellite'].isin([me, san])]
            counts.loc[counts['satellite'] == Ycenter, 'satellite'] = me
            counts.loc[counts['satellite'] == Scenter, 'satellite'] = san

        print(f'Star {star} - minimum transfers from YOU to SAN is {transfers}')
        return transfers

    else:
        raise Exception('Star number must be either 1 or 2.')
