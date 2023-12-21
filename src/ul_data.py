import login_global_var

def uploadPlaylist(name, recommendations):
    playlist = login_global_var.spotify.user_playlist_create(login_global_var.spotify.me()['id'], name, public = False)
    #tracks = recommendations['Uri']
    #login_global_var.spotify.playlist_add_items(playlist['id'], tracks)

    # Add tracks to the playlist
    track_uris = []
    for _, track in recommendations.iterrows():
        results = login_global_var.spotify.search(q=f"{track['Artist']} {track['Track']}", type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)

    login_global_var.spotify.playlist_add_items(playlist['id'], track_uris)