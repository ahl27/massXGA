import pickle
import argparse
import math
import re
import random
random.seed()

def get_y(dct, x, sp, cp):
    y = 0

    if 'linear' in dct:
        y += dct['linear'] * x
    if 'quadratic' in dct:
        y += dct['quadratic'] * (x**2)
    if 'sin' in dct:
        y += dct['sin'] * math.sin(sp * x)
    if 'cos' in dct:
        y += dct['cos'] * math.cos(cp * x)
    if 'constant' in dct:
        y += dct['constant']

    return y


def main():
    #argument parser
    parser = argparse.ArgumentParser(description = 'generate points that match a well-defined graph for GA function optimizer.')
    parser.add_argument('type', nargs='*',
        help='type of graph to generate. Supported inputs: custom, linear, quadratic, sin, cos, constant. ' + \
        'If multiple inputs are received, graph will be a combination. \nDefault is custom.', default='custom')
    parser.add_argument('-m', '--slopes', nargs='*', 
        help='constants to use with the equation generating the line. Use "?" for random integers.' + \
        '\nDefault is a random integer in the range [-25, 25] for all values.')
    parser.add_argument('-sp', '--sinperiod', default=1, type=int, help='value of "a" in f(x) = sin(ax)')
    parser.add_argument('-cp', '--cosperiod', default=1, type=int, help='value of "a" in f(x) = cos(ax)')
    parser.add_argument('-start', '--startval', default=-50, type=int, help='x value of first point to generate. Default: -50')
    parser.add_argument('-end', '--endval', default=50, type=int, help='x value of last point to generate. Default: 50')

    #reading in commandline args
    args = parser.parse_args()

    types = args.type
    slopes = args.slopes
    cp = args.cosperiod
    sp = args.sinperiod
    cur = args.startval
    max_val = args.endval
    points = []

    if slopes is None:
        slopes = []

    #some warning messages
    if 'custom' in types and len(slopes) > 0:
        print('Warning: slopes provided but the "custom" input type is being used. Slopes will be ignored.')

    elif len(slopes) > len(types):
        cont = input('Warning: more slopes provided than types provided. Program will not use last ' + \
            str(len(slopes) - len(types)) + ' values. Continue? (y/n): ')

        cont = cont.lower()

        #ensure we have valid input
        while cont != 'y' and cont != 'n':
            cont = (input('Continue? (y/n): ').lower())
        
        #quit
        if cont == 'n':
            return
    
    elif len(types) > len(slopes):
        print('Warning: Fewer slopes than types received. Program will randomly generate remaining values.')

    #fill in random numbers and convert strings to ints
    for i in range(len(slopes)):
        if slopes[i] == '?':
            slopes[i] = random.randint(-25, 25)
        else:
            slopes[i] = int(slopes[i])

    while len(slopes) < len(types):
        slopes.append(random.randint(-25, 25))

    #no custom read in
    if 'custom' not in types:
        dictionary = dict(zip(types, slopes))
        done = False
        while not done:
            if cur >= max_val:
                cur = max_val
                done = True
            points.append((cur, get_y(dictionary, cur, sp, cp)))
            cur += random.randint(1, 5)


    #custom read in
    else:
        read_from_file = ''
        while read_from_file != 'y' and read_from_file != 'n':
            read_from_file = input("Do you want to read from a text file? (y/n): ")

        if read_from_file == 'y':
            print("Expected file format a text file space separated values of (x, y).")
            print("Alternatively, file can contain a series of space separated numbers.")
            print("Files in this format will read in every pair of numbers as a point.\n")
            fname = input("Enter name of txt file to read in: ")

            with open(fname, 'r') as infile:
                data = infile.read()

            #everyone loves regexes :P
            #this regex will convert the string to space separated numbers, 
            #then splits it into a list of integers
            data = ((re.sub(r' *, *|[)] *[(]|[()]', ' ', data)).strip()).split()

            #add points to the points list
            for i in range(len(data))/2:
                points.append((int(data[2*i]), int(data[2*i+1])))

        else:
            print('Enter space separated numbers corresponding to the x and y values of each point.')
            print('Enter "delete" to delete the previous entry, "print" to print current entries,')
            print('"help" to print this message, and "quit" when you are finished entering points.\n')

            done = ''

            while done != 'quit':
                done = input('')
                done = done.lower()

                if done == 'help':
                    print('Enter space separated numbers corresponding to the x and y values of each point.')
                    print('Enter "delete" to delete the previous entry, "print" to print current entries,')
                    print('"help" to print this message, and "quit" when you are finished entering points.\n')
                elif done == 'print':
                    for entry in points:
                        print(entry)
                elif done == 'quit':
                    continue
                elif done == 'delete':
                    print('Removed value ', end='')
                    print(points.pop(-1))
                else:
                    x, y = done.split()
                    try:
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        print("Error: invalid input. Please try again.")
                        continue
                    points.append((x,y))


    #generate filename
    fname = './points/'
    
    if 'custom' in types:
        fname = input('\nEnter name of file to save to: ')
    else:
        fname2 = '_'
        for key in sorted(dictionary.keys()):
            fname += key[0].upper()
            fname2 += str(dictionary[key]) + '_'
        if sp != 1:
            fname2 += 'sp' + str(sp) + '_'
        if cp != 1:
            fname2 += 'cp' + str(cp) + '_'

        fname2 = fname2[:-1]
        fname = fname + fname2

    pickle.dump(points, open(fname + '.pickle', 'wb'))

            






if __name__ == '__main__':
    main()
