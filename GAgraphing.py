#NOTE: in order to run this, you need the most up to date version of ggplot
#Unfortunately, pip may give you the wrong version
#if this happens, run the "ggplotFix.py" script included with this

from ggplot import *
import pandas as pd
import random
import math
import copy
import argparse
import pickle
import matplotlib
matplotlib.interactive(True)

LINE_STEP = 0.1

#range function that support floats
def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


def convert_to_df(points, cols = ['x', 'y']):
    newPoints = copy.deepcopy(points)

    for i in range(len(newPoints)):
        newPoints[i] = (i, [newPoints[i][0], newPoints[i][1]])

    newDF = pd.DataFrame.from_items(newPoints, orient='index', columns=cols)
    
    return newDF

def generate_line(vals, points):
    start_x = points[0][0]
    stop_x = points[-1][0]

    line_points = []
 
    #mas = [0, 0, 0, 0, 0, 0, 0]
    mas = [0, 1, 1, 0, 0, 0, 0]

    j = 0
    for i in range(len(mas)):
        if (i+len(vals)) >= len(mas):
            mas[i] = vals[j]
            j += 1

    #modify code here to use mas[] values

    #mas[3] = (mas[3] / (2**6))*10


    for i in frange(start_x, stop_x, LINE_STEP):
        #y = mas[0]*(i**4) + mas[1]*(i**3) + mas[2]*(i**2) + mas[3]*(i) + \
        #    mas[4]*math.sin(i) + mas[5]*math.cos(i) + mas[6]
        
        y = mas[0]*(i**2) + mas[3]*(i) + mas[4]*math.sin(mas[1]*i) + mas[5]*math.cos(mas[2]*i) + mas[6]
        line_points.append((i, y))

    return line_points

def graph_pop(points, population):
    pointsDF = convert_to_df(points)

    #converting each individual's curve into a set of datapoints to be graphed
    popDFs = []
    for indiv in population:
        indVals = indiv.get_values()
        indLine = generate_line(indVals, points)
        indDF = convert_to_df(indLine)
        popDFs.append(indDF)

    #this will add each line onto the plot
    #lines that are not the best fit are less opaque than the best fit line
    plot = ggplot(aes(x='x', y='y'), data=pointsDF) + geom_point(color='blue')
    for i in range(len(popDFs)):
        alph = 0.05
        if i == 0:
            alph=1.0
            plot = plot + geom_line(aes(x='x', y='y'), data=popDFs[i], color = 'red', alpha=alph, size=4)

        else:
            plot = plot + geom_line(aes(x='x', y='y'), data=popDFs[i], color = 'black', alpha=alph)

    start = points[0]
    stop = points[-1]
    
    plot = plot + scale_x_continuous(limits=(pointsDF['x'].min(), pointsDF['x'].max())) + \
        scale_y_continuous(limits=(pointsDF['y'].min(), pointsDF['y'].max()))

    #plot = plot + scale_x_continuous(limits=(start[0], stop[0])) + \
    #        scale_y_continuous(limits=(start[1], stop[1]))
    #this brings up the plot
    plot.show()

def graph_avgs(data):
    pointsDF = convert_to_df(data, ['Generation', 'Average Fitness'])
    plot = ggplot(aes(x='Generation', y='Average Fitness'), data=pointsDF) + geom_point(color='blue') + geom_line(color='black')

    plot = plot + scale_x_continuous(limits=(pointsDF['Generation'].min(), pointsDF['Generation'].max())) + \
        scale_y_continuous(limits=(pointsDF['Average Fitness'].min(), pointsDF['Average Fitness'].max()))
    plot.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='name of pickle file to read in with data to graph')
    #parser.add_argument('-p', '--points', help='[Flag] Add this flag to only plot points, remove it to also plot a population',
    #                    action='store_true')

    args = parser.parse_args()
    filepath = args.file
    #points_only = args.points
    
    data = pickle.load(open(filepath, 'rb'))

    pointsDF = convert_to_df(data)
    plot = ggplot(aes(x='x', y='y'), data=pointsDF) + geom_point(color='blue')

    plot = plot + scale_x_continuous(limits=(pointsDF['x'].min(), pointsDF['x'].max())) + \
        scale_y_continuous(limits=(pointsDF['y'].min(), pointsDF['y'].max()))
    plot.show()
    input("Press enter:")
    