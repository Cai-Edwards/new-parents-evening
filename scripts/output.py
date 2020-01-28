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

            y = analysis[point]
            x = list(range(len(analysis[point])))
            
            ybar = sum(y)/len(y)
            xbar = sum(x)/len(x)

            ax[0].set_title(point)
            ax[1].set_title(point)

            ax[0].scatter(x, y)
            ax[1].hist(analysis[point], 30)

            sxy = sum((xv-xbar)*(yv - ybar) for xv, yv in zip(x, y))
            sxx = sum((xv-xbar)**2 for xv in x)
            syy = sum((yv-ybar)**2 for yv in y)

            b = sxy/sxx
            c = ybar - b * xbar

            ax[0].plot([0, max(x)], [c, b*max(x)+c])

    
    plt.show()
