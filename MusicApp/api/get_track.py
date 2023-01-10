from decimal import MAX_EMAX
from distutils.archive_util import make_archive
from pprint import pprint
from .spotify_auth import token
# from spotify_auth import token

class GetTrack(object):

    def __init__(self,username):
        self.spotify = token(username=username,scope=None)

    # 指定したアーティストのidを返す
    def search_artist_id(self,artist) -> str:
        result_search = self.spotify.search(
            q=artist, type="artist", limit=5)  # get artist_info
        artist_id = result_search["artists"]["items"][0]["id"]
        return artist_id


    #アーティストの人気の10曲を取得
    def get_artist_top_track(self,artist_id) -> dict:
        result = self.spotify.artist_top_tracks(artist_id)
        tracklist = {}
        for track in result["tracks"]:
            tracklist[track['name']] = track['uri']
        return tracklist

    #トラックの特徴量を取得
    def get_track_feature(self,track_id):
        features = self.spotify.audio_features(tracks=track_id)
        # track_analyze = self.spotify.
        for i in range(len(features)):
            feature = {"danceability":features[i]["danceability"], "energy":features[i]["energy"],"valence": features[i]["valence"],
                "acousticness":features[i]["acousticness"],"loudness":features[i]['loudness'],'tempo':features[i]['tempo']}
        return feature

    # #userのトップトラックを取得
    # def get_user_top_tracks(self):
    #     user_id = self.spotify.me()['id']  # get user_id
    #     top_tracks = self.spotify.current_user_top_tracks(time_range='medium_term', limit=20, offset=0)
    #     print(top_tracks)

    #userの最近再生したトラックを取得　

