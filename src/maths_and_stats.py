from scipy.stats import pearsonr
from io import BytesIO
import pandas as pd
import base64
import numpy as np
import ai_global_var
import dl_data
import matplotlib.pyplot as plt


def calculateCorrelation(playlist1, playlist2):
    playlist1_data_flat = playlist1[ai_global_var.all_features_list].values.flatten()
    playlist2_data_flat = playlist2[ai_global_var.all_features_list].values.flatten()
    correlation_coefficient, p_value = pearsonr(playlist1_data_flat, playlist2_data_flat)
    print(f"Correlation: {correlation_coefficient}")
    print(f"p-value: {p_value}")
    return correlation_coefficient


def calculateUserNumericals():
    favourites = dl_data.getUserFavourites(50)

    input_tracks = []
    for track in favourites:
        input_tracks.append(dl_data.downloadTrackMetadataToUse(track.uri))

    columns = ['speechiness', 'instrumentalness', 'liveness', 'valence', 'danceability', 'energy', 'acousticness', 'loudness', 'tempo']
    tracks_df = pd.DataFrame(input_tracks, columns=columns)
    tracks_df.columns = tracks_df.columns.str.capitalize()
    ai_global_var.data_to_display = tracks_df
    mean_track = np.mean(tracks_df, axis=0)

    return mean_track


def calculateDatasetNumericals():
    input_tracks = pd.DataFrame(ai_global_var.mood_features)
    ai_global_var.data_to_display = input_tracks
    mean_track = np.mean(input_tracks, axis=0)
    return mean_track


def calculateColumnStats(column_df, column_name):
    stats = {
        'Mean': column_df.mean(),
        'Median': column_df.median(),
        'Standard deviation': column_df.std(),
        'Max value': column_df.max(),
        'Min value': column_df.min(),
        'Quartile 1': column_df.quantile(0.25),
        'Quartile 3': column_df.quantile(0.75),
        'Skew': column_df.skew(),
        'Kurtosis': column_df.kurtosis()
    }

    histogram = generate_histogram(column_df, column_name)
    return (stats, histogram)


def generate_histogram(column_df, column_name):

    plt.figure(figsize=(30, 24))
    plt.hist(column_df, bins=50, color='skyblue', edgecolor='black')
    plt.title(f'Plot for {column_name}', fontsize=30)
    plt.xlabel('Value', fontsize=24)
    plt.ylabel('Indices', fontsize=24)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_base64 = base64.b64encode(buf.read()).decode('utf-8')

    plt.close()
    
    return plot_base64