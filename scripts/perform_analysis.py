from initialise_algorithms import first_few, first_fit, shake_first_fit, skip_few, randomise, variable_first_fit
from analysis import analysis
from database import connection, clear_slots, get_appointments
from manipulation import dict_to_str, order_by_double, order_by_length, swap
import json

def check(db, algorithm):
    '''Return all the data of all possibilities for a single algorithm'''

    first = (("teacher", "pupil"), ("pupil", "teacher"))
    sort_algos = (order_by_length, order_by_double)
    txt_sort = ("BaseSorted", "DoubleSorted")
    order = (True, False)

    values = {}

    for option in first:

        for i, sort in enumerate(sort_algos):

            for o in order:

                clear_slots(db)

                if sort == order_by_double:
                    appointments = sort(db, option[0], get_appointments(db, option[1]), longest=o)

                else:
                    appointments = sort(get_appointments(db, option[1]), longest=o)

                result = algorithm(db, option[0], appointments)

                if option[0] == "teacher":
                    values[txt_sort[i] + "TeachersFor" + option[0] + str(o)] = dict_to_str(analysis(result))
                    values[txt_sort[i] + "PupilsFor" + option[0] + str(o)] = dict_to_str(analysis(swap(db, result, "p")))
                else:
                    values[txt_sort[i] + "TeachersFor" + option[0] + str(o)] = dict_to_str(analysis(swap(db, result, "t")))
                    values[txt_sort[i] + "PupilsFor" + option[0] + str(o)] = dict_to_str(analysis(result))
    
    return values


db = connection("pe")

algos = [first_fit, skip_few, first_few, shake_first_fit, variable_first_fit, randomise]

values = {}

txt = ["first_fit", "skip_few", "first_few", "shake_first_fit", "variable_first_fit", "randomise"]

for i, algo in enumerate(txt):
    print("Generating data for:",algo)
    values[algo] = check(db, algos[i])

with open("init_analysis.json", "w") as file:
    json.dump(values, file, ensure_ascii=False, indent=4)

print("hi")