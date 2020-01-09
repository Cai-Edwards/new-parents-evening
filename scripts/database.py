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

    q = "insert ignore into pe.relationships select p.pid, t.tid, t.classID, NULL from data.classteacher t inner join data.classpupil p on t.classID=p.classID where t.yeargroup=%s;"
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

def clear_slots(db):
    '''Clear the slots field'''
    cursor = db.cursor()
    q1 = "UPDATE relationships SET slot = NULL"
    cursor.execute(q1)
    db.commit()

def clear_analysis(db): 
    '''Truncates the analysis table in database'''

    cursor = db.cursor()
    q1 = "truncate table analysis"
    cursor.execute(q1)
    db.commit()

    return "Complete"

def get_timetable(db, group):
    '''Gets the appointment timetable TODO''' 

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

def remove_subject(db, subject_name):
    '''Removes all instances of a classID with a subject=subject_name in relationships
    
    Takes db and the subject name'''

    q = "DELETE FROM relationships WHERE classID IN (SELECT classID FROM data.setsubject WHERE subject=(SELECT d.subject FROM data.subjectname d WHERE subjectName='{}'));".format(
        subject_name
    )

    cursor = db.cursor()
    cursor.execute(q)

    db.commit()

    return "Done"

def remove_general(db):
    '''Removes all subjects generally not in parents evening'''

    subjects = ["Personal Development", "Private Study", "Physical Education", "Diploma",
    "Games", "Swimming", "EPQ", "English Support", "Maths Support", "Toilet Duty", 
    "Learning Support", "Private Study Lib", "Tutor Commendation"]

    for i in subjects:
        remove_subject(db, i)

    return "Done"

def update_slots(db, timetable, group):
    '''Inserts slots into the database'''

    cursor = db.cursor()
    cursor2 = db.cursor()

    if group == "pid": other = 1
    elif group == "tid": other = 0
    else: return "Incorrect group"

    for i in timetable:
        q = "SELECT pid, tid, classID from relationships where {}={}".format(group, i)
        cursor.execute(q)

        teacher_info = cursor.fetchall()

        for k in teacher_info:
            slot = timetable[i].index(k[other]) + 1

            q2 = "UPDATE relationships SET slot = {} WHERE (pid={} and tid={} and classID={})".format(slot, k[0], k[1], k[2])
            cursor2.execute(q2)
    
    db.commit()

    return "Done"

print("Loaded database.py")