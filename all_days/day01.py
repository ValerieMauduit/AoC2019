# Day 1: The Tyranny of the Rocket Equation

# First star:
# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module,
# take its mass, divide by three, round down, and subtract 2.
# The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed
# for the mass of each module (your puzzle input), then add together all the fuel values.
# What is the sum of the fuel requirements for all of the modules on your spacecraft?

# Second star:
# During the second Go / No Go poll, the Elf in charge of the Rocket Equation Double-Checker stops the launch sequence.
# Apparently, you forgot to include additional fuel for the fuel you just added.
# Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However,
# that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel
# should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing
# really hard, which has no mass and is outside the scope of this calculation.
# So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated
# as the input mass and repeat the process, continuing until a fuel requirement is zero or negative.
# What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the
# mass of the added fuel? (Calculate the fuel requirements for each module separately, then add them all up at the end.)


def total_fuel(mass):
    if mass // 3 <= 2:
        return 0
    else:
        return mass // 3 - 2 + total_fuel(mass // 3 - 2)


def run(data_dir, star):
    with open(f'{data_dir}/input-day01.txt', 'r') as fic:
        modules = [int(x) for x in fic.read().split('\n')[:-1]]

    if star == 1:
        fuel_requirement = sum([x // 3 - 2 for x in modules])
    elif star == 2:
        fuel_requirement = sum([total_fuel(module) for module in modules])
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'Fuel requirement (star {star}) is: {fuel_requirement}')
    return fuel_requirement