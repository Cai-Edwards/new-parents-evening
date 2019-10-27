from initialise_algorithms import *
from analysis import *
from output import *
from database import *
from dict_manipulation import *

db = connection("pe")

visualise(analyse(first_fit(db, "p", order_by_longest(get_appointments(db, "p"), True))))

print("hi")