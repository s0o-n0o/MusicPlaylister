from http.client import REQUEST_TIMEOUT
import sys
import spotipy
import spotipy.util as util
from . import info
# import info

scope=("user-read-playback-position user-read-private user-read-email playlist-modify-public playlist-modify-private playlist-read-public playlist-read-private user-library-read user-library-modify user-top-read playlist-read-collaborative ugc-image-upload user-follow-read user-follow-modify user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played")

def token(user_email,scope=None):
    token= spotipy.SpotifyPKCE(username=user_email, scope=scope, client_id=info.SPOTIPY_CLIENTID,redirect_uri=info.SPOTIPY_REDIRECTURI).get_access_token(check_cache=True)
    sp = spotipy.Spotify(auth=token)
    return sp
        