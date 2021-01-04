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

class ChemicalReaction():
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

    def use_reaction(self, reaction):
        if reaction.main_product in self.other_reactants():
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

    def other_reactants(self):
        return [mol for mol, nb in self.reactants.items() if nb > 0 and mol != 'ORE']

    def print_formula(self):
        formula = ''
        for mol, nb in self.reactants.items():
            if nb > 0:
                formula = formula + str(nb) + ' ' + mol + ', '
        formula = formula[:-2] + ' => '
        for mol, nb in self.products.items():
            if nb > 0:
                formula = formula + str(nb) + ' ' + mol + ', '
        print(formula[:-2])


def find_all_molecules(formulas):
    all_values = [x for formula in formulas for x in formula.replace('=>', '').replace(',', '').split()]
    all_values = list(set([all_values[n] for n in range(1, len(all_values), 2)]))
    return all_values

def compute_ores(formulas):
    all_molecules = find_all_molecules(formulas)
    reactions = [ChemicalReaction(formula, all_molecules) for formula in formulas]
    final_reaction = [reaction for reaction in reactions if reaction.products['FUEL'] > 0][0]
    reactions = [reaction for reaction in reactions if reaction != final_reaction]
    while len(final_reaction.other_reactants()) > 0:
        for reaction in reactions:
            final_reaction.use_reaction(reaction)
    final_reaction.print_formula()
    return final_reaction.reactants['ORE']


def run(data_dir, star):
    with open(f'{data_dir}/input-day14.txt', 'r') as fic:
        reactions =  fic.read().strip('\n').split('\n')
    if star == 1:
        ores = compute_ores(reactions)
        print(f'Star {star} - you need {ores} ORE molecules')
        return
    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
