import flask_app
import database
import database_global

try:
    database_global.db_connection, database_global.cursor = database.setupDatabseConnection()
finally:
    database.closeDatabaseConnection(database_global.db_connection, database_global.cursor)

app = flask_app.flaskInit()
if __name__ == "__main__":
    app.run(debug = True)