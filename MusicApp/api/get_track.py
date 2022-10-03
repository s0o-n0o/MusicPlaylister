import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

client_id = '82352952d43e4c0e8edde1b08667a646'
client_secret = '4a4cfaca9d2446e78ea14f0a81e21349'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret, )
spotify = spotipy.Spotify(auth_manager=client_credentials_manager)


def search_artist_id(artist) -> dict:
    result_search = spotify.search(
        q=artist, type="artist", limit=5)  # get artist_info
    artist_id = result_search["artists"]["items"][0]["id"]
    track_top10_list = get_artist_top_track(artist_id=artist_id)
    return track_top10_list


def get_artist_top_track(artist_id) -> dict:
    result = spotify.artist_top_tracks(artist_id)
    tracklist = {}
    for track in result["tracks"]:
        tracklist[track['name']] = track['uri']
    return tracklist


# test
search_artist_id("マカロニえんぴつ")
