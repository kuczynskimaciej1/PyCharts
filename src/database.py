import mysql.connector

def setupDatabseConnection():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="mkuczyns",
        password="ExamplePassword5657",
        database="pycharts"
    )
    cursor =  db_connection.cursor()
    return db_connection, cursor

def closeDatabaseConnection(db_connection, cursor):
    cursor.close()
    db_connection.close()