import mysql.connector
import database_global
import login_global_var

def setupDatabseConnection():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="mkuczyns",
        password="ExamplePassword5657",
        database="pycharts"
    )
    cursor = db_connection.cursor()
    return db_connection, cursor

def closeDatabaseConnection(db_connection, cursor):
    cursor.close()
    db_connection.close()

def addUserToDatabase():
    username = login_global_var.user_info['display_name']
    uri = login_global_var.user_info['uri']

    query_check_if_exists = "SELECT * FROM users WHERE spotify_uri = %s"
    database_global.cursor.execute(query_check_if_exists, (uri))
    existing_user = database_global.cursor.fetchone()

    if not existing_user:
        query_add_to_database = "INSERT INTO user (spotify_nickname, uri) VALUES (%s, %s)"
        database_global.cursor.execute(query_add_to_database, (username, uri))
        database_global.db_connection.commit()

def addPlaylistToDatabase():
    return

def addTrackToDatabase():
    return