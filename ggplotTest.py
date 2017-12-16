from ggplot import *
import pandas as pd
import random
import math

#range function that support floats
def frange(start, stop, step):
	i = start
	while i < stop:
		yield i
		i += step


def convert_to_df(points):
	newPoints = points
	for i in range(len(points)):
		newPoints[i] = (i, [points[i][0], points[i][1]])

	newDF = pd.DataFrame.from_items(points, orient='index', columns=['x', 'y'])
	
	return newDF

def generate_line(a, b, c, points):
	start_x = points[0][0]
	end_x = points[-1][0]

	line_points = []
	for i in frange(start_x, start_y, 0.1):
		y = a*(i*i) + b*(i) + c*math.sin(i)
		line_points.append((i, y))

	return line_points

def graph_pop(points, population):
	pointsDF = convert_to_df(points)

	#converting each individual's curve into a set of datapoints to be graphed
	popDFs = []
	for indiv in population:
		indVals = indiv.get_values()
		indLine = generate_line(indVals[0], indVals[1], indVals[2], points)
		indDF = convert_to_df(indLine)
		popDFs.append(indDF)

	#this will add each line onto the plot
	#lines that are not the best fit are less opaque than the best fit line
	plot = ggplot(aes(x='x', y='y'), data=pointsDF) + geom_point(color='red')
	for i in range(len(popDFs)):
		alph = 0.3
		if i = 0:
			alph=1.0

		plot = plot + geom_line(aes(x='x', y='y'), data=popDFs[i], alpha=alph)

	#this brings up the plot
	plot