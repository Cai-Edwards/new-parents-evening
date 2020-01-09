from initialise_algorithms import *
from analysis import *
from output import *
from database import *
from dict_manipulation import *
from adaptive_algorithms import *

db = connection("pe")

clear_slots(db)

algo = (first_fit(db, "t", order_by_length(get_appointments(db, "p"), True)))

visualise(analysis(algo))



print("hi")