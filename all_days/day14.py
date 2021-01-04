# --- Day 14: Space Stoichiometry ---

# First star:
# You ask the nanofactory to produce a list of the reactions it can perform that are relevant to this process (your
# puzzle input). Every reaction turns some quantities of specific input chemicals into some quantity of an output
# chemical. Almost every chemical is produced by exactly one reaction; the only exception, ORE, is the raw material
# input to the entire process and is not produced by a reaction.
# You just need to know how much ORE you'll need to collect before you can produce one unit of FUEL.
# Each reaction gives specific quantities for its inputs and output; reactions cannot be partially run, so only whole
# integer multiples of these quantities can be used. (It's okay to have leftover chemicals when you're done, though.)
# You can run the full reaction as many times as necessary.
# Given the list of reactions in your puzzle input, what is the minimum amount of ORE required to produce exactly
# 1 FUEL?

# Second star:
# After collecting ORE for a while, you check your cargo hold: 1 trillion (1000000000000) units of ORE.
# Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?

from copy import deepcopy


def printable_formula(reactants, products):
    formula = ''
    for mol, nb in reactants.items():
        if nb > 0:
            formula = formula + str(nb) + ' ' + mol + ', '
    formula = formula[:-2] + ' => '
    for mol, nb in products.items():
        if nb > 0:
            formula = formula + str(nb) + ' ' + mol + ', '
    return formula[:-2]


class ChemicalReaction():
    @classmethod
    def from_dicts(cls, reactants, products, molecules):
        return cls(printable_formula(reactants, products), molecules)

    def __init__(self, formula, molecules):
        self.initial_formula = formula
        self.molecules = molecules
        reactants, products = formula.split('=>')
        self.reactants = {m: 0 for m in self.molecules}
        self.products = {m: 0 for m in self.molecules}
        for reactant in reactants.split(','):
            nb, mol = reactant.split()
            self.reactants[mol] = int(nb)
        nb, mol = products.split()
        self.products[mol] = int(nb)
        self.main_product = mol

    def use_reaction(self, reaction, authorized):
        if reaction.main_product in self.other_reactants(authorized):
            self.reactants = {mol: nb + nb0 for mol0, nb0 in reaction.reactants.items()
                              for mol, nb in self.reactants.items() if mol == mol0}
            self.products = {mol: nb + nb0 for mol0, nb0 in reaction.products.items()
                             for mol, nb in self.products.items() if mol == mol0}
            actual_reactants = [mol for mol, nb in self.reactants.items() if nb > 0]
            actual_products = [mol for mol, nb in self.products.items() if nb > 0]
            molecules_to_simplify = list(set(actual_reactants).intersection(actual_products))
            for molecule in molecules_to_simplify:
                value = min(self.reactants[molecule], self.products[molecule])
                self.reactants[molecule] -= value
                self.products[molecule] -= value
        return None

    def other_reactants(self, authorized):
        return [mol for mol, nb in self.reactants.items() if nb > 0 and mol not in authorized]

    def print_formula(self):
        print(printable_formula(self.reactants, self.products))


