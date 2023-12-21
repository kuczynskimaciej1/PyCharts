from flask_app import flaskInit
import database

def main():
    if __name__ == "__main__":
        app.run(debug = True)

#app = flaskInit()
#main()

try:
    connection, cursor = database.setupDatabseConnection()
    app = flaskInit()
    main()
finally:
    database.closeDatabaseConnection(connection, cursor)