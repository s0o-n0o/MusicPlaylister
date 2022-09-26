import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import sys
import json

client_id = '0a465697c9f94fed90cfdb37cff38052'
client_secret = '6124cc97ca3148a6a9254698f1db5a9e'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret, )
spotify = spotipy.Spotify(auth_manager=client_credentials_manager)

def search_artist_id(artist):
    result_search=spotify.search(q=artist,type="artist",limit=5) #get artist_info
    artist_id=result_search["artists"]["items"][0]["id"]
    track_ids = get_artist_top_track(artist_id=artist_id) 
    return track_ids

def get_artist_top_track(artist_id):
    result = spotify.artist_top_tracks(artist_id)
    track_ids=[] 
    for track in result["tracks"]:
        track_ids.append(track['uri'])
    return track_ids





#test
# search_artist_id("マカロニえんぴつ")




