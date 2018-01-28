#Class to hold members of population
import math

class individual():
    
    #normal initialization
    def __init__(self, initList):
        self.values = initList
        self.smoosher = 1

    #splits a single bitstring into its individual parts
    def set_bitstring(self, bitstring):
        #we know all values must have the same length
        length = len(bitstring)
        num_vars = len(self.values)

        newList = []
        section = int(length/num_vars)
        for i in range(num_vars):
            newList.append(bitstring[i*section : (1+i)*section])

        self.values = newList

    #returns the bitstring for the individual
    def get_bitstring(self):
        return ''.join(self.values)

    #returns the list of bitstrings corresponding to individual values
    def get_value_list(self):
        return self.values

    #returns a list of integers corresponding to individual values
    def get_values(self):
        vals = []
        
        #converting from two's complement binary to integer
        for i in range(len(self.values)):
            if self.values[i][0] == '1':
                vals.append((2**(len(self.values[i])-1) - int(self.values[i][1:], 2)) * (-1))
                
            else:
                vals.append(int(self.values[i][1:], 2))

        return vals

    #calculates the fitness of the function by measuring squared error between graph and points
    def calculate_fitness(self, points):
        fitness = 0.
        vals = self.get_values()

        #master values
        #gx^4 + fx^3 + ex^2 + dx + csin(x) + bcos(x) + a
        #mas = [0, 0, 0, 0, 0, 0, 0]

        #different way with period evolution
        #ex^2 + dx + csin(gx) + bcos(fx) + a
        mas = [0, 1, 1, 0, 0, 0, 0]
        j = 0
        for i in range(len(mas)):
            if (i+len(vals)) >= len(mas):
                mas[i] = vals[j]
                j += 1

        #modify code here to use mas[] values

        #mas[3] = (mas[3] / (2**6))*10

        for point in points:
            x = point[0]
            obsY = point[1]
            
            #expY = mas[0]*(x**4) + mas[1]*(x**3) + mas[2]*(x**2) + mas[3]*(x) + \
            #        mas[4]*math.sin(x) + mas[5]*math.cos(x) + mas[6]
            
            expY = mas[0]*(x**2) + mas[3]*(x) + mas[4]*math.sin(mas[1] * x) + mas[5]*math.cos(mas[2] * x) + mas[6]
            #if testing:
                #print(str(obsY) + ' ' + str(expY))

            #right now using mean squared error
            fitness += (expY - obsY)**2
        fitness = fitness/len(points)
        return fitness