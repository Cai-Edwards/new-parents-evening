from initialise_algorithms import *
from analysis import *
from database import *
from dict_manipulation import *
import json

def check(db, algorithm):

    first = (("t", "p"), ("p", "t"))
    order = (True, False)

    values = {}

    for option in first:

        for o in order:

            clear_slots(db)

            appointments = order_by_longest(get_appointments(db, option[1]), o)
            result = algorithm(db, option[0], appointments)
            values[option[0] + str(o)] = dict_to_str(analysis(result))
    
    return values


db = connection("pe")

algos = [first_fit, skip_few, first_few, shake_first_fit, ordered, variable_first_fit]

values = {}

txt = ["first_fit", "skip_few", "first_few", "shake_first_fit", "ordered", "variable_first_fit"]

for i, algo in enumerate(txt):
    values[algo] = check(db, algos[i])

with open("init_analysis.json", "w") as file:
    json.dump(values, file, ensure_ascii=False, indent=2)

print("hi")