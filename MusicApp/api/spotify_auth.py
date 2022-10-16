import sys
import spotipy
import spotipy.util as util
from . import info

scope=("user-read-playback-position user-read-private user-read-email playlist-modify-public playlist-modify-private playlist-read-public playlist-read-private user-library-read user-library-modify user-top-read playlist-read-collaborative ugc-image-upload user-follow-read user-follow-modify user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played")

def token(username,scope):
    if scope :
        token= util.prompt_for_user_token(username=username, scope=scope, client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)
        sp = spotipy.Spotify(auth=token)
        return sp
    else:
        token= util.prompt_for_user_token(username=username, scope=None, client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)
        sp = spotipy.Spotify(auth=token)
        return sp