import mysql.connector

def connection(dataBase): #Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database=dataBase
    )

    print("Connected")
    return db

def dataToPe(db, yeargroup):
    q = "insert into pe.relationships select p.pid, t.tid, t.classID, NULL from data.classteacher t inner join data.classpupil p on t.classID=p.classID where t.yeargroup=%s;"
    cursor = db.cursor()
    cursor.execute(q, (yeargroup, ))

    db.commit()

    return "Complete"

def clear_pe(db):
    cursor = db.cursor()
    q1 = "truncate table relationships"
    cursor.execute(q1)

    db.commit()

    return "Complete"

def get_appointments(db, group):
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
        appointments[int(i[0])] = list(map(int, i[1].split(",")))

    return appointments

def get_ids(db, group):
    cursor = db.cursor()

    q1 = "SELECT {} from relationships;"

    if group[0].lower() == "p":
        cursor.execute(q1.format("pid"))
    elif group[0].lower() == "t":
        cursor.execute(q1.format("tid"))
    else:
        return "Not a valid input"

    return [x[0] for x in cursor.fetchall()]

