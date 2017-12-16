import pexpect
import argparse
import sys
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
    fitnesses = []


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
        if float(data[1]) <= 5.:
            gensNear.append(int(data[2]))
        if float(data[1]) == 0.:
            gensSuccess.append(int(data[2]))
        fitnesses.append(float(data[1]))
    
    if len(gensNear) > 0:
        avgNear = reduce(lambda x, y: x + y, gensNear) / float(len(gensNear)) 
    else:
        avgNear = "No near successes"

    if len(gensSuccess) > 0:
        avgSuccess = reduce(lambda x, y: x + y, gensSuccess) / float(len(gensSuccess)) 
    else:
        avgSuccess = "No perfect successes" 

    avgFitness = fitnesses = reduce(lambda x, y: x + y, fitnesses) / float(len(fitnesses))

    print("\nAverage fitness across all iterations: " + str(avgFitness))
    print("\nNear success rate: " + str((len(gensNear) / iterations) * 100) + "%")
    print("Average generations for near success: " + str(avgNear))
    print("\nPerfect optimization rate: " + str((len(gensSuccess) / iterations) * 100) + "%")
    print("Average generations for perfect success: " + str(avgSuccess))
    

if __name__ == '__main__':
    main()

