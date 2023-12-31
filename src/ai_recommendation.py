import numpy as np
import ai_global_var
import dl_data
import database_global_var

def getTrackRecommendation(track_index, num_recommendations):
    input_track = ai_global_var.scaled_features[track_index].reshape(1, -1)
    reconstructed_track = ai_global_var.ai_model.predict(input_track)
    distances = np.linalg.norm(ai_global_var.scaled_features - reconstructed_track, axis=1)
    recommended_indices = np.argsort(distances)[1:num_recommendations + 1]
    database_global_var.recommended_indices = recommended_indices
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print(recommended_tracks)
    return recommended_tracks


def getVectorRecommendation(track_indices, num_recommendations):
    input_tracks = ai_global_var.scaled_features[track_indices]
    mean_track = np.mean(input_tracks, axis=0, keepdims=True)
    reconstructed_mean_track = ai_global_var.ai_model.predict(mean_track)
    distances = np.linalg.norm(ai_global_var.scaled_features - reconstructed_mean_track, axis=1)
    recommended_indices = np.argsort(distances)[:num_recommendations]
    database_global_var.recommended_indices = recommended_indices
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print("Recommended Tracks:")
    print(recommended_tracks[['Track', 'Artist']])
    return recommended_tracks


def getBarRecommendation(parameters, num_recommendations):
    input_features = np.array(parameters, dtype=float).reshape(1, -1)
    reconstructed_input_features = ai_global_var.ai_model_mood.predict(input_features)
    distances = np.linalg.norm(ai_global_var.scaled_mood_features - reconstructed_input_features, axis=1)
    recommended_indices = np.argsort(distances)[:num_recommendations]
    database_global_var.recommended_indices = recommended_indices
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print("Recommended Tracks:")
    print(recommended_tracks[['Track', 'Artist']])
    print(database_global_var.user_id)
    return recommended_tracks


def getHistoryRecommendation(num_recommendations):
    history = dl_data.getUserPlayback(50)

    input_tracks = []
    for track in history:
        input_tracks.append(dl_data.downloadTrackMetadataToUse(track.uri))

    speechiness = [track['speechiness'] for track in input_tracks]
    instrumentalness = [track['instrumentalness'] for track in input_tracks]
    liveness = [track['liveness'] for track in input_tracks]
    valence = [track['valence'] for track in input_tracks]
    danceability = [track['danceability'] for track in input_tracks]
    energy = [track['energy'] for track in input_tracks]
    acousticness = [track['acousticness'] for track in input_tracks]
    loudness = [track['loudness'] for track in input_tracks]
    tempo = [track['tempo'] for track in input_tracks]

    speechiness_array = np.array(speechiness)
    instrumentalness_array = np.array(instrumentalness)
    liveness_array = np.array(liveness)
    valence_array = np.array(valence)
    danceability_array = np.array(danceability)
    energy_array = np.array(energy)
    acousticness_array = np.array(acousticness)
    loudness_array = np.array(loudness)
    tempo_array = np.array(tempo)

    mean_track = np.array([speechiness_array.mean(), instrumentalness_array.mean(), 
                        liveness_array.mean(), valence_array.mean(), 
                        danceability_array.mean(), energy_array.mean(), 
                        acousticness_array.mean(), loudness_array.mean(), 
                        tempo_array.mean()])
    

    database_global_var.parameters = str(mean_track)
    recommended_tracks = getBarRecommendation(mean_track, num_recommendations)
    return recommended_tracks


def getFavouritesRecommendation(num_recommendations):
    favourites = dl_data.getUserFavourites(50)

    input_tracks = []
    for track in favourites:
        input_tracks.append(dl_data.downloadTrackMetadataToUse(track.uri))

    speechiness = [track['speechiness'] for track in input_tracks]
    instrumentalness = [track['instrumentalness'] for track in input_tracks]
    liveness = [track['liveness'] for track in input_tracks]
    valence = [track['valence'] for track in input_tracks]
    danceability = [track['danceability'] for track in input_tracks]
    energy = [track['energy'] for track in input_tracks]
    acousticness = [track['acousticness'] for track in input_tracks]
    loudness = [track['loudness'] for track in input_tracks]
    tempo = [track['tempo'] for track in input_tracks]

    speechiness_array = np.array(speechiness)
    instrumentalness_array = np.array(instrumentalness)
    liveness_array = np.array(liveness)
    valence_array = np.array(valence)
    danceability_array = np.array(danceability)
    energy_array = np.array(energy)
    acousticness_array = np.array(acousticness)
    loudness_array = np.array(loudness)
    tempo_array = np.array(tempo)

    mean_track = np.array([speechiness_array.mean(), instrumentalness_array.mean(), 
                        liveness_array.mean(), valence_array.mean(), 
                        danceability_array.mean(), energy_array.mean(), 
                        acousticness_array.mean(), loudness_array.mean(), 
                        tempo_array.mean()])

    database_global_var.parameters = str(mean_track)

    recommended_tracks = getBarRecommendation(mean_track, num_recommendations)
    return recommended_tracks