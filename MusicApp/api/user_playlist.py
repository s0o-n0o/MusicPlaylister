import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
import os
from .spotify_auth import token
from .get_track import GetTrack

class Playlist(GetTrack):
    def __init__(self,username):
        self.spotify = token(username=username,scope="playlist-modify-public user-library-read")

    def create_playlist(self,artist_list, playlist_name):
        user_id = self.spotify.me()['id']  # get user_id
        playlists = self.spotify.user_playlist_create(user_id, playlist_name)  # create playlist
        playlist_id = playlists["id"]
        for artist in artist_list:
            if artist=='':
                break
            artist_id = self.search_artist_id(artist)
            track_ids = list(self.get_artist_top_track(artist_id).values())
            results = self.spotify.user_playlist_add_tracks(user_id, playlist_id, track_ids)

    def get_playlist(self) -> dict:
        user_id =self.spotify.me()['id']
        user_playlist_info = self.spotify.user_playlists(user=user_id)
        playlists_info = {}
        for i in range(len(user_playlist_info['items'])):
            playlists_info[user_playlist_info['items'][i]
                        ['name']] = user_playlist_info['items'][i]['id']
        return playlists_info


    def get_all_saved_tracks(self,limit_step=50) -> list:
        tracks = []
        for offset in range(0, 1000, limit_step):
            response = self.spotify.current_user_saved_tracks(limit=limit_step, offset=offset,)
            if len(response) == 0:
                break
            for i in range(len(response['items'])):
                tracks.append(response['items'][i]['track']['name'])
        return tracks


    def playlist_tracks(self,playlist_id) -> list:
        playlist = []
        playlist_tracks = self.spotify.playlist_items(playlist_id=playlist_id)
        for i in range(len(playlist_tracks['items'])):
            if playlist_tracks['items'][i]['track'] == None:
                continue
            else:
                playlist_track = playlist_tracks['items'][i]['track']['name']
                playlist.append(playlist_track)
        return playlist
        
