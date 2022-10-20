from pprint import pprint
import spotipy
import spotipy.util as util
import info
# from user_playlist import Playlist


token= util.prompt_for_user_token(username="lcl", scope="playlist-modify-public user-library-read", client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)
sp = spotipy.Spotify(auth=token)
user_id =sp.me()['id']
user_playlist_info = sp.user_playlists(user=user_id)['items'][]
pprint(user_playlist_info)
playlists_info = {}
all_tracks={}

