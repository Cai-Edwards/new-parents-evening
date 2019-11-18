from initialise_algorithms import *
from analysis import *
from output import *
from database import *
from dict_manipulation import *

db = connection("pe")

algo = (first_few(db, "t", order_by_longest(get_appointments(db, "p"))))


update_slots(db, algo, "tid")
visualise(analyse(db, algo))
write(algo, "f1.csv")
algo = swap(db, algo, "p")
visualise(analyse(db, algo))
write(algo, "f2.csv")



print("hi")