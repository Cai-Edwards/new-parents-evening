import random

def dict_shuffle(dictionary):
    '''Randomly shuffles the dictionary order'''
    new = list(dictionary.items())
    random.shuffle(new)
    return dict(new)

def dict_to_str(dictionary):
    for x in dictionary:
        dictionary[x] = str(dictionary[x])
    return dictionary

def order_by_double(db, group, appointments, longest=True):

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

def longest(timetable):
    return max([len(timetable[x]) for x in timetable])

def shortest(timetable):
    return min([len(timetable[x]) for x in timetable])

def expand(timetable):

    longe = longest(timetable)

    for person in timetable:
        timetable[person].extend([0,]*(longe-len(timetable[person])))

    return timetable

def swap_any_columns(timetable):

    timetable = expand(timetable)
    longe = longest(timetable)

    col1, col2 = random.sample(range(longe), 2)

    for person in timetable:
        timetable[person][col1], timetable[person][col2] = timetable[person][col2], timetable[person][col1]
    
    return timetable

def swap_existing_columns(timetable):

    timetable = expand(timetable)
    short = shortest(timetable)

    col1, col2 = random.sample(range(short), 2)

    for person in timetable:
        timetable[person][col1], timetable[person][col2] = timetable[person][col2], timetable[person][col1]
    
    return timetable

def shift_left(timetable, number=1):

    for _ in range(number):
        for person in timetable:
            for slot, x in enumerate(timetable[person]):
                if slot-1 < 0:
                    break
                elif timetable[person][slot-1] != 0:
                    break
                elif x in [timetable[p][slot-1] for p in timetable if p != person]:
                    break

                timetable[person][slot-1] = x

    return timetable