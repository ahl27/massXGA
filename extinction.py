import random
import GAops
from GAindiv import individual
from mainGA import get_rates, CONST_BITS, NUM_VALS, EXTINCT_RANDOM_NUM


# Mass extinction with no change to the parameters
# Inputs:
#     -Population: population of individuals
#     -Points: set of points
#     -percent_to_kill: percentage of the total population to kill off (float between 0 and 1)
#     -total_gens: total number of generations that have finished (TOTAL_GENS global param from mainGA.py)
#     -interval: integer describing how often to perform this (ex. interval=5 means every 5 generations)
#     -gens_to_repop (optional): for gradual repopulation, defines the number of steps to take to repopulate
#     -altparams: list containing alternate parameters, for the adaptive repopulation.
#                 size of this list can be from 0-4, and omitted values will use the default values from mainGA
#             ~Index 0 corresponds to Tournament_Size
#             ~Index 1 corresponds to Tournament_Rate
#             ~Index 2 corresponds to Crossover_Rate
#             ~Index 3 corresponds to Mutation_Rate
def extinct(population, points, percent_to_kill, total_gens, interval, gens_to_repop=1, altparams=[]):
    # this only runs every [interval] generations
    if interval <= 0:
        return population
        
    if total_gens%interval != 0 or total_gens == 0:
        return population



    # this will get the normal parameters from mainGA.py
    params = get_rates()

    # picking better names for some key variables
    total_members = len(population)    
    num_to_remove = int(total_members * percent_to_kill)
    tourn_size = params[0]
    tourn_rate = params[1]
    x_rate = params[2]
    mute_rate = params[3]

    # this list will hold the change in each parameter per generation
    change = []
    for i in range(len(altparams)):
        change.append((params[i] - altparams[i])/gens_to_repop)

    while len(change) < 4:
        altparams.append(params[len(change)])
        change.append(0)




    # random.sample(range(max), k) returns a list of k unique numbers between 0 and max
    indexes_to_remove = random.sample(range(total_members), num_to_remove)

    new_pop = []

    for i in range(len(population)):
        if i not in indexes_to_remove:
            new_pop.append(individual(population[i].get_value_list()))

    # add random members to population if indicated by EXTINCT_RANDOM
    for i in range(EXTINCT_RANDOM_NUM):
        # these are two's complement bit strings
        memberVals = [''.join(random.choice(['0', '1'])
                        for j in range(CONST_BITS))
                        for k in range(NUM_VALS)]

        member = individual(memberVals)
        # adding member to the population
        new_pop.append(member)

    # at this point we've killed off a percentage of the population, so len(new_pop) < len(population)
    # now we have to repopulate

    # this will be the number of individuals added per generation
    add_per_gen = int((total_members - len(new_pop)) / gens_to_repop)

    # this handles gradual repopulation
    for i in range(gens_to_repop):
        # selection
        if i == gens_to_repop - 1:
            # this line resolves rounding errors by setting the total size to total_members on the last iteration
            new_pop = GAops.selection(population, points, int(altparams[0]), altparams[1], size=total_members)
        else:   
            new_pop = GAops.selection(population, points, int(altparams[0]), altparams[1], size=len(new_pop) + add_per_gen)
    
        # crossover
        GAops.crossover(new_pop, altparams[2])

        # mutation
        GAops.mutate_bits(new_pop, altparams[3])

        for i in range(4):
            altparams[i] += change[i]

    return new_pop







