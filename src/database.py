import sqlite3
import login_global_var


def setupDatabseConnection():
    db_connection = sqlite3.connect('database/database.db')
    cursor = db_connection.cursor()
    return db_connection, cursor


def commitAndCloseDatabaseConnection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def createTables():
    connection, cursor = setupDatabseConnection()

    with open('database/db_setup.sql', 'r') as file:
        sql_commands = file.read()
        cursor.executescript(sql_commands)

    commitAndCloseDatabaseConnection(connection, cursor)


def addUserToDatabase():
    connection, cursor = setupDatabseConnection()

    username = login_global_var.user_info['display_name']
    uri = login_global_var.user_info['uri']

    print(username)
    print(uri)

    query_check_if_exists = "SELECT * FROM user WHERE uri = ?"
    cursor.execute(query_check_if_exists, (uri,))
    existing_user = cursor.fetchone()

    if not existing_user:
        query_add_to_database = "INSERT INTO user (spotify_name, uri) VALUES (?, ?)"
        cursor.execute(query_add_to_database, (username, uri))
        commitAndCloseDatabaseConnection(connection, cursor)


def addPlaylistToDatabase():
    return


def addTrackToDatabase():
    return