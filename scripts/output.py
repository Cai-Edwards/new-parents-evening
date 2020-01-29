import csv
import matplotlib.pyplot as plt
from list_manipulation import dictToList
from scipy.stats import linregress #INPLEMENT BY SELF
from dict_manipulation import longest
import pygame
from random import randint

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

def draw_timetable(timetable):
    
    rows = longest(timetable) + 1
    columns = len(timetable) + 1
    
    pygame.init()

    d = pygame.display.set_mode((600, 300), pygame.RESIZABLE)
    pygame.display.set_caption("Timetable")

    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 125, 0)

    offset = 5

    while True:
        d.fill(black)

        w = d.get_width()
        h = d.get_height()

        cx = round(w/columns)
        cy = round(h/rows)

        for i, person in enumerate(timetable):
            for k, slot in enumerate(timetable[person]):
                    
                if k == 0 or i == 0:
                    pass
                elif slot != 0:
                    pygame.draw.rect(d, green, (cx*(k), cy*(i), cx*(k+1), cy*(i+1)))

        for k in range(rows):
            pygame.draw.line(d, white, (cx*(k+1), 0), (cx*(k+1), h))
        for i in range(columns):
            pygame.draw.line(d, white, (0, cy*(i+1)), (w, cy*(i+1)))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.VIDEORESIZE:
                d = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)