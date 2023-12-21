from flask import Flask, render_template, redirect, url_for, session, request, abort
from secrets import token_hex
import login_global_var
import dl_data
import learning_set
import ai
import recommendation
import ul_data
import ai_global_var

def checkAccess(): ###TODO add to particular functions
    if login_global_var.user_info['display_name'] == "kuczynskimaciej1":
        return True
    else:
        return False

def flaskInit():
    app = Flask(__name__)
    app.secret_key = token_hex(16)

    @app.route('/')
    def initialPage():
        return render_template("initial.html")

    @app.route('/login')
    def authenticationPage():
        auth_url = login_global_var.sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    @app.route('/after_login_setup')
    def afterLoginSetup():
        login_global_var.token_info = login_global_var.sp_oauth.get_access_token(request.args['code'])
        session['token_info'] = login_global_var.token_info
        login_global_var.spotify.auth = login_global_var.token_info['access_token']
        login_global_var.user_info = login_global_var.spotify.me()
        
        return redirect(url_for('adminDashboard'))
    
    @app.route('/logout')
    def logout():
        session.pop('token_info', None)
        login_global_var.token_info = None
        login_global_var.spotify.auth = None
        login_global_var.user_info = None
        app.secret_key = token_hex(16)
        login_global_var.sp_oauth.state = token_hex(16)
        response = redirect(url_for('initialPage'))
        response.set_cookie('spotipy_token', '', expires=0)
        return response
    
    @app.route('/admin_dashboard')
    def adminDashboard():
        return render_template("admin_dashboard.html", user_info = login_global_var.user_info)

    @app.route('/user_dashboard')
    def userDashboard():
        return render_template("user_dashboard.html", user_info = login_global_var.user_info)
    
    @app.route('/user_favorites')
    def userFavorites():
        return render_template("user_favorites.html", user_info = login_global_var.user_info)
    
    @app.route('/user_playback')
    def userPlayback():
        tracks = dl_data.getUserPlayback()
        return render_template("user_playback.html", user_info = login_global_var.user_info, tracks = tracks)
    
    @app.route('/user_statistics')
    def userStatistics():
        return render_template("user_statistics.html", user_info = login_global_var.user_info)
    
    @app.route('/user_generate')
    def userGenerate():
        recommendations = recommendation.getVectorRecommendation([43, 44, 47, 39, 50], 15)
        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)
    
    @app.route('/embeddings')
    def embeddings():
        ai.trainEmbeddings()
        return "Embeddings trained and saved."
    
    @app.route('/training')
    def training():
        return render_template("train.html", user_info = login_global_var.user_info)
    
    @app.route('/start_training')
    def startTraining():
        ai.teach(ai_global_var.scaled_features)
        return render_template("training_progress.html", user_info = login_global_var.user_info)
    
    @app.route('/dataset')
    def dataset():
        learning_set.buildDefaultLearningSet()
        return render_template("dataset.html", user_info = login_global_var.user_info)
    
    @app.route('/upload_playlist', methods=["POST"])
    def uploadToAccount():
        recommendations = recommendation.getVectorRecommendation([43, 44, 47, 39, 50], 15)
        playlist_name = request.form.get('playlist_name')
        ul_data.uploadPlaylist(playlist_name, recommendations)
        return f"Playlist '{playlist_name}' created successfully!"
    
    return app