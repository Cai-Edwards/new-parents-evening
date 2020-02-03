import csv
import matplotlib.pyplot as plt
from list_manipulation import dictToList
from dict_manipulation import longest
from random import randint
import os

def write(timetable, file):
    '''Write a timetable to a csv file
    
    timetable: dict
    file: filename/path'''

    timetable = dictToList(timetable)

    with open(file, "w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(timetable)
    
    return "Done"

def visualise(analysis, save = False, filepath=''):
    '''Visualise analysis of a timetable.
    Gives Minimum, Maximum, Mean and Standard deviation of each data point
    Writes all values, and plots the values for each data point as a scatter plot and histogram'''

    for point in analysis:

        if type(analysis[point]) is list and len(analysis[point]) == 4:
            if not(save):
                print("""
                {}:
                Mninimum: {}
                Maximum: {}
                Mean: {}
                Standard Deviation: {}

                """.format(point, *analysis[point]))
            else:
                with open(os.path.normpath(filepath + "/data.txt"), "a") as file:
                    file.write("""
                {}:
                Mninimum: {}
                Maximum: {}
                Mean: {}
                Standard Deviation: {}

                """.format(point, *analysis[point]))
        
        elif type(analysis[point]) is list and len(analysis[point]) > 4:
            fig, ax = plt.subplots(2)

            y = analysis[point]
            x = list(range(len(analysis[point])))
            
            ybar = sum(y)/len(y)
            xbar = sum(x)/len(x)

            sxy = sum((xv-xbar)*(yv - ybar) for xv, yv in zip(x, y))
            sxx = sum((xv-xbar)**2 for xv in x)
            #syy = sum((yv-ybar)**2 for yv in y)

            b = sxy/sxx
            c = ybar - b * xbar
        
            ax[0].set_title(point)
            ax[1].set_title(point)

            ax[0].scatter(x, y)
            ax[1].hist(analysis[point], 30)

            ax[0].plot([0, max(x)], [c, b*max(x)+c])

            if save:
                plt.savefig(os.path.normpath(filepath + "/" + point))

    if not(save):
        plt.show()