import ai_global_var
from classes import Track
from login_global_var import spotify

def getUserPlayback():
    recently_played = ai_global_var.spotify.current_user_recently_played(limit = 50)
    tracks = []
    for item in recently_played['items']:
        tracks.append(Track(item['track']['name'], item['track']['artists'][0]['name'], item['track']['album']['name'], item['track']['album']['images'][0]['url']))
    return tracks

def downloadTrackMetadataToTxt(uri):
    track = spotify.track(uri)
    numerals = spotify.audio_features(uri)[0]
    data = {**track, **numerals}

    with open(f"{uri}.txt", "a") as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
    
    file.close()
    return data

def downloadTrackMetadataToUse(uri):
    track = spotify.track(uri)
    numerals = spotify.audio_features(uri)[0]
    data = {**track, **numerals}
    return data