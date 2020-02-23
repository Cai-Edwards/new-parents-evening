'''Initialisation algorithms'''

from database import get_ids
from dict_manipulation import find_available
from list_manipulation import remove_excess
from random import randint, choice

def first_fit(db, group, appointments, init=50, increase = 5):
    '''First fit algorithm. The opposite appointment data needs to be provided. Can be done to teachers or pupils'''

    #Initialising where the timetable will be stored
    timetable = {}

    #Creating keys with the people's ids and filling their list with 0's
    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)] #Fills their ids with 0's

    #Loop over the people that need to be assigned appointments
    for person in appointments:
        slots_taken = []

        #Loop over who they need to see.
        for relationships in appointments[person]:
            slot = 0

            #Find available slot
            while True:

                #Check if the list is long enough
                if len(timetable[relationships]) <= slot:
                    timetable[relationships].extend([0,] * increase)

                #Checking if the slot is available
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

    #For person that needs a schedule
    for person in appointments:
        num += 1
        slots_taken = []

        #Set starting position
        start = num % skip_amount

        #Looping over whoever they need to see
        for relationships in appointments[person]:
            slot = start
            value = 1

            while True:

                #If slot is greater than the length of the list, go back and try the ones that were skipped
                if slot >= len(timetable[relationships]):
                    slot = (num + value) % skip_amount
                    value += 1

                    #If there is absolutely no space, then extend the list.
                    if slot == start:
                        timetable[relationships].extend([0,] * increase)

                if timetable[relationships][slot] == 0 and slot not in slots_taken:
                    timetable[relationships][slot] = person
                    slots_taken.append(slot)
                    break
                
                else:
                    #Go to the next slot we want to check
                    slot += skip_amount

    return remove_excess(timetable)

def first_few(db, group, appointments, init=30, increment=5, increase=3):
    '''Selects the first x needed, then the next x...'''

    timetable = {}

    slots_taken = {x:[] for x in appointments}
    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)]

    #While there are still appointments to assign
    while len(appointments) != 0:

        to_remove = []
        
        #For person that needs a schedule
        for person in appointments:

            #Get the appointments we need to look at.
            look = appointments[person][0:increment]

            #Loop over these appointments and try to assign them a slot
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

            #Remove these appointments from the while list.
            del appointments[person][0:increment]

            #If the person we are looking at has no more appoinments to assign, then add the id to to_remove
            if len(appointments[person]) == 0:
                to_remove.append(person)
        
        #If there is someone in to_remove, remove them from appointments.
        if len(to_remove) != 0:
            for i in to_remove:
                del appointments[i]    

    return remove_excess(timetable)

def shake_first_fit(db, group, appointments, init=50, increase = 5):
    '''First fit but assign forward, then backwards'''

    timetable = {}

    for person in get_ids(db, group[0].lower()):
        timetable[person] = [0 for x in range(init)] #Fills their ids with 0's

    num = 0
    for person in appointments:
        slots_taken = []
        num += 1

        for relationships in appointments[person]:
            
            #If person is even-numbered
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

            #If person is off numbered
            else:
                
                #slot becomes the last index of the list.
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

        #Start at a random position
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

    #Loop over who needs a schedule
    for person in appointments:
        
        #Initialise slots taken keys.
        slots_taken[person] = []

        #Loop over appointments
        for relationships in appointments[person]:

            #Get the available slots we can place the appointment in
            ava_slots = [slot for slot, value in enumerate(timetable[relationships]) if value == 0 and slot not in slots_taken[person]]

            #If there are no available slots, extend the list and re-check the slots.
            while len(ava_slots) == 0:
                timetable[relationships].extend([0,]*increase)
                ava_slots = [slot for slot, value in enumerate(timetable[relationships]) if value == 0 and slot not in slots_taken[person]]

            #Select a random slot
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
