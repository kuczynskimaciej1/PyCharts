import numpy as np
import ai_global_var

def getVectorRecommendation(track_indices, num_recommendations):
    # Example: Get recommendations for a list of track indices
    input_tracks = ai_global_var.scaled_features[track_indices]
    
    # Calculate the mean of the input tracks' features
    mean_track = np.mean(input_tracks, axis=0, keepdims=True)
    
    # Generate recommendations based on the mean track
    reconstructed_mean_track = ai_global_var.ai_model.predict(mean_track)
    
    # Compute Euclidean distance between mean track and all tracks
    distances = np.linalg.norm(ai_global_var.scaled_features - reconstructed_mean_track, axis=1)
    
    # Get indices of the closest tracks
    recommended_indices = np.argsort(distances)[:num_recommendations]
    
    # Display recommended tracks
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print("Recommended Tracks:")
    print(recommended_tracks[['Track', 'Artist']])
    
    return recommended_tracks

def getRecommendation(track_index, num_recommendations):
    # Example: Get recommendations for track at index 0
    input_track = ai_global_var.scaled_features[track_index].reshape(1, -1)
    reconstructed_track = ai_global_var.ai_model.predict(input_track)
        
    # Compute Euclidean distance between input and all tracks
    distances = np.linalg.norm(ai_global_var.scaled_features - reconstructed_track, axis=1)
        
    # Get indices of the closest tracks
    recommended_indices = np.argsort(distances)[1:num_recommendations + 1]

    # Display recommended tracks
    recommended_tracks = ai_global_var.df.iloc[recommended_indices]
    print(recommended_tracks)
    print(recommended_tracks[['Track', 'Artist']])

    return recommended_tracks