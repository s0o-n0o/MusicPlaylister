from .spotify_auth import token
from .get_track import GetTrack

class Playlist(GetTrack):
    #トークン取得
    def __init__(self,username):
        self.spotify = token(username=username,scope="playlist-modify-public user-library-read")

    #プレイリスト作成
    def create_playlist(self,artist_list, playlist_name):
        user_id = self.spotify.me()['id']  # get user_id
        playlists = self.spotify.user_playlist_create(user_id, playlist_name)  # create playlist
        playlist_id = playlists["id"] #get playlist_id
        for artist in artist_list:
            if artist=='':
                break
            artist_id = self.search_artist_id(artist)
            track_ids = list(self.get_artist_top_track(artist_id).values())
            results = self.spotify.user_playlist_add_tracks(user_id, playlist_id, track_ids)

    #お気に入りの曲取得
    def get_all_saved_tracks(self,limit_step=50) -> list:
        tracks = []
        for offset in range(0, 1000, limit_step):
            response = self.spotify.current_user_saved_tracks(limit=limit_step, offset=offset,)
            if len(response) == 0:
                break
            for i in range(len(response['items'])):
                tracks.append(response['items'][i]['track']['name'])
        return tracks


    #全プレイリスト取得
    def get_playlist(self) -> dict:
        user_id =self.spotify.me()['id']
        user_playlist_info = self.spotify.user_playlists(user=user_id)
        playlists_info = {}
        for i in range(len(user_playlist_info['items'])):
            playlists_info[user_playlist_info['items'][i]['name']] = user_playlist_info['items'][i]['id']
        return playlists_info

    #プレイリスト内の全曲取得
    def playlist_tracks(self,playlist_id) -> list:
        info = []
        track_info ={}
        playlist_tracks = self.spotify.playlist_items(playlist_id=playlist_id)
        # print(len(playlist_tracks['items']))
        for i in range(len(playlist_tracks['items'])):
            if playlist_tracks['items'][i]['track'] == None:
                continue
            else:
                playlist_track = playlist_tracks['items'][i]['track']['name'] #トラック名取得
                playlist_track_artist = playlist_tracks['items'][i]['track']['artists'][0]['name'] # artist名取得
                playlist_track_id = playlist_tracks['items'][i]['track']['id'] #id取得
                playlist_track_feature = self.get_track_feature(playlist_track,playlist_track_id)[playlist_track_id]
                track_info[playlist_track] = {"id":playlist_track_id,'artist':playlist_track_artist,'feature':playlist_track_feature}
        info.append(track_info)
        # print(info)
        #[ { name; {id:id,artist:artist} , {name:{id:id,artist:artist}} ,...} ]
        return info

    #ユーザのプレイリスト内にある全曲
    def user_all_tracks(self) -> dict:
        all_tracks = {}
        playlist= self.get_playlist()
        for playlist_name,playlist_id in playlist.items():
            all_tracks[playlist_name] = self.playlist_tracks(playlist_id=playlist_id)
        # {"playlist":[{ name; {id:id,artist:artist}} ,{name:{id:id,artist:artist} ,...}], [{name; {id:id,artist:artist} ,{id:id,artist:artist} ,...}]}
        return all_tracks
