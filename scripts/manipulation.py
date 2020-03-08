import random
from database import get_ids

def dictToList(dict):
    return [dict[x] for x in dict]

def remove_excess(timetable):
    '''Removes all zeros at the end of a value for every key'''

    for i in timetable:
        try:
            index = timetable[i].index(next(filter(lambda x: x != 0, timetable[i][::-1]))) + 1 #Find the last non-zero digit
        except:
            index = None

        timetable[i] = timetable[i][:index]

    return timetable

def swap(db, timetable, group):
    '''Turns a timetable for teachers into a timetable for pupils or vice versa.
    
    timetable -- Dictionary\n
    group -- group to convert to
    '''
    new = {}

    for person in get_ids(db, group[0].lower()):
        new[person] = [0 for x in range(200)] #Fills their ids with 0's

    for original in timetable:
        slot = 0

        for other in timetable[original]:
            if other != 0:
                new[other][slot] = original
            
            slot += 1
    
    return remove_excess(new)

def convert_to_slots(timetable):
    '''Takes a timetable and converts all appointments into slot times.
    
    This will forget who the appointment is with.'''

    new = {}

    for person in timetable:
        new[person] = []

        slot = 1

        for time in timetable[person]:
            if time != 0:
                new[person].append(slot)
            
            slot += 1

    return new

def dict_shuffle(dictionary):
    '''Randomly shuffles the dictionary order'''
    new = list(dictionary.items())
    random.shuffle(new)
    return dict(new)

def dict_to_str(dictionary : str):
    '''Converts all values in a dictionary to str'''

    return {x:str(dictionary[x]) for x in dictionary}

def order_by_double(db, group, appointments, longest=True):
    '''Orders by the longest pupil and inside each pupil orders teachers by ammount of appointments
    or vice versa'''

    schedule = {x:appointments[x] for x in sorted(appointments, key=lambda x: len(appointments[x]), reverse=longest)}

    cursor = db.cursor()

    q1 = "SELECT {}, count({}) from relationships group by {} order by COUNT({}) DESC" 

    if group[0].lower() == "p":
        cursor.execute(q1.format("pid", "tid", "pid", "tid"))
    elif group[0].lower() == "t":
        cursor.execute(q1.format("tid", "pid", "tid", "pid"))
    else:
        return "Not a valid input"
    
    lengths = dict(cursor.fetchall())

    for person in schedule:
        values = [(ids, lengths[ids]) for ids in schedule[person]]
        schedule[person] = [x[0] for x in sorted(values, key=lambda k: k[1], reverse=longest)]
    
    return schedule

def order_by_length(d, longest=True):
    '''longest=False for ordering by shortest'''
    return {x:d[x] for x in sorted(d, key=lambda a: len(d[a]), reverse=longest)}

def validate(timetable):
    '''Checks if the timetable is valid'''

    uniq = []

    for person in timetable:
        occurences = []

        for app in timetable[person]:
            if app in occurences and app != 0:
                return False
            else:
                occurences.append(app)
    
        uniq.extend([x for x in occurences if x not in uniq and x != 0])

    for ids in uniq:

        indexs = []

        for person in timetable:
            if ids in timetable[person]:
                if timetable[person].index(ids) in indexs:
                    return False
                indexs.append(timetable[person].index(ids))

    return True

def find_available(d):
    '''Find available lengths of places.
    
    returns [[0, 2], [4, 10], [15, 20]] for example'''

    available = [x for x, i in enumerate(d) if (x == 0 or x == len(d)-1 or d[x-1] != i) and (i ==0 or d[x-1] == 0)]

    data = [[available[i], available[i+1]-1] for i in range(len(available)) if i % 2 == 0]

    if data[-1][-1]+1 == len(d)-1:
        data[-1][-1] = len(d)-1

    return data
    
def longest(timetable):
    return max((len(timetable[x]) for x in timetable))

def shortest(timetable):
    return min((len(timetable[x]) for x in timetable))
