import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

client_id = '0a465697c9f94fed90cfdb37cff38052'
client_secret = '6124cc97ca3148a6a9254698f1db5a9e'

def get_playlist():
    scope = "playlist-modify-public "
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = '0a465697c9f94fed90cfdb37cff38052',
                                                    client_secret = '6124cc97ca3148a6a9254698f1db5a9e',
                                                    redirect_uri="http://127.0.0.1:8080/",scope=scope))
    user_id = sp.me()['id']
    # playlist_data = sp.me()['']
    a = sp.user_playlists(user=user_id)
    print(a)
    print("*"*100)
    pprint.pprint(a['items'])
    print("*"*100)
    pprint.pprint(a['items'][0])

get_playlist()

