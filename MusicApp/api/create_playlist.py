import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import get_track

client_id = '0a465697c9f94fed90cfdb37cff38052'
client_secret = '6124cc97ca3148a6a9254698f1db5a9e'

#Success
def create_playlist(artist,playlist_name,):
    scope = "playlist-modify-public "
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = '0a465697c9f94fed90cfdb37cff38052',
                                                    client_secret = '6124cc97ca3148a6a9254698f1db5a9e',
                                                    redirect_uri="http://127.0.0.1:8080/",scope=scope))
    user_id = sp.me()['id']
    playlists = sp.user_playlist_create(user_id, playlist_name)
    playlist_id = playlists["id"]
    track_ids = get_track.search_artist_id(artist)
    results = sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)
    print(results)

# create_playlist( artist="バウンディ",playlist_name="vaundy")