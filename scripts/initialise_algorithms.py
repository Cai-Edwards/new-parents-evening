from database import *
from output import *


def remove_excess(timetable):
    for i in timetable:
        try:
            index = timetable[i].index(next(filter(lambda x: x != 0, timetable[i][::-1]))) + 1
        except:
            index = None

        timetable[i] = timetable[i][:index]

    return timetable

def first_fit(db, group):

    appointments = get_appointments(db, group)

    timetable = {}

    for person in get_ids(db, (lambda x: "p" if x == "t" else "t")(group[0].lower())):
        timetable[person] = [0 for x in range(100)]

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


write(first_fit(connection("pe"), "t"), "output.csv")
