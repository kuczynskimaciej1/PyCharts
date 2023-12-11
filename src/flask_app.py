from flask import Flask, render_template, redirect, url_for, session, request
import global_var
from secrets import token_hex
import dl_data

def flaskInit():
    app = Flask(__name__)
    app.secret_key = token_hex(16)

    @app.route('/')
    def initialPage():
        return render_template("initial.html")

    @app.route('/login')
    def authenticationPage():
        auth_url = global_var.sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    @app.route('/after_login_setup')
    def afterLoginSetup():
        global_var.token_info = global_var.sp_oauth.get_access_token(request.args['code'])
        session['token_info'] = global_var.token_info
        global_var.spotify.auth = global_var.token_info['access_token']
        global_var.user_info = global_var.spotify.me()
        return redirect(url_for('userDashboard'))
    
    @app.route('/logout')
    def logout():
        session.pop('token_info', None)
        global_var.token_info = None
        global_var.spotify.auth = None
        global_var.user_info = None
        app.secret_key = token_hex(16)
        global_var.sp_oauth.state = token_hex(16)
        response = redirect(url_for('initialPage'))
        response.set_cookie('spotipy_token', '', expires=0)
        return response

    @app.route('/user_dashboard')
    def userDashboard():
        return render_template("user_dashboard.html", user_info = global_var.user_info)
    
    @app.route('/user_favorites')
    def userFavorites():
        dl_data.downloadMetadata()
        return render_template("user_favorites.html", user_info = global_var.user_info)
    
    @app.route('/user_playback')
    def userPlayback():
        tracks = dl_data.getUserPlayback()
        return render_template("user_playback.html", user_info = global_var.user_info, tracks = tracks)
    
    @app.route('/user_statistics')
    def userStatistics():
        return render_template("user_statistics.html", user_info = global_var.user_info)
    
    @app.route('/user_generate')
    def userGenerate():
        return render_template("user_generate.html", user_info = global_var.user_info)
    
    @app.route('/training')
    def training():
        return render_template("train.html")
    
    return app