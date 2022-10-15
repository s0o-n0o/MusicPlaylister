import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import get_track
import os
import info

client_id = info.SPOTIPY_CLIENTID
client_secret = info.SPOTIPY_SECRET
redirect_uri = info.SPOTIPY_SECRET
# Success


def create_playlist(artist_list, playlist_name):
    scope = "playlist-modify-public "
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri, scope=scope))
    user_id = sp.me()['id']  # get user_id
    playlists = sp.user_playlist_create(user_id, playlist_name)  # create playlist
    playlist_id = playlists["id"]
    # print(artist_list)
    for artist in artist_list:
        if artist=='':
            break
        track_ids = list(get_track.search_artist_id(artist).values())
        results = sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)
    
    # print(results)


# create_playlist(artist="バウンディ", playlist_name="vaundy")


        