import mysql.connector

def connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="pe"
    )

    return db

db = connection()



q = "insert into pe.relationships select p.pid, t.tid, t.classID, NULL from classteacher t inner join classpupil p on t.classID=p.classID where t.yeargroup=12;"