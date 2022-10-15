import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import os
import info

client_id = info.SPOTIPY_CLIENTID
client_secret = info.SPOTIPY_SECRET
redirect_uri = info.SPOTIPY_SECRET



class GetTrack(object):

    def __init__(self) -> None:
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotify = spotipy.Spotify(auth_manager=client_credentials_manager,language="ja")


    # 指定したアーティストのidを返す
    def search_artist_id(self,artist) -> str:
        result_search = self.spotify.search(
            q=artist, type="artist", limit=5)  # get artist_info
        artist_id = result_search["artists"]["items"][0]["id"]
        return artist_id
        # track_top10_list = self.get_artist_top_track(artist_id=artist_id)
        # return track_top10_list

    #
    def get_artist_top_track(self,artist_id) -> dict:
        result = self.spotify.artist_top_tracks(artist_id)
        tracklist = {}
        for track in result["tracks"]:
            tracklist[track['name']] = track['uri']
        return tracklist



# test
# search_artist_id("マカロニえんぴつ")

