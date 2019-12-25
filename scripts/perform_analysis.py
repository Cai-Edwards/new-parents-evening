from initialise_algorithms import *
from analysis import *
from database import *
from dict_manipulation import *

db = connection("pe")

algos = [first_fit, skip_few, first_few, shake_first_fit, ordered, variable_first_fit]

values = {}

txt = ["first_fit", "skip_few", "first_few", "shake_first_fit", "ordered", "variable_first_fit"]

for algo, text in zip(algos, txt):

    for p1, p2 in zip(["t", "p"], ["p", "t"]):

        for order in [True, False]:

            clear_slots(db)

            result = algo(db, p1, order_by_longest(get_appointments(db, p2), order))

            values[text + "_" + p1 + "_" + str(order)] = analysis(result)

print("hi")