from analysis import analysis
from dict_manipulation import shift_left, swap_any_columns, swap_existing_columns
from random import random
import numpy as np

def anneal(timetable, max_step):
    '''Simulated annealing'''

    old_score = analysis(timetable)['score']

    for i in range(1, max_step):
        T = i/max_step

        new = shift_left(swap_existing_columns(timetable))


        new_score = analysis(new)['score']

        if new_score < old_score:
            timetable = new
            old_score = new_score
        elif np.exp(-(new_score-old_score)/T) > random():
            timetable = new
            old_score = new_score

        print(new_score, old_score)

    return timetable

    


