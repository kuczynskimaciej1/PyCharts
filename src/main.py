import flask_app

app = flask_app.flaskInit()
if __name__ == "__main__":
    app.run(debug = True)