from scipy.stats import pearsonr
import numpy as np
import ai_global_var
import dl_data
import pandas as pd

def calculateCorrelation(playlist1, playlist2):
    playlist1_data_flat = playlist1[ai_global_var.all_features_list].values.flatten()
    playlist2_data_flat = playlist2[ai_global_var.all_features_list].values.flatten()
    correlation_coefficient = pearsonr(playlist1_data_flat, playlist2_data_flat)[0]
    return (correlation_coefficient)

def calculateUserNumericals():
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

    return mean_track