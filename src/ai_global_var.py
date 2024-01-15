import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

global ai_model, df, artist_encoded, album_encoded, presentation_features, all_features, mood_features, scaled_features, scaled_mood_features, data_to_display

ai_model = load_model("models/spotify_recommendation_model.h5")
ai_model_mood = load_model("models/spotify_recommendation_model_mood.h5")
df = pd.read_csv("learning_set/spotify_dataset_exported.csv")
artist_encoded = None
album_encoded = None

presentation_features = df[['Artist',
                            'Track',
                            'Album',
                            'Speechiness', 
                            'Instrumentalness', 
                            'Liveness', 
                            'Valence', 
                            'Danceability', 
                            'Energy', 
                            'Acousticness',  
                            'Loudness', 
                            'Tempo']]

all_features = df[['Speechiness', 
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

mood_features = df[['Speechiness', 
                   'Instrumentalness', 
                   'Liveness', 
                   'Valence', 
                   'Danceability', 
                   'Energy', 
                   'Acousticness',  
                   'Loudness', 
                   'Tempo']]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(all_features)
scaled_mood_features = scaler.fit_transform(mood_features)

all_features_list = ['Speechiness', 
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
                   'Album_num']

data_to_display = None