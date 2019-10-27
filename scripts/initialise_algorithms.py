'''Initialisation algorithms'''

from database import *
from output import *
from list_manipulation import *

def first_fit(db, group, appointments):
    '''First fit algorithm. The appointment data needs to be provided. Can be done to teachers or pupils
    
    Returns the opposite groups timetable
    '''

    timetable = {}

    for person in get_ids(db, (lambda x: "p" if x == "t" else "t")(group[0].lower())): #Gets the ids for the opposite status given. Pid --> Tid
        timetable[person] = [0 for x in range(100)] #Fills their ids with 0's

    for i in appointments:

        slots_taken = []
        slot = 0

        for x in appointments[i]:
            while True:

                if timetable[x][slot] == 0 and slot not in slots_taken:
                    timetable[x][slot] = i
                    slots_taken.append(slot)
                    break

                else:
                    slot += 1

    return remove_excess(timetable)


