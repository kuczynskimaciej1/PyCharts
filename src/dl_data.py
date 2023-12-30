import login_global_var
from classes import Track

def getUserPlayback(limit):
    recently_played = login_global_var.spotify.current_user_recently_played(limit = limit)
    tracks = []
    for item in recently_played['items']:
        tracks.append(Track(item['track']['uri'], 
                            item['track']['name'], 
                            item['track']['artists'][0]['name'], 
                            item['track']['album']['name'], 
                            item['track']['album']['images'][0]['url']))
    return tracks


def getUserFavourites(limit):
    favourites = login_global_var.spotify.current_user_top_tracks(limit = limit)
    tracks = []
    for item in favourites['items']:
        tracks.append(Track(item['uri'], 
                            item['name'], 
                            item['artists'][0]['name'], 
                            item['album']['name'], 
                            item['album']['images'][0]['url']))
    return tracks


def downloadTrackMetadataToTxt(uri):
    track = login_global_var.spotify.track(uri)
    numerals = login_global_var.spotify.audio_features(uri)[0]
    data = {**track, **numerals}

    with open(f"{uri}.txt", "a") as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
    
    file.close()
    return data


def downloadTrackMetadataToUse(uri):
    track = login_global_var.spotify.track(uri)
    numerals = login_global_var.spotify.audio_features(uri)[0]
    data = {**track, **numerals}
    return data