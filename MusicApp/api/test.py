from pprint import pprint
import spotipy
import spotipy.util as util
import info
# from user_playlist import Playlist


token= util.prompt_for_user_token(username="lcl", scope="playlist-modify-public user-library-read user-read-playback-state user-modify-playback-state", client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)
sp = spotipy.Spotify(auth=token)
user_id =sp.me()['id']
user_playlist_info = sp.user_playlists(user=user_id)['items']
tracks = sp.user_playlist_tracks(playlist_id="01ujVQzL0iEUVDafFXBJe9")
# sp_recommend= sp.featured_playlists()#おすすめのプレイリスト　
# pl_cover = sp.playlist_cover_image(playlist_id="01ujVQzL0iEUVDafFXBJe9") #プレイリストのカバー画像取得

# features = sp.audio_analysis(track_id='4b6txnDj8rrMgw3gXlFP6x')
sp.start_playback(device_id="30cdf9d1c06ea770e45246d0889ce391b3fa2f8d",context_uri=['6ocYdFNcNTRJkEA1OB94EE'])
# devices =sp.devices()
# print(devices)
# for i in range(len(features)):
#     feature = {"danceability":features[i]["danceability"], "energy":features[i]["energy"],"valence": features[i]["valence"],
#                 "acousticness":features[i]["acousticness"],"loudness":features[i]['loudness'],'tempo':features[i]['tempo']}
#     max_feature = max(feature,key=feature.get)
# pprint(tracks)
# pprint(max_feature)
# playlists_info = {}
# all_tracks={}
