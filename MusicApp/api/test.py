from pprint import pprint
import spotipy
import spotipy.util as util
import info
from spotipy.oauth2 import SpotifyOAuth
from models import SpotifyArtist,SpotifyPlaylist,SpotifyTracks

# from user_playlist import Playlist


# token= util.prompt_for_user_token(username="lcl", scope="user-modify-playback-state user-read-playback-state user-read-currently-playing user-read-recently-played", client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)
# sp = spotipy.Spotify(auth=token)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI,
                                                scope="user-modify-playback-state user-read-playback-state user-read-currently-playing user-read-recently-played"))
user_id =sp.me()['id']
user_playlist_info = sp.user_playlists(user=user_id)['items']
tracks = sp.user_playlist_tracks(playlist_id="01ujVQzL0iEUVDafFXBJe9")
# sp_recommend= sp.featured_playlists()#おすすめのプレイリスト　
# pl_cover = sp.playlist_cover_image(playlist_id="01ujVQzL0iEUVDafFXBJe9") #プレイリストのカバー画像取得
tracks = SpotifyTracks.objects.get(pk=1)
print(tracks)
# features = sp.audio_analysis(track_id='4b6txnDj8rrMgw3gXlFP6x')
# sp.start_playback(device_id="30cdf9d1c06ea770e45246d0889ce391b3fa2f8d",uris = ['spotify:track:2FZXuCw75FYVfiNHtFQON9'])
# devices =sp.devices() #デバイスID取得
# print(devices)
# for i in range(len(features)):
#     feature = {"danceability":features[i]["danceability"], "energy":features[i]["energy"],"valence": features[i]["valence"],
#                 "acousticness":features[i]["acousticness"],"loudness":features[i]['loudness'],'tempo':features[i]['tempo']}
#     max_feature = max(feature,key=feature.get)
# pprint(tracks)
# pprint(max_feature)
# playlists_info = {}
# all_tracks={}
