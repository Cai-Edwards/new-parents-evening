from initialise_algorithms import *
from analysis import *
from output import *
from database import *
from dict_manipulation import *

db = connection("pe")

clear_slots(db)

algo = (first_few(db, "t", order_by_longest(get_appointments(db, "p"), True)))

visualise(analysis(algo))



print("hi")