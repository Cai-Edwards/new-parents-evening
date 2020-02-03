'''Initialisation algorithms'''

from database import get_ids
from dict_manipulation import find_available
from list_manipulation import remove_excess
from random import randint, choice

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


    while len(appointments) != 0:

        to_remove = []
        for person in appointments:

            look = appointments[person][0:increment]

            for relationships in look:
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

            del appointments[person][0:increment]

            if len(appointments[person]) == 0:
                to_remove.append(person)
        
        if len(to_remove) != 0:
            for i in to_remove:
                del appointments[i]    

    return remove_excess(timetable)

def shake_first_fit(db, group, appointments, init=50, increase = 5):
    '''First fit but shaking'''

    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)] #Fills their ids with 0's

    num = 0
    for person in appointments:
        slots_taken = []
        num += 1

        for relationships in appointments[person]:
            if num % 2 == 0:
                slot = 0

                while True:
                    if slot >= len(timetable[relationships]):
                        timetable[relationships].extend([0,]*increase)
                    
                    if timetable[relationships][slot] == 0 and slot not in slots_taken:
                        timetable[relationships][slot] = person
                        slots_taken.append(slot)
                        break

                    else:
                        slot += 1

            else:
                slot = len(timetable[relationships])-1
                while True:
                    
                    if slot < 0:
                        timetable[relationships].extend([0,]*increase)
                        slot = len(timetable[relationships])-1
                    
                    if timetable[relationships][slot] == 0 and slot not in slots_taken:
                        timetable[relationships][slot] = person
                        slots_taken.append(slot)
                        break

                    else:
                        slot -= 1

    return remove_excess(timetable)

def variable_first_fit(db, group, appointments, init=50, increase = 5):
    '''First fit starting at random positions'''
    
    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)] #Fills their ids with 0's

    for person in appointments:
        slots_taken = []

        init = randint(0, len(appointments[person]))

        for relationships in appointments[person]:
            slot = init

            if slot >= len(timetable[relationships]):
                slot = len(timetable[relationships])
                init = slot

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

def randomise(db, group, appointments, init=110, increase=5):
    '''Assigns each appoitments into a randomly available slot'''

    timetable = {}
    slots_taken = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)] #Fills their ids with 0's

    for person in appointments:
        
        slots_taken[person] = []

        for relationships in appointments[person]:

            ava_slots = [slot for slot, value in enumerate(timetable[relationships]) if value == 0 and slot not in slots_taken[person]]

            while len(ava_slots) == 0:
                timetable[relationships].extend([0,]*increase)
                ava_slots = [slot for slot, value in enumerate(timetable[relationships]) if value == 0 and slot not in slots_taken[person]]

            slot = choice(ava_slots)

            slots_taken[person].append(slot)
            timetable[relationships][slot] = person

    return remove_excess(timetable)

def minimum_gaps(db, group, appointments, init=200):
    '''Assumes infinite time'''

    slots_taken = {}
    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)]

    for person in appointments:

        ava = find_available(appointments[person])

        for i in ava:
            temp = {}

            if i[1] - i[0] > len(appointments[person]):

                for k, other in enumerate(appointments[person]):

                    if slots_taken[other][i[0]+k] != 0:
                        
                        while found := False:
                            pass



    return remove_excess(timetable)
