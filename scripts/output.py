import csv
import matplotlib.pyplot as plt
from list_manipulation import dictToList
from scipy.stats import linregress #INPLEMENT BY SELF

def write(timetable, file):
    '''Write a timetable to a csv file
    
    timetable: dict
    file: filename/path'''

    timetable = dictToList(timetable)

    with open(file, "w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(timetable)
    
    return "Done"

def visualise(analysis):
    '''Visualise analysis of a timetable.
    Gives Minimum, Maximum, Mean and Standard deviation of each data point
    Writes all values, and plots the values for each data point as a scatter plot and histogram'''

    for point in analysis:

        if type(analysis[point]) is list and len(analysis[point]) == 4:
            print("""
            {}:
            Mninimum: {}
            Maximum: {}
            Mean: {}
            Standard Deviation: {}

            """.format(point, *analysis[point]))
        
        elif type(analysis[point]) is list and len(analysis[point]) > 4:
            fig, ax = plt.subplots(2)

            ax[0].set_title(point)
            ax[1].set_title(point)

            ax[0].scatter(range(len(analysis[point])), analysis[point])
            ax[1].hist(analysis[point], 30)

            m, c, r, p, s = linregress(range(len(analysis[point])), analysis[point])


            #m, c = lobf(analysis[point])
            y = [(m * (x+1)) + c for x, t in enumerate(analysis[point])]

            ax[0].plot(y)
    
    plt.show()

def lobf(ydata):
    '''Least square method - doesn't work'''

    n = len(ydata)
    xdata = [x for x in range(n)]

    xbar = sum(xdata)/n
    ybar = sum(ydata)/n

    m = sum([int((xdata[i]-xbar) * (ydata[i]-ybar)) for i, t in enumerate(range(n))])
    c = ybar - m * xbar

    return m, c