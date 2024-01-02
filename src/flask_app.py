from flask import Flask, render_template, redirect, url_for, session, request, abort
from secrets import token_hex
import login_global_var
import dl_data
import learning_set
import ai
import ai_recommendation
import no_ai_recommendation
import ul_data
import ai_global_var
import pandas as pd
import maths_and_stats
import database
import database_global

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
        database.addUserToDatabase()
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
    

    @app.route('/share_feedback')
    def shareFeedback():
        return redirect("https://forms.gle/ySkaayeJWKhgRVRN8")
    

    @app.route('/admin_dashboard')
    def adminDashboard():
        return render_template("admin_dashboard.html", user_info = login_global_var.user_info)


    @app.route('/user_dashboard')
    def userDashboard():
        return render_template("user_dashboard.html", user_info = login_global_var.user_info)
    

    @app.route('/browse_dataset')
    def browseDataset():
        data = ai_global_var.presentation_features.to_html(classes="table table-bordered", index=True)
        return render_template("browse_dataset.html", data = data, user_info = login_global_var.user_info)
    

    @app.route('/browse_recommendations')
    def browseRecommendations():
        db_connection, cursor = database.setupDatabaseConnection()
        playlist_query = cursor.execute('SELECT * FROM Playlist')
        database_global.playlists = playlist_query.fetchall()
        database.commitAndCloseDatabaseConnection(db_connection, cursor)
        return render_template("browse_recommendations.html", playlists = database_global.playlists, user_info = login_global_var.user_info)


    @app.route('/browse_tracks', methods=['GET', 'POST'])
    def browseTracks():
        playlist_id = request.form.get('playlist_id')
        db_connection, cursor = database.setupDatabaseConnection()
        tracks_query = cursor.execute('SELECT * FROM Track WHERE playlist_id = ?', (playlist_id,))
        database_global.tracks = tracks_query.fetchall()
        database.commitAndCloseDatabaseConnection(db_connection, cursor)
        return render_template('browse_tracks.html', tracks=database_global.tracks, user_info = login_global_var.user_info)


    @app.route('/rate_track', methods=['GET', 'POST'])
    def rateTrack():
        rate = request.form.get('track_rate')
        track_id = request.form.get('track_id')
        db_connection, cursor = database.setupDatabaseConnection()
        cursor.execute('UPDATE track SET mark_given = ? WHERE track_id = ?', (rate, track_id))
        database.commitAndCloseDatabaseConnection(db_connection, cursor)
        return redirect(url_for('browseRecommendations'))


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
        numerical_statistics = maths_and_stats.calculateUserNumericals()
        for i, element in enumerate(numerical_statistics):
            numerical_statistics[i] = round(element, 5)
        return render_template("user_statistics.html", numerical_statistics = numerical_statistics, user_info = login_global_var.user_info)
    

    @app.route('/ai_generate_options')
    def aiGenerateOptions():
        return render_template("ai_generate_options.html", user_info = login_global_var.user_info)
    

    @app.route('/no_ai_generate_options')
    def noAiGenerateOptions():
        return render_template("no_ai_generate_options.html", user_info = login_global_var.user_info)
    

    @app.route('/single_generate', methods=["GET", "POST"])
    def singleGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        track = request.form.get('track')
        recommendations = ai_recommendation.getTrackRecommendation(int(track), int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data

        no_ai_playlist = no_ai_recommendation.getNoAITrackRecommendation(int(track), int(number_of_tracks))
        correlation = maths_and_stats.calculateCorrelation(recommendations, no_ai_playlist)

        database_global.generation_method = "single"
        database_global.parameters = track

        return render_template("user_generate_ai.html", recommendations = recommendations, correlation = correlation, user_info = login_global_var.user_info)
    

    @app.route('/single_no_ai_generate', methods=["GET", "POST"])
    def singleNoAiGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        track = request.form.get('track')
        recommendations = no_ai_recommendation.getNoAITrackRecommendation(int(track), int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data

        database_global.generation_method = "singleNoAi"
        database_global.parameters = track

        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)


    @app.route('/vector_generate', methods=["GET", "POST"])
    def vectorGenerate():
        def validate_input(input_str):
            try:
                numbers = [int(num.strip()) for num in input_str.split(',')]
                if all(0 <= num <= 20593 for num in numbers):
                    return numbers
                else:
                    return None
            except ValueError:
                return None
        
        number_of_tracks = request.form.get('number_of_tracks')
        input_numbers = request.form['numbers']
        vector = validate_input(input_numbers)
        
        if vector is not None:
            recommendations = ai_recommendation.getVectorRecommendation(vector, int(number_of_tracks))
            recommendations_data = recommendations.to_dict(orient='records')
            session['recommendations'] = recommendations_data

            no_ai_playlist = no_ai_recommendation.getNoAIVectorRecommendation(vector, int(number_of_tracks))
            correlation = maths_and_stats.calculateCorrelation(recommendations, no_ai_playlist)

            database_global.generation_method = "vector"
            database_global.parameters = database.vectorToString(vector)

            return render_template("user_generate_ai.html", recommendations = recommendations, correlation = correlation, user_info = login_global_var.user_info)
        else:
            return "Invalid input. Please enter integers in the range 1 to 20496, separated by commas."
        
    
    @app.route('/vector_no_ai_generate', methods=["GET", "POST"])
    def vectorNoAiGenerate():
        def validate_input(input_str):
            try:
                numbers = [int(num.strip()) for num in input_str.split(',')]
                if all(0 <= num <= 20593 for num in numbers):
                    return numbers
                else:
                    return None
            except ValueError:
                return None
        
        number_of_tracks = request.form.get('number_of_tracks')
        input_numbers = request.form['numbers']
        vector = validate_input(input_numbers)
        
        if vector is not None:
            recommendations = no_ai_recommendation.getNoAIVectorRecommendation(vector, int(number_of_tracks))
            recommendations_data = recommendations.to_dict(orient='records')
            session['recommendations'] = recommendations_data

            database_global.generation_method = "vectorNoAi"
            database_global.parameters = database.vectorToString(vector)

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
        recommendations = ai_recommendation.getBarRecommendation(parameters, int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data

        database_global.generation_method = "bar"
        database_global.parameters = database.vectorToString(parameters)

        no_ai_playlist = no_ai_recommendation.getNoAIBarRecommendation(parameters, int(number_of_tracks))
        correlation = maths_and_stats.calculateCorrelation(recommendations, no_ai_playlist)
        return render_template("user_generate_ai.html", recommendations = recommendations, correlation = correlation, user_info = login_global_var.user_info)
    

    @app.route('/bar_no_ai_generate', methods=["GET", "POST"])
    def barNoAiGenerate():
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
        recommendations = no_ai_recommendation.getNoAIBarRecommendation(parameters, int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data

        database_global.generation_method = "barNoAi"
        database_global.parameters = parameters

        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)


    @app.route('/history_generate', methods=["GET", "POST"])
    def historyGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        recommendations = ai_recommendation.getHistoryRecommendation(int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data

        no_ai_playlist = no_ai_recommendation.getNoAIHistoryRecommendation(int(number_of_tracks))
        correlation = maths_and_stats.calculateCorrelation(recommendations, no_ai_playlist)

        database_global.generation_method = "history"

        return render_template("user_generate_ai.html", recommendations = recommendations, correlation = correlation, user_info = login_global_var.user_info)
    

    @app.route('/history_no_ai_generate', methods=["GET", "POST"])
    def historyNoAiGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        recommendations = no_ai_recommendation.getNoAIHistoryRecommendation(int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data
        database_global.generation_method = "historyNoAi"
        return render_template("user_generate.html", recommendations = recommendations, user_info = login_global_var.user_info)


    @app.route('/favourites_generate', methods=["GET", "POST"])
    def favouritesGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        recommendations = ai_recommendation.getFavouritesRecommendation(int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data

        no_ai_playlist = no_ai_recommendation.getNoAIFavouritesRecommendation(int(number_of_tracks))
        correlation = maths_and_stats.calculateCorrelation(recommendations, no_ai_playlist)

        database_global.generation_method = "favourites"

        return render_template("user_generate_ai.html", recommendations = recommendations, correlation = correlation, user_info = login_global_var.user_info)
    

    @app.route('/favourites_no_ai_generate', methods=["GET", "POST"])
    def favouritesNoAiGenerate():
        number_of_tracks = request.form.get('number_of_tracks')
        recommendations = no_ai_recommendation.getNoAIFavouritesRecommendation(int(number_of_tracks))
        recommendations_data = recommendations.to_dict(orient='records')
        session['recommendations'] = recommendations_data
        database_global.generation_method = "favouritesNoAi"
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
        return "Dataset built and saved."
    
    
    @app.route('/upload_playlist', methods=["POST"])
    def uploadToAccount():
        playlist_name = request.form.get('playlist_name')
        recommendations_data = session.get('recommendations', [])
        recommendations = pd.DataFrame(recommendations_data)

        track_uris = ul_data.uploadPlaylist(playlist_name, recommendations)

        database.addPlaylistToDatabase(playlist_name, database_global.generation_method, database_global.parameters)
        for index, track_uri in enumerate(track_uris):
            database.addTrackToDatabase(None, index+1, track_uri, int(database_global.recommended_indices[index]), recommendations.iloc[index]['Track'], recommendations.iloc[index]['Artist'], recommendations.iloc[index]['Album'])

        return f"Playlist '{playlist_name}' created successfully!"
    
    return app