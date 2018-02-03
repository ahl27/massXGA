import pexpect
import argparse
import sys
import pickle
import numpy as np
from scipy import stats
from datetime import datetime
from time import time
import os
from functools import reduce
from io import open

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

    # make sure logs file exists
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # List of sets of settings to use for multiple runs.  Empty string uses values defined in mainGA
    # Each string contains 6 values:
    #       NUM_VALS
    #       EXTINCT_PERCENT
    #       EXTINCT_INTERVAL
    #       EXTINCT_LIST
    #       REPOP_RATE
    #       ALTPARAMS
    run_settings = ["7 0.50 0 '[]' 1 '[]'", "7 0.50 5 '[]' 1 '[]'", "7 0.50 5 '[]' 5 '[]'",
                    "7 0.50 5 '[]' 10 '[]'", "7 0.50 5 '[]' 20 '[]'",
                    "7 0.50 10 '[]' 1 '[]'", "7 0.50 10 '[]' 5 '[]'",
                    "7 0.50 10 '[]' 10 '[]'", "7 0.50 10 '[]' 20 '[]'",
                    "7 0.50 20 '[]' 1 '[]'", "7 0.50 20 '[]' 5 '[]'",
                    "7 0.50 20 '[]' 10 '[]'", "7 0.50 20 '[]' 20 '[]'",
                    "7 0.50 50 '[]' 1 '[]'", "7 0.50 50 '[]' 5 '[]'",
                    "7 0.50 50 '[]' 10 '[]'", "7 0.50 50 '[]' 20 '[]'"]
    # run_settings = ["7 0.50 0 '[]' 1 '[]'", "7 0.50 5 '[]' 5 '[5, 0.5, 0.8, 0.4]'",
    #                 "7 0.50 5 '[]' 10 '[5, 0.5, 0.8, 0.4]'", "7 0.50 5 '[]' 20 '[5, 0.5, 0.8, 0.4]'",
    #                 "7 0.50 10 '[]' 5 '[5, 0.5, 0.8, 0.4]'",
    #                 "7 0.50 10 '[]' 10 '[5, 0.5, 0.8, 0.4]'", "7 0.50 10 '[]' 20 '[5, 0.5, 0.8, 0.4]'",
    #                 "7 0.50 20 '[]' 5 '[5, 0.5, 0.8, 0.4]'",
    #                 "7 0.50 20 '[]' 10 '[5, 0.5, 0.8, 0.4]'", "7 0.50 20 '[]' 20 '[5, 0.5, 0.8, 0.4]'",
    #                 "7 0.50 50 '[]' 5 '[5, 0.5, 0.8, 0.4]'",
    #                 "7 0.50 50 '[]' 10 '[5, 0.5, 0.8, 0.4]'", "7 0.50 50 '[]' 20 '[5, 0.5, 0.8, 0.4]'"]
    # run_settings = ["7 0.50 0 '[5, 15, 25]' 1 '[]'", "7 0.50 5 '[5, 15, 25]' 1 '[]'", "7 0.50 5 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.50 5 '[5, 15, 25]' 10 '[]'",
    #                 "7 0.50 10 '[5, 15, 25]' 1 '[]'", "7 0.50 10 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.50 10 '[5, 15, 25]' 10 '[]'",
    #                 "7 0.50 20 '[5, 15, 25]' 1 '[]'", "7 0.50 20 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.50 20 '[5, 15, 25]' 10 '[]'",
    #                 "7 0.50 50 '[5, 15, 25]' 1 '[]'", "7 0.50 50 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.50 50 '[5, 15, 25]' 10 '[]'"]
    # run_settings = ["7 0.250 0 '[5, 15, 25]' 1 '[]'", "7 0.250 5 '[5, 15, 25]' 1 '[]'", "7 0.250 5 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.250 5 '[5, 15, 25]' 10 '[]'",
    #                 "7 0.250 10 '[5, 15, 25]' 1 '[]'", "7 0.250 10 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.250 10 '[5, 15, 25]' 10 '[]'",
    #                 "7 0.250 20 '[5, 15, 25]' 1 '[]'", "7 0.250 20 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.250 20 '[5, 15, 25]' 10 '[]'",
    #                 "7 0.250 50 '[5, 15, 25]' 1 '[]'", "7 0.250 50 '[5, 15, 25]' 5 '[]'",
    #                 "7 0.250 50 '[5, 15, 25]' 10 '[]'"]
    # run_settings = ["7 0.50 20 '[]' 10 '[5, 0.5, 0.8, 0.4]'"]

    # make a call to mainGA.py for each set of settings above
    for settings in run_settings:
        print ('\nSettings for this run: ' + settings)
        gensNear = []
        gensSuccess = []
        numgens = []
        fitnesses = []
        solutions = []
        indivs = []

        todays_date = datetime.fromtimestamp(time()).strftime('%Y-%m-%d')
        run_time = datetime.fromtimestamp(time()).strftime('%H-%M-%S')

        # create directories for logging if they don't already exist
        if not os.path.exists('logs/{}'.format(todays_date)):
            os.makedirs('logs/{}'.format(todays_date))
        if not os.path.exists('logs/{}/{}'.format(todays_date, run_time + '-' + str(os.getpid()))):
            os.makedirs('logs/{}/{}'.format(todays_date, run_time + '-' + str(os.getpid())))

        filepath = 'logs/{}/{}'.format(todays_date, run_time + '-' + str(os.getpid()))

        # create the file for pickling the constants and points in mainGA.py
        # used for logging
        # file is automatically removed at end of this function
        if not os.path.exists(filepath + '/params.pickle'):
            params_file = open(filepath + '/params.pickle', 'w')
            params_file.close()
        else:
            print('Error - pickle file for parameters already exists.')
            return

        if sys.version_info[0] < 3:
            py_ver = "python"
        else:
            py_ver = "python3"

        # -s flag is for the settings being sent -- see above
        if len(settings) > 0:
            command = py_ver + " mainGA.py --subprocess -p " + fname + " -f " + filepath + " -s " + settings
        else:
            command = py_ver + " mainGA.py --subprocess -p " + fname + " -f " + filepath

        for i in range(iterations):
            process = pexpect.spawn(command)
            process.expect("Enter the number of generations to iterate through: ", timeout=60)
            process.sendline(gens)
            #process.expect("Enter the number of generations to iterate through: ")
            #process.sendline("quit")
            process.expect("Process Finished", timeout=300)
            # data = (process.before).decode(sys.stdout.encoding)
            # data = data.split()

            print("\nIteration " + str(i+1) + " Complete!")
            returns_file = open(filepath + '/returns_file.pickle', 'rb')
            data = pickle.load(returns_file)
            returns_file.close()
            if data[1] == '0.0':
                print("Best fitness: 0.0 [Perfect!]")
            else:
                print("Best fitness: " + str(data[1]))
            print("Best member: " + data[4])
            print("Generations to produce: " + str(data[2]))
            print("Number of unique solutions: " + str(data[3]))
            if data[1] <= 5.:
                gensNear.append(data[2])
            if data[1] == 0.:
                gensSuccess.append(data[2])
            numgens.append(data[2])
            fitnesses.append(data[1])
            solutions.append(data[3])
            indivs.append(data[4])

            # read unique solutions from pickle file created in mainGA
            os.rename(filepath + '/solns.pickle', filepath + '/Run' + str(i))
            # solns_file = open('solns.pickle', 'rb')
            # solution_set = pickle.load(solns_file)
            # solns_file.close()
            # os.remove('solns.pickle')

            # create text file to store all unique solutions for this run
            # run_file = open('logs/{}/{}/{}.txt'.format(todays_date, run_time, 'Run' + str(i)), 'w')
            # for soln in solution_set:
            #     for i in soln:
            #         run_file.write(str(float(int(i, 2))))
            #         run_file.write('  ')
            #     run_file.write('\n')
            # run_file.close()

        # open the logging pickle file for reading
        # read the constants and points
        params_file = open(filepath + '/params.pickle', 'rb')
        consts = pickle.load(params_file)
        params_file.close()
        # points = pickle.load(params_file)

        avg_fit = np.mean(fitnesses)
        avg_gens = np.mean(numgens)
        avg_solns = np.mean(solutions)
        trim_avg_fit = stats.trim_mean(fitnesses, 0.05, axis=None)

        # write constants, generations, points, and data from each run to the csv file
        with open('logs/{}/{}/{}.csv'.format(todays_date, run_time + '-' + str(os.getpid()), run_time), 'a') as csv_file:
            if sys.version_info[0] < 3:
                csv_file.write(unicode(', Points file: ' + fname + '\n\n'))
                csv_file.write(unicode(',' + str(consts) + '\n\n'))
                csv_file.write(unicode(',' + str(gens) + '\n\n'))
                # csv_file.write(',' + str(points) + '\n\n')
                csv_file.write(unicode(', Avg fitness: {}  Trim fit: {}  Avg gens: {}  Avg solns: {}\n\n'.format(avg_fit, trim_avg_fit, avg_gens, avg_solns)))
                for i in range(len(solutions)):
                    csv_file.write(unicode(',{0:.3f},{1},{2},{3}\n'.format(float(fitnesses[i]), numgens[i], solutions[i], indivs[i])))
            else:
                csv_file.write(', Points file: ' + fname + '\n\n')
                csv_file.write(',' + str(consts) + '\n\n')
                csv_file.write(',' + str(gens) + '\n\n')
                # csv_file.write(',' + str(points) + '\n\n')
                csv_file.write(', Avg fitness: {}  Trim fit: {}  Avg gens: {}  Avg solns: {}\n\n'.format(avg_fit, trim_avg_fit, avg_gens, avg_solns))
                for i in range(len(solutions)):
                    csv_file.write(',{0:.3f},{1},{2},{3}\n'.format(float(fitnesses[i]), numgens[i], solutions[i], indivs[i]))

        if len(gensNear) > 0:
            avgNear = reduce(lambda x, y: x + y, gensNear) / float(len(gensNear))
        else:
            avgNear = "No near successes"

        if len(gensSuccess) > 0:
            avgSuccess = reduce(lambda x, y: x + y, gensSuccess) / float(len(gensSuccess))
        else:
            avgSuccess = "No perfect successes"

        # avgFitness = fitnesses = reduce(lambda x, y: x + y, fitnesses) / float(len(fitnesses))
        # avgSolutions = np.mean(solutions)

        print("\n\nAverage fitness across all iterations: " + str(avg_fit))
        print("\nAverage generations across all iterations: " + str(avg_gens))
        print("\nAverage number of unique solutions: " + str(avg_solns))
        print("\nNear success rate: " + str((len(gensNear) / iterations) * 100) + "%")
        print("Average generations for near success: " + str(avgNear))
        print("\nPerfect optimization rate: " + str((len(gensSuccess) / iterations) * 100) + "%")
        print("Average generations for perfect success: " + str(avgSuccess))

        # delete the pickle file used for logging
        if os.path.exists(filepath + '/params.pickle'):
            os.remove(filepath + '/params.pickle')

        if os.path.exists(filepath + '/returns_file.pickle'):
            os.remove(filepath + '/returns_file.pickle')

if __name__ == '__main__':
    main()

