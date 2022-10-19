import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import os
from .spotify_auth import token
# from spotify_auth import token



class GetTrack(object):

    def __init__(self,username):
        self.spotify = token(username=username,scope=None)

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

# get_track = GetTrack(username="lcl").search_artist_id("vaundy")
# print(get_track)

# test
# search_artist_id("マカロニえんぴつ")

