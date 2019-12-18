import csv
import matplotlib.pyplot as plt
from list_manipulation import dictToList

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
            fig = plt.figure()

            ax = fig.add_subplot()
            ax.set_title(point)
            ax.plot(analysis[point])
    
    plt.show()

