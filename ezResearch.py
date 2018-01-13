import pexpect
import argparse
import sys
import pickle
import numpy as np
from datetime import datetime
from time import time
import os
from functools import reduce

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("points", help="Pickle file containing the points to map a line to.")
    parser.add_argument("-i", "--iterations", default=20, type=int, 
        help="Number of times to run the program. Default = 20")
    parser.add_argument('-g', '--generations', default='100',
        help="Number of generations to run the each iteration for. Default = 100")

    args = parser.parse_args()
    fname = args.points
    iterations = args.iterations
    gens = args.generations

    gensNear = []
    gensSuccess = []
    numgens = []
    fitnesses = []
    solutions = []

    todays_date = datetime.fromtimestamp(time()).strftime('%Y-%m-%d')
    run_time = datetime.fromtimestamp(time()).strftime('%H-%M-%S')

    # create the file for pickling the constants and points in mainGA.py
    # used for logging
    # file is automatically removed at end of this function
    if not os.path.exists('params.pickle'):
        params_file = open('params.pickle', 'x')
        params_file.close()
    else:
        print('Error - pickle file for parameters already exists.')
        return

    # create directories for logging if they don't already exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('logs/{}'.format(todays_date)):
        os.makedirs('logs/{}'.format(todays_date))


    command = "python3 mainGA.py --subprocess -p " + fname
    for i in range(iterations):
        process = pexpect.spawn(command)
        process.expect("Enter the number of generations to iterate through: ")
        process.sendline(gens)
        #process.expect("Enter the number of generations to iterate through: ")
        #process.sendline("quit")
        process.expect("Process Finished")
        data = (process.before).decode(sys.stdout.encoding)
        data = data.split()

        print("\nIteration " + str(i+1) + " Complete!")
        if data[1] == '0.0':
            print("Best fitness: 0.0 [Perfect!]")
        else:
            print("Best fitness: " + data[1])
        print("Generations to produce: " + data[2])
        print("Number of unique solutions: " + data[3])
        if float(data[1]) <= 5.:
            gensNear.append(int(data[2]))
        if float(data[1]) == 0.:
            gensSuccess.append(int(data[2]))
        numgens.append(data[2])
        fitnesses.append(float(data[1]))
        solutions.append(int(data[3]))

    # open the logging pickle file for reading
    # read the constants and points
    params_file = open('params.pickle', 'rb')
    consts = pickle.load(params_file)
    points = pickle.load(params_file)

    # write constants, generations, points, and data from each run to the csv file
    with open('logs/{}/{}.csv'.format(todays_date, run_time), 'a') as csv_file:
        csv_file.write(',' + str(consts) + '\n\n')
        csv_file.write(',' + str(gens) + '\n\n')
        csv_file.write(',' + str(points) + '\n\n')
        for i in range(len(solutions)):
            csv_file.write(',{0:.3f},{1},{2},\n'.format(float(fitnesses[i]), numgens[i], solutions[i]))

    if len(gensNear) > 0:
        avgNear = reduce(lambda x, y: x + y, gensNear) / float(len(gensNear)) 
    else:
        avgNear = "No near successes"

    if len(gensSuccess) > 0:
        avgSuccess = reduce(lambda x, y: x + y, gensSuccess) / float(len(gensSuccess)) 
    else:
        avgSuccess = "No perfect successes" 

    avgFitness = fitnesses = reduce(lambda x, y: x + y, fitnesses) / float(len(fitnesses))
    avgSolutions = np.mean(solutions)

    print("\n\nAverage fitness across all iterations: " + str(avgFitness))
    print("\nAverage number of unique solutions: " + str(avgSolutions))
    print("\nNear success rate: " + str((len(gensNear) / iterations) * 100) + "%")
    print("Average generations for near success: " + str(avgNear))
    print("\nPerfect optimization rate: " + str((len(gensSuccess) / iterations) * 100) + "%")
    print("Average generations for perfect success: " + str(avgSuccess))

    # delete the pickle file used for logging
    if os.path.exists('params.pickle'):
        os.remove('params.pickle')

if __name__ == '__main__':
    main()

