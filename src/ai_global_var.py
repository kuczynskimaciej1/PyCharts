import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

global ai_model, df, artist_encoded, album_encoded, numerical_features, scaled_features

ai_model = load_model("models/spotify_recommendation_model.h5")
df = pd.read_csv("learning_set/spotify_dataset_exported.csv")
artist_encoded = None
album_encoded = None

numerical_features = df[['Speechiness', 
                   'Instrumentalness', 
                   'Liveness', 
                   'Valence', 
                   'Danceability', 
                   'Energy', 
                   'Acousticness',  
                   'Loudness', 
                   'Tempo', 
                   'Duration_min',
                   'Artist_num',
                   'Album_num']]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(numerical_features)