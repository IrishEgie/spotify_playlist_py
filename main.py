from bs4 import BeautifulSoup
import os
import requests as rq
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def auth_to_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                                scope="user-library-read"))
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = rq.get("https://www.billboard.com/charts/hot-100/"+date)

soup = BeautifulSoup(response.text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

print(song_names)