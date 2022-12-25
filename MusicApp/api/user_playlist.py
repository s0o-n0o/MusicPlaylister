from .spotify_auth import token
from .get_track import GetTrack
from MusicApp.models import SpotifyArtist,SpotifyPlaylist,SpotifyTracks
from user.models import Users
from pprint import pprint

class Playlist(GetTrack):
    #トークン取得
    def __init__(self,user_id,email):
        self.spotify = token(user_email=email,scope="playlist-modify-public user-library-read playlist-modify-private playlist-read-private playlist-read-collaborative")
        self.user_id = user_id
        self.email  = email

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
    def get_playlist(self,id) -> dict:

        def differential_adjustment(current_db_playlists, spotify_playlists):
            delete_list = []
            for db in current_db_playlists:
                existflag = False
                for sp in spotify_playlists:
                    if db == sp:
                        existflag =True
                if existflag == False:
                    delete_list.append(db)
            for delete in delete_list:
                SpotifyPlaylist.objects.filter(playlist_id = delete).delete()


        user_id =self.spotify.me()['id']
        # print(user_id)
        current_playlist = SpotifyPlaylist.objects.filter(user_id=id) #db内
        user_playlist_info = self.spotify.user_playlists(user=user_id) #spotify内
        # print(current_playlist_name)
        # print(user_playlist_info)
        current_playlist_name = current_playlist.values('playlist_id')
        current_playlist_name = [current_playlist_name[i]['playlist_id'] for i in range(len(current_playlist_name))]
        user_playlists = [user_playlist_info['items'][i]["id"] for i in range(len(user_playlist_info['items']))]
        # print(user_playlists)
        # print(current_playlist_name)
        # db内にspotifyのプレイリストがないときにカラム作成
        for i in range(len(user_playlist_info['items'])):
            if not user_playlist_info['items'][i]['name'] in current_playlist_name:
                playlist,created= SpotifyPlaylist.objects.get_or_create(
                                        user = Users.objects.get(email=self.email),
                                        playlist_name=user_playlist_info['items'][i]['name'],
                                        playlist_id= user_playlist_info['items'][i]['id']
                                        )
        differential_adjustment(current_db_playlists=current_playlist_name,spotify_playlists=user_playlists)
        
        

        
            

    
            


    #プレイリスト内の全曲取得
    def playlist_tracks(self,playlist_id,user_id) -> list:
        playlist_tracks = self.spotify.playlist_items(playlist_id=playlist_id)
        playlist = SpotifyPlaylist.objects.get(playlist_id=playlist_id,user_id=user_id)
        current_tracks = SpotifyTracks.objects.filter(playlist=playlist)

        if not len(current_tracks)==len(playlist_tracks['items']):
            for i in range(len(playlist_tracks['items'])):
                if playlist_tracks['items'][i]['track'] == None:
                    continue
                else:
                    artist,create = SpotifyArtist.objects.get_or_create(
                        artist_id = playlist_tracks['items'][i]['track']['artists'][0]['id'],
                        artist_name= playlist_tracks['items'][i]['track']['artists'][0]['name'],
                        )
                    playlist_track_id = playlist_tracks['items'][i]['track']['id'] #id取得
                    playlist_track_feature = self.get_track_feature(playlist_track_id)

                    track,created = SpotifyTracks.objects.get_or_create(
                        track_id= playlist_tracks['items'][i]['track']['id'],
                        track_name= playlist_tracks['items'][i]['track']['name'],
                        artist =  artist,
                        danceability=playlist_track_feature['danceability'],
                        energy=playlist_track_feature['energy'],
                        valence=playlist_track_feature['valence'],
                        acousticness=playlist_track_feature['acousticness'],
                        loudness=playlist_track_feature['loudness'],
                        tempo=playlist_track_feature['tempo'],
                        )
                    track.playlist.add(playlist)

    #ユーザのプレイリスト内にある全曲
    def user_all_tracks(self) -> dict:
        all_tracks = {}
        playlist= self.get_playlist()
        for playlist_name,playlist_id in playlist.items():
            all_tracks[playlist_name] = self.playlist_tracks(playlist_id=playlist_id)
        # {"playlist":[{ name; {id:id,artist:artist}} ,{name:{id:id,artist:artist} ,...}], [{name; {id:id,artist:artist} ,{id:id,artist:artist} ,...}]}
        return all_tracks
