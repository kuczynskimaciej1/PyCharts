import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import token_hex

SPOTIPY_CLIENT_ID = "8e50c2065b334b158b7d20399aea45af"
SPOTIPY_CLIENT_SECRET = "60b71876911648ff8ebbdd4a67f21293"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000/after_login_setup"

global token_info, user_info, spotify, sp_oauth

token_info = None
user_info = None

spotify = spotipy.Spotify(auth=None, 
                          client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(
                            SPOTIPY_CLIENT_ID, 
                            SPOTIPY_CLIENT_SECRET))

sp_oauth = SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID, 
                        client_secret = SPOTIPY_CLIENT_SECRET, 
                        redirect_uri = SPOTIPY_REDIRECT_URI,
                        state = token_hex(16),
                        scope = "user-library-read,user-library-modify,user-follow-read,user-follow-modify,playlist-modify-private,playlist-modify-public,user-read-private,user-read-email,user-read-playback-position,user-top-read,user-read-recently-played,ugc-image-upload")