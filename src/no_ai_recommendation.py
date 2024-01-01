import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ai_global_var
import dl_data
import database
import database_global

def getNoAITrackRecommendation(track_index, num_recommendations):
    similarity_matrix = cosine_similarity(ai_global_var.mood_features, ai_global_var.mood_features)
    similarity_df = pd.DataFrame(similarity_matrix, index=ai_global_var.df.index, columns=ai_global_var.df.index)
    track_similarity = similarity_df[track_index]
    recommended_indices = track_similarity.sort_values(ascending=False).index[1:num_recommendations+1]
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print(f"Recommendations for {track_index}:")
    print(recommended_tracks)
    return recommended_tracks


def getNoAIVectorRecommendation(track_indices, num_recommendations):
    similarity_matrix = cosine_similarity(ai_global_var.mood_features, ai_global_var.mood_features)
    similarity_df = pd.DataFrame(similarity_matrix, index=ai_global_var.df.index, columns=ai_global_var.df.index)
    track_similarity = similarity_df.loc[track_indices].mean(axis=0)
    recommended_indices = track_similarity.sort_values(ascending=False).index[1:num_recommendations+1]
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print(f"Recommendations for {track_indices}:")
    print(recommended_tracks)
    return recommended_tracks


def getNoAIBarRecommendation(parameters, num_recommendations):
    input_features = pd.DataFrame([parameters], columns=['Danceability', 'Energy', 'Loudness', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo'])
    input_similarity = cosine_similarity(ai_global_var.mood_features, input_features)
    input_similarity_df = pd.DataFrame(input_similarity, index=ai_global_var.df.index, columns=['Similarity'])
    recommended_indices = input_similarity_df['Similarity'].sort_values(ascending=False).index[:num_recommendations]
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print(f"Recommendations for {parameters}:")
    print(recommended_tracks)
    return recommended_tracks


def getNoAIHistoryRecommendation(num_recommendations):
    history = dl_data.getUserPlayback(3)

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
    
    database_global.parameters = database.vectorToString(mean_track)
    recommended_tracks = getNoAIBarRecommendation(mean_track, num_recommendations)
    return recommended_tracks


def getNoAIFavouritesRecommendation(num_recommendations):
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

    database_global.parameters = database.vectorToString(mean_track)
    recommended_tracks = getNoAIBarRecommendation(mean_track, num_recommendations)
    return recommended_tracks