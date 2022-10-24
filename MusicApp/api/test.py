from pprint import pprint
import spotipy
import spotipy.util as util
import info
# from user_playlist import Playlist


token= util.prompt_for_user_token(username="lcl", scope="playlist-modify-public user-library-read", client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)
sp = spotipy.Spotify(auth=token)
user_id =sp.me()['id']
user_playlist_info = sp.user_playlists(user=user_id)['items']
tracks = sp.user_playlist_tracks(playlist_id="01ujVQzL0iEUVDafFXBJe9")
# pprint(user_playlist_info)
pprint(tracks['items'])
features = sp.audio_features(tracks='4b6txnDj8rrMgw3gXlFP6x')
for i in range(len(features)):
    feature = {"danceability":features[i]["danceability"], "energy":features[i]["energy"],"valence": features[i]["valence"],
                "acousticness":features[i]["acousticness"],"loudness":features[i]['loudness'],'tempo':features[i]['tempo']}
    max_feature = max(feature,key=feature.get)
pprint(features)
pprint(max_feature)
# playlists_info = {}
# all_tracks={}

# p = {"playlist":[{"id":'id',"info":{'name':"ai",'artist':"ia"}}}]
# p2 =p["playlist"]['track']
# for key,value in p2.items():
# print("{}:{}".format(key,value))
