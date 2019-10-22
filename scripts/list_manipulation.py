'''List manipulations. eg) students --> teachers'''
from database import get_ids

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
        new[person] = [0 for x in range(100)] #Fills their ids with 0's

    for original in timetable:
        slot = 0

        for other in timetable[original]:
            if other != 0:
                new[other][slot] = original
            
            slot += 1
    
    return remove_excess(new)