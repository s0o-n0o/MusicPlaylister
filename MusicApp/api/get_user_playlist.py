import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

client_id = '82352952d43e4c0e8edde1b08667a646'
client_secret = '4a4cfaca9d2446e78ea14f0a81e21349'


def get_playlist() -> dict:
    scope = "playlist-modify-public "
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://127.0.0.1:8080/callback", scope=scope))
    user_id = sp.me()['id']
    user_playlist_info = sp.user_playlists(user=user_id)
    playlists_info = {}
    for i in range(len(user_playlist_info['items'])):
        playlists_info[user_playlist_info['items'][i]
                       ['name']] = user_playlist_info['items'][i]['id']
    return playlists_info


# get_tracks()

def get_all_saved_tracks(limit_step=50) -> list:
    scope = "playlist-modify-public user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://127.0.0.1:8080/callback", scope=scope))
    tracks = []
    for offset in range(0, 1000, limit_step):
        response = sp.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )
        if len(response) == 0:
            break
        for i in range(len(response['items'])):
            tracks.append(response['items'][i]['track']['name'])
    return tracks


def playlist_tracks(playlist_id='UP') -> list:
    scope = "playlist-modify-public user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://127.0.0.1:8080/callback", scope=scope))
    playlist = []
    playlist_tracks = sp.playlist_items(playlist_id=playlist_id)
    for i in range(len(playlist_tracks['items'])):
        if playlist_tracks['items'][i]['track'] == None:
            continue
        else:
            playlist_track = playlist_tracks['items'][i]['track']['name']
            playlist.append(playlist_track)
    return playlist
    
# get_playlist_tracks()
# get_all_saved_tracks()
# get_playlist()
