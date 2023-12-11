from flask import Flask, render_template, redirect, url_for, session, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure secret key

SPOTIPY_CLIENT_ID = "8e50c2065b334b158b7d20399aea45af"
SPOTIPY_CLIENT_SECRET = "60b71876911648ff8ebbdd4a67f21293"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000/"

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope="user-library-read")

@app.route('/')
def home():
    if 'token_info' in session:
        # User is logged in, retrieve user's data from Spotify
        token_info = session['token_info']
        spotify = spotipy.Spotify(auth=token_info['access_token'])
        user_info = spotify.me()

        return render_template('home.html', user_info=user_info)

    return redirect(url_for('login'))

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.pop('token_info', None)
    return redirect(url_for('home'))

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
