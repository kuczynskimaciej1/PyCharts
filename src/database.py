import sqlite3
import random
import datetime
import string
import login_global_var
import database_global_var


def generateInternalId():
    result_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(64))
    return result_str


def getDateAndTime():
    current_datetime = datetime.datetime.now()
    sqlite_formatted_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return sqlite_formatted_date


def vectorToString(vector):
    vector_string = ", ".join(map(str, vector))
    return vector_string


def setupDatabaseConnection():
    db_connection = sqlite3.connect('database/database.db')
    cursor = db_connection.cursor()
    return db_connection, cursor


def commitAndCloseDatabaseConnection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def createTables():
    connection, cursor = setupDatabaseConnection()

    with open('database/db_setup.sql', 'r') as file:
        sql_commands = file.read()
        cursor.executescript(sql_commands)

    commitAndCloseDatabaseConnection(connection, cursor)


def addUserToDatabase():
    connection, cursor = setupDatabaseConnection()

    username = login_global_var.user_info['display_name']
    uri = login_global_var.user_info['uri']

    query_check_if_exists = "SELECT * FROM user WHERE uri = ?"
    cursor.execute(query_check_if_exists, (uri,))
    existing_user = cursor.fetchone()

    if not existing_user:
        internal_id = generateInternalId()
        database_global_var.user_id = internal_id
        query_add_to_database = "INSERT INTO user (spotify_name, uri, user_internal_id) VALUES (?, ?, ?)"
        cursor.execute(query_add_to_database, (username, uri, internal_id))
        commitAndCloseDatabaseConnection(connection, cursor)
    else:
        query_select_internal_id = "SELECT user_internal_id FROM user WHERE spotify_name = ? AND uri = ?"
        cursor.execute(query_select_internal_id, (username, uri))
        internal_id = cursor.fetchone()
        database_global_var.user_id = internal_id[0]


def addPlaylistToDatabase(playlist_name, generation_method, parameters):
    connection, cursor = setupDatabaseConnection()

    user_id = database_global_var.user_id
    date_time = getDateAndTime()
    correlation = database_global_var.correlation
    internal_id = generateInternalId()
    database_global_var.playlist_id = internal_id

    query_add_to_database = "INSERT INTO playlist (user_id, playlist_name, date_of_creation, playlist_internal_id, generation_method, parameters, correlation) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query_add_to_database, (user_id, playlist_name, date_time, internal_id, generation_method, parameters, correlation))
    commitAndCloseDatabaseConnection(connection, cursor)


def addTrackToDatabase(mark_given, rank_on_list, uri, dataset_id, title, artist, album):
    connection, cursor = setupDatabaseConnection()

    playlist_id = database_global_var.playlist_id

    query_add_to_database = "INSERT INTO track (playlist_id, mark_given, rank_on_list, uri, dataset_id, title, artist, album) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query_add_to_database, (playlist_id, mark_given, rank_on_list, uri, dataset_id, title, artist, album))
    commitAndCloseDatabaseConnection(connection, cursor)