class Reserve():
    def __init__(self, nb_ores):
        if nb_ores is None:
            nb_ores = 1
        self.reactants = {'ORE': nb_ores}

    def present_molecules(self):
        return [k for k in self.reactants if self.reactants[k] > 0]

    def add(self, molecule, quantity):
        if molecule in self.reactants:
            self.reactants[molecule] += quantity
        else:
            self.reactants[molecule] = quantity

    def coefs_for_reaction(self, reaction):
        return {
            mol: self.reactants[mol] // reaction.reactants[mol] for mol in self.reactants if reaction.reactants[mol] > 0
        }

    def product_fuel(self, fuel_reaction, other_reactions):
        coefs = self.coefs_for_reaction(fuel_reaction)
        coef = min(coefs)
        while coef == 0:
            molecules_ok = {                                # Molecules we can use to transform fuel_reaction
                mol: fuel_reaction.reactants[mol] - self.reactants[mol]
                for mol, c in coefs.items() if c > 0
            }
            for reaction in other_reactions:                # Transform to use other molecules we have in reserve
                fuel_reaction.use_reaction(reaction, molecules_ok)
            if coefs['ORE'] == 0:                           # Specific treatment for ORE
                ore_reaction_found, n = False, 0
                while not ore_reaction_found:
                    reaction = other_reactions[n]
                    if (reaction.reactants['ORE']) > 0 and (reaction.main_product in molecules_ok):
                        fuel_reaction.reactants['ORE'] -= reaction.reactants['ORE']
                        fuel_reaction.reactants[reaction.main_product] += reaction.products[reaction.main_product]
                        ore_reaction_found = True
            coefs = self.coefs_for_reaction(fuel_reaction)  # Update coefs for fuel_reaction
            coef = min(coefs)
        fuel_created = coef
        for mol in self.reactants:
            self.reactants[mol] = self.reactants[mol] - coef * fuel_reaction.reactants[mol]
        for mol in fuel_reaction.products:
            self.add(mol, fuel_reaction.products[mol] * coef)
        self.reactants['FUEL'] = 0
        return fuel_created

    def get_ores(self, reactions):
        has_changed = True
        while has_changed:
            has_changed = False
            for reaction in reactions:
                if reaction.main_product in self.present_molecules():
                    molecule = reaction.main_product
                    if reaction.products[molecule] <= self.reactants[molecule]:
                        has_changed = True
                        coef = self.reactants[molecule] // reaction.products[molecule]
                        self.reactants[molecule] = self.reactants[molecule] % reaction.products[molecule]
                        for mol in reaction.reactants:
                            self.add(mol, coef * reaction.reactants[mol])

    def print(self):
        text = ' + '.join([' '.join([str(v), k]) for k, v in self.reactants.items() if v > 0])
        if len(text) == 0:
            print('Empty reserve')
        else:
         print(text)


def find_all_molecules(formulas):
    all_values = [x for formula in formulas for x in formula.replace('=>', '').replace(',', '').split()]
    all_values = list(set([all_values[n] for n in range(1, len(all_values), 2)]))
    return all_values


def chained_reactions(reactions, authorized=None):
    if authorized == None:
        authorized = ['ORE']
    final_reaction = [reaction for reaction in reactions if reaction.products['FUEL'] > 0][0]
    reactions = [reaction for reaction in reactions if reaction != final_reaction]
    while len(final_reaction.other_reactants(authorized)) > 0:
        for reaction in reactions:
            final_reaction.use_reaction(reaction, authorized)
    return final_reaction


def compute_total_fuel(reactions, total_ores):
    reserve = Reserve(total_ores)
    initial_reactions = deepcopy(reactions)
    fuel_reaction = chained_reactions(reactions)
    total_fuel = reserve.product_fuel(fuel_reaction)

    fuel_added = total_fuel
    while (fuel_added > 0) | (len(reserve.present_molecules()) > 1) :
        reactions = deepcopy(initial_reactions)
        fuel_reaction = chained_reactions(reactions, reserve)
        fuel_added = reserve.product_fuel(fuel_reaction)
        total_fuel += fuel_added
    return total_fuel


def run(data_dir, star):
    with open(f'{data_dir}/input-day14.txt', 'r') as fic:
        formulas =  fic.read().strip('\n').split('\n')
    all_molecules = find_all_molecules(formulas)
    reactions = [ChemicalReaction(formula, all_molecules) for formula in formulas]
    if star == 1:
        ores = chained_reactions(reactions).reactants['ORE']
        print(f'Star {star} - you need {ores} ORE molecules')
        return ores
    elif star == 2: # 2269324 too low
        total_fuel = compute_total_fuel(reactions, 1000000000000)
        print(f'Star {star} - I will produce {total_fuel} FUEL')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
