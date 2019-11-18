'''Initialisation algorithms'''

from database import *
from output import *
from list_manipulation import *

def first_fit(db, group, appointments):
    '''First fit algorithm. The opposite appointment data needs to be provided. Can be done to teachers or pupils'''

    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(200)] #Fills their ids with 0's

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

def skip_few(db, group, appointments, skip_amount=2, init=20, increase=5):
    '''First fit, but only considers every n places.'''

    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)]
    
    num = 0

    for person in appointments:
        num += 1
        slots_taken = []

        start = num % skip_amount

        for relationships in appointments[person]:
            slot = start
            value = 1

            while True:
                if slot >= len(timetable[relationships]):
                    slot = (num+value) % skip_amount
                    value += 1

                    if slot == start:
                        timetable[relationships].extend([0,]*increase)

                if timetable[relationships][slot] == 0 and slot not in slots_taken:
                    timetable[relationships][slot] = person
                    slots_taken.append(slot)
                    break
                
                else:
                    slot += skip_amount

    return remove_excess(timetable)

def first_few():
    '''TODO'''