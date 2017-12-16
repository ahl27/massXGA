import random
import math
from GAindiv import *

#selecting members from the population to be parents for the next generation
def selection(population, points, k, p):
    #k is the tournament size
    #p is the probability that the highest fitness individual will be selected
    size = len(population)
    newPopulation = []

    newPopulation.append(individual(population[0].get_value_list()))

    while len(newPopulation) < size:
        #random.sample will pick unique numbers from the range specified
        indices = random.sample(range(size), k)
        contestants = []

        '''
        if 0 in indices:
            newPopulation.append(population[0])
            continue
        '''

        #select contestants
        for index in indices:
            contestants.append(population[index])

        #sort based on fitness, best fitness to worst
        contestants.sort(key=lambda indiv: indiv.calculate_fitness(points), reverse=False)

        #random roll, 0-1
        roll = random.random()

        #this loop will select an individual based on the roll
        rate = 0
        i = 0
        while i < (k-1) and i >= 0:
            rate += p*((1-p)**i)

            if roll < rate:
                newPopulation.append(individual(contestants[i].get_value_list()))
                i = -1
            else:
                i+=1

        #if we didn't select an individual, the last one will be selected
        if i > 0:
            newPopulation.append(individual(contestants[i].get_value_list()))

    return newPopulation



#crossover between two individuals in population
def crossover(population, rate):
    for i in range(math.floor(len(population)/2)):
        roll = random.random()

        if roll > rate:
            continue

        parent1 = population[2*i]
        parent2 = population[2*i+1]

        #making the complete genome (bitstring) for each parent
        genome1 = parent1.get_bitstring()
        genome2 = parent2.get_bitstring()

        #pick a random point to cross over
        #to switch between two point and uniform, (un)comment the first ''' and (un)comment the third '''

        '''

        #two point crossover
        splitPoint1 = math.floor(random.random() * len(genome1))
        splitPoint2 = math.floor(random.random() * len(genome1))

        if splitPoint1 > splitPoint2:
            temp = splitPoint1
            splitPoint1 = splitPoint2
            splitPoint2 = temp

        newGenome1 = genome1[:splitPoint1] + genome2[splitPoint1:splitPoint2] + genome1[splitPoint2:]
        newGenome2 = genome2[:splitPoint1] + genome1[splitPoint1:splitPoint2] + genome1[splitPoint2:]

        '''

        #uniform crossover
        MASK_PROB = 0.2
        base_mask = '0' * len(genome1)
        mask = ''
        for i in range(len(base_mask)):
            roll2 = random.random()
            if roll2 < MASK_PROB:
                mask += '1'
            else:
                mask += '0'

        newGenome1 = ''
        newGenome2 = ''
        for i in range(len(genome1)):
            newGenome1 += genome1[i] if mask[i] == '0' else genome2[i]
            newGenome2 += genome2[i] if mask[i] == '0' else genome1[i]

        #'''

        #set the new values of the individuals
        parent1.set_bitstring(newGenome1)
        parent2.set_bitstring(newGenome2)


#mutates the bits of individuals in the population
def mutate_bits(population, rate):
    mutations = 0

    #iterates through the bitstrings for each individual and generates a number between 0 and 1 for each
    #if the number is less than rate, the bit is flipped (0 to 1 or 1 to 0)
    for individual in population:
        bitstring = individual.get_bitstring()

        newBitstring = ''
        for bit in bitstring:
            roll = random.random()
            if roll <= rate:
                mutations += 1
                newBitstring += '1' if bit == '0' else '0'
            else:
                newBitstring += bit

        individual.set_bitstring(newBitstring)

    return mutations


#TODO: mass extinction
#def extinct():

