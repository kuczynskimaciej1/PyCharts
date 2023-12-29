from flask import Flask, render_template, redirect, url_for, session, request, abort
from secrets import token_hex
import login_global_var
import dl_data
import learning_set
import ai
import recommendation
import ul_data
import ai_global_var
import pandas as pd

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
        tracks = dl_data.getUserFavourites(50)
        print(tracks)
        return render_template("user_favorites.html", user_info = login_global_var.user_info, tracks = tracks)
    

    @app.route('/user_playback')
    def userPlayback():
        tracks = dl_data.getUserPlayback(50)
        return render_template("user_playback.html", user_info = login_global_var.user_info, tracks = tracks)
    

    @app.route('/user_statistics')
    def userStatistics():
        return render_template("user_statistics.html", user_info = login_global_var.user_info)
    

    @app.route('/generate_options')
    def generateOptions():
        return render_template("generate_options.html", user_info = login_global_var.user_info)
    

    @app.route('/single_generate', methods=["GET", "POST"])
    def singleGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        track = request.form.get('track')
        recommendations = recommendation.getRecommendation(int(track), int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data
        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)
    

    @app.route('/vector_generate', methods=["GET", "POST"])
    def vectorGenerate():
        def validate_input(input_str):
            try:
                numbers = [int(num.strip()) for num in input_str.split(',')]
                if all(1 <= num <= 20496 for num in numbers):
                    return numbers
                else:
                    return None
            except ValueError:
                return None
        
        number_of_tracks = request.form.get('number_of_tracks')
        input_numbers = request.form['numbers']
        vector = validate_input(input_numbers)
        
        if vector is not None:
            # Do something with the validated_numbers, like saving as a vector
            recommendations = recommendation.getVectorRecommendation(vector, int(number_of_tracks))
            recommendations_data = recommendations.to_dict(orient='records')
            session['recommendations'] = recommendations_data
            return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)
        else:
            return "Invalid input. Please enter integers in the range 1 to 20496, separated by commas."

    @app.route('/bar_generate', methods=["GET", "POST"])
    def barGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        parameters = [float(request.form.get('valueSliderSpeechiness')), 
                      float(request.form.get('valueSliderInstrumentalness')), 
                      float(request.form.get('valueSliderLiveness')), 
                      float(request.form.get('valueSliderValence')), 
                      float(request.form.get('valueSliderDanceability')), 
                      float(request.form.get('valueSliderEnergy')), 
                      float(request.form.get('valueSliderAcousticness')), 
                      float(request.form.get('valueSliderLoudness')), 
                      float(request.form.get('valueSliderTempo'))]
        recommendations = recommendation.getBarRecommendation(parameters, int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data
        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)
    

    @app.route('/history_generate', methods=["GET", "POST"])
    def historyGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        recommendations = recommendation.getHistoryRecommendation(int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data 
        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)
    

    @app.route('/favourites_generate', methods=["GET", "POST"])
    def favouritesGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        recommendations = recommendation.getFavouritesRecommendation(int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data 
        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)
    

    @app.route('/embeddings')
    def embeddings():
        ai.trainEmbeddings()
        return "Embeddings trained and saved."
    

    @app.route('/mood_training')
    def moodTraining():
        ai.teachNumerical(ai_global_var.scaled_mood_features)
        return "Numerical (mood and acoustic) values trained and saved."
    

    @app.route('/full_training')
    def fullTraining():
        ai.teach(ai_global_var.scaled_features)
        return "Full data trained and saved."
    

    @app.route('/dataset')
    def dataset():
        learning_set.buildDefaultLearningSet()
        return render_template("dataset.html", user_info = login_global_var.user_info)
    
    
    @app.route('/upload_playlist', methods=["POST"])
    def uploadToAccount():
        playlist_name = request.form.get('playlist_name')
        recommendations_data = session.get('recommendations', [])
        recommendations = pd.DataFrame(recommendations_data)
        ul_data.uploadPlaylist(playlist_name, recommendations)
        return f"Playlist '{playlist_name}' created successfully!"
    
    return app