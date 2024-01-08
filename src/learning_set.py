import csv
from login_global_var import spotify
from dl_data import downloadTrackMetadataToUse
import ai_global_var


def buildDefaultLearningSet():
    csv_filename = "learning_set/spotify_dataset_exported.csv"

    with open(csv_filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    artist_mapping = {}
    for index, row in ai_global_var.artist_encoded.iterrows():
        artist_mapping[row[0]] = row[1]

    album_mapping = {}
    for index, row in ai_global_var.album_encoded.iterrows():
        album_mapping[row[0]] = row[1]

    for row in data:
        artist = row['Artist']
        album = row['Album']
        row['Artist_num'] = artist_mapping.get(artist, 0.0)
        row['Album_num'] = album_mapping.get(album, 0.0)

    output_csv_file = "learning_set/spotify_dataset_exported.csv"

    with open(output_csv_file, 'w', newline='', encoding='utf-8') as output_file:
        fieldnames = list(data[0].keys())# + ['Artist_num', 'Album_num']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        csv_writer.writerows(data)


def buildAPILearningSet():
    playlists_to_save = ["spotify:playlist:7sfrYAuobUw9O679LwuvIm", 
                        "spotify:playlist:2NfTM2df5tHVUquNwet0yB", 
                        "spotify:playlist:4qXpkv2SqtIqjMmVk2JAcy"]

    csv_filename = "learning_set/playlist_data.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        headers_written = False

        for playlist in playlists_to_save:
            offset = 0
            limit = 10
            
            while True:
                results = spotify.playlist_tracks(playlist, offset=offset, limit=limit)

                if not headers_written:
                    first_song_url = results['items'][0]['track']['uri']
                    headers = downloadTrackMetadataToUse(first_song_url).keys()
                    csv_writer.writerow(headers)
                    headers_written = True

                for track in results['items']:
                    print(track)
                    values = downloadTrackMetadataToUse(track['track']['uri']).values()
                    csv_writer.writerow(values)

                if not results['next']:
                    break

                offset += limit