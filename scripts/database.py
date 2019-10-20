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
    print("Executed")

    db.commit()

db = connection("pe")

dataToPe(db, 12)


