import csv

def dictToList(dict):
    return [dict[x] for x in dict]

def write(timetable, file):

    timetable = dictToList(timetable)

    with open(file, "w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(timetable)
    
    return "Done"

