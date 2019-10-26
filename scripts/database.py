'''All functions relating to accessing the databases'''
import mysql.connector

def connection(dataBase):
    '''Connect to the database entered'''

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database=dataBase
    )

    print("Connected")
    return db


def data_to_pe(db, yeargroup): 
    '''Takes the data from the data database and moves a yeargroup to the pe database.
    Year group from 6-13'''

    q = "insert into pe.relationships select p.pid, t.tid, t.classID, NULL from data.classteacher t inner join data.classpupil p on t.classID=p.classID where t.yeargroup=%s;"
    cursor = db.cursor()
    cursor.execute(q, (yeargroup, ))
    db.commit()

    return "Complete"


def clear_relationships(db): 
    '''Truncates the relationships table in database'''

    cursor = db.cursor()
    q1 = "truncate table relationships"
    cursor.execute(q1)
    db.commit()

    return "Complete"

def clear_analysis(db): 
    '''Truncates the analysis table in database'''

    cursor = db.cursor()
    q1 = "truncate table analysis"
    cursor.execute(q1)
    db.commit()

    return "Complete"


def get_appointments(db, group):
    '''Gets all the appointments each pupil/teacher needs to go to.'''

    cursor = db.cursor()

    q1 = "SELECT {}, group_concat({}) from relationships group by {}"

    if group[0].lower() == "p":
        cursor.execute(q1.format("pid", "tid", "pid"))
    elif group[0].lower() == "t":
        cursor.execute(q1.format("tid", "pid", "tid"))
    else:
        return "Not a valid input"
    
    appointments = {}

    for i in cursor.fetchall():
        appointments[int(i[0])] = list(map(int, i[1].split(","))) #Converts it all to ints and makes it a list, with a key of the id.

    return appointments


def get_ids(db, group):
    '''Pulls every UNIQUE id from relationships.'''

    cursor = db.cursor()

    q1 = "SELECT DISTINCT {} from relationships;"

    if group[0].lower() == "p":
        cursor.execute(q1.format("pid"))
    elif group[0].lower() == "t":
        cursor.execute(q1.format("tid"))
    else:
        return "Not a valid input"

    return [x[0] for x in cursor.fetchall()] #Returns it as a list.

def upload_analysis(db, analysis):
    
    cursor = db.cursor()

    for person in range(len(analysis["order"])):

        q1 = "INSERT INTO analysis (pid, earliest, latest, difference, average_gap, min_gap, max_gap) VALUES ({}, {}, {}, {}, {}, {}, {})".format(analysis["order"][person],
        analysis["all_earliest"][person], analysis["all_latest"][person],
        analysis["all_difference"][person], analysis["all_average_gap"][person],
        analysis["all_min_gap"][person], analysis["all_max_gap"][person])

        cursor.execute(q1)

    db.commit()

    return "Done"

