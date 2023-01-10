from .spotify_auth import token
from .get_track import GetTrack
from MusicApp.models import SpotifyArtist,SpotifyPlaylist,SpotifyTracks
from user.models import Users
from pprint import pprint

class TrackPlay(object):
    def __init__(self,user_id,email):
        self.spotify = token(user_email=email,scope="playlist-modify-public user-library-read playlist-modify-private playlist-read-private playlist-read-collaborative")
        self.user_id = user_id
        self.email  = email
        
    def pause():
        pass
    
    def next():
        pass
    
        
