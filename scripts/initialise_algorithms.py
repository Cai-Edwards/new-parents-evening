'''Initialisation algorithms'''

from database import *
from output import *
from list_manipulation import *
from random import randint

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

def ordered(db, group, appointments, init=50, increase = 5, longest=True):
    '''Order by longest/shortest pupil and teacher'''  

    longest_person = {x:appointments[x] for x in sorted(appointments, key=lambda x: len(appointments[x]), reverse=longest)}

    cursor = db.cursor()

    q1 = "SELECT {}, count({}) from relationships group by {} order by COUNT({}) DESC" 

    if group[0].lower() == "p":
        cursor.execute(q1.format("pid", "tid", "pid", "tid"))
    elif group[0].lower() == "t":
        cursor.execute(q1.format("tid", "pid", "tid", "pid"))
    else:
        return "Not a valid input"
    
    lengths = dict(cursor.fetchall())

    for person in longest_person:
        values = [(ids, lengths[ids]) for ids in longest_person[person]]
        longest_person[person] = [x[0] for x in sorted(values, key=lambda k: k[1], reverse=longest)]

    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)] #Fills their ids with 0's

    for person in longest_person:
        slots_taken = []

        for relationships in longest_person[person]:
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
