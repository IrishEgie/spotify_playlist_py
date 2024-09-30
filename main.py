from bs4 import BeautifulSoup
import os
import requests as rq
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Authenticate with Spotify
def auth_to_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                                   client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                                   redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                                   scope="playlist-modify-private"))

    return sp

# Create a new playlist and add songs
def create_playlist_and_add_tracks(sp, song_uris, date):
    user_id = sp.current_user()["id"]

    # Create a new private playlist
    playlist_name = "Billboard Hot 100 Playlist"
    playlist_description = "Top songs from Billboard Hot 100"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description=playlist_description)
    
    playlist_id = playlist["id"]

    # Add songs to the playlist
    sp.playlist_add_items(playlist_id, song_uris)
    print(f"Added {len(song_uris)} songs to playlist: {playlist_name+date}")


# Search for a song on Spotify and get its URI
def search_song_on_spotify(sp, song_name):
    search_results = sp.search(q=song_name, type='track', limit=1)

    # Get the first track URI if it exists
    if search_results['tracks']['items']:
        return search_results['tracks']['items'][0]['uri']
    return None


# Scrape Billboard Hot 100 chart
def scrape_billboard_hot_100(date):
    response = rq.get(f"https://www.billboard.com/charts/hot-100/{date}")
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract song names
    song_names_spans = soup.select("li ul li h3")
    song_names = [song.getText().strip() for song in song_names_spans]
    
    return song_names


# Main function to handle everything
def main():
    # Get date input from user
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

    # Scrape the Billboard Hot 100 songs for the given date
    song_names = scrape_billboard_hot_100(date)
    print(f"Scraped {len(song_names)} songs from Billboard Hot 100.")

    # Authenticate to Spotify
    sp = auth_to_spotify()

    # Store URIs of the found songs
    song_uris = []

    # Search for each song on Spotify
    for song_name in song_names:
        uri = search_song_on_spotify(sp, song_name)
        if uri:
            print(f"Found {song_name} on Spotify.")
            song_uris.append(uri)
        else:
            print(f"Could not find {song_name} on Spotify.")

    # If any song URIs were found, create a playlist and add the songs
    if song_uris:
        create_playlist_and_add_tracks(sp, song_uris, date)
    else:
        print("No songs found on Spotify to add to the playlist.")


if __name__ == "__main__":
    main()
