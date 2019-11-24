'''Initialisation algorithms'''

from database import *
from output import *
from list_manipulation import *

def first_fit(db, group, appointments, init=50, increase = 5):
    '''First fit algorithm. The opposite appointment data needs to be provided. Can be done to teachers or pupils'''

    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)] #Fills their ids with 0's

    for person in appointments:
        slots_taken = []

        for relationships in appointments[person]:
            slot = 0

            while True:

                if len(timetable[relationships]) <= slot:
                    timetable[relationships].extend([0,] * increase)

                if timetable[relationships][slot] == 0 and slot not in slots_taken:
                    timetable[relationships][slot] = person
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
                    slot = (num + value) % skip_amount
                    value += 1

                    if slot == start:
                        timetable[relationships].extend([0,] * increase)

                if timetable[relationships][slot] == 0 and slot not in slots_taken:
                    timetable[relationships][slot] = person
                    slots_taken.append(slot)
                    break
                
                else:
                    slot += skip_amount

    return remove_excess(timetable)

def first_few(db, group, appointments, init=30, increment=5, increase=3):
    '''Selects the first x needed, then the next x...'''

    timetable = {}

    slots_taken = {x:[] for x in appointments}
    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)]

    not_full = True
    current = 0

    while not_full == True:

        for person in appointments:

            if len(appointments[person][current:current+increment]) == 0:
                not_full = False
                pass
            else:
                not_full = True

                for relationships in appointments[person][current:current+increment]:
                    slot = 0

                    while True:
                        if slot >= len(timetable[relationships]):
                            timetable[relationships].extend([0,]*increase)

                        if timetable[relationships][slot] == 0 and slot not in slots_taken[person]:
                            timetable[relationships][slot] = person
                            slots_taken[person].append(slot)
                            break
                        
                        else:
                            slot += 1

        
        current += increment

    return remove_excess(timetable)

    
