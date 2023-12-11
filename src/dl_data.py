import global_var
from classes import Track
from global_var import spotify

def getUserPlayback():
    recently_played = global_var.spotify.current_user_recently_played(limit = 50)
    tracks = []
    for item in recently_played['items']:
        tracks.append(Track(item['track']['name'], item['track']['artists'][0]['name'], item['track']['album']['name'], item['track']['album']['images'][0]['url']))
    return tracks

def print_albums_example():
    birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'

    results = spotify.artist_albums(birdy_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])

def downloadMetadata():
    uri = 'spotify:track:2KtSYjhcujuunRR3wyogzu'
    track = spotify.track(uri)
    numerals = spotify.audio_features(uri)[0]
    data = {**track, **numerals}

    with open("demo.txt", "a") as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
    
    file.close()
    return data