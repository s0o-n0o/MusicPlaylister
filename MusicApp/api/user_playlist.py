from .spotify_auth import token
from .get_track import GetTrack
from MusicApp.models import SpotifyArtist,SpotifyPlaylist,SpotifyTracks
from user.models import Users
from pprint import pprint
import random

class Playlist(GetTrack):
    #トークン取得
    def __init__(self,user_id,email):
        self.spotify = token(user_email=email,scope="playlist-modify-public user-library-read playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read")
        self.user_id = user_id
        self.email  = email

    #プレイリスト作成
    def create_playlist(self,artist_list,playlist_name):
        sp_user_id = self.spotify.me()['id']  # get user_id
        playlists = self.spotify.user_playlist_create(sp_user_id, playlist_name)  # create playlist
        playlist_id = playlists["id"] #get playlist_id
        for artist in artist_list:
            if artist=='':
                break
            artist_id = self.search_artist_id(artist)
            track_ids = list(self.get_artist_top_track(artist_id).values())
            results = self.spotify.user_playlist_add_tracks(sp_user_id, playlist_id, track_ids)

#ランダムで曲を選択してプレイリスト作成
    def user_random_playlist(self,playlist_name,track_list,number_of_track):
        sp_user_id = self.spotify.me()['id']  # get user_id
        
        random_list = random.sample(track_list,int(number_of_track))
        user_playlist = self.spotify.user_playlist_create(sp_user_id,playlist_name)
        playlist_id = user_playlist["id"] #get playlist_id
        results = self.spotify.user_playlist_add_tracks(sp_user_id, playlist_id, random_list)
        print(random_list)

    #お気に入りの曲取得
    def get_all_saved_tracks(self,limit_step=50):
        #favorite_tracksのプレイリストdbを作成
        playlist,created= SpotifyPlaylist.objects.get_or_create(
                                        user = Users.objects.get(email=self.email),
                                        playlist_name='Favorite Tracks',
                                        playlist_id= f'{self.user_id}_Favorite' #userid_Favorite <- playlist_id
                                        )
        
        for offset in range(0, 1000, limit_step):
            response = self.spotify.current_user_saved_tracks(limit=limit_step, offset=offset,) #お気に入りの曲データを取得
            if len(response) == 0:
                break

            for i in range(len(response['items'])):
                if response['items'][i]['track'] == None :
                    continue
                else:
                    if not SpotifyArtist.objects.filter(artist_id = response['items'][i]['track']['artists'][0]['id']).exists():
                        artist,create = SpotifyArtist.objects.create(
                            artist_id = response['items'][i]['track']['artists'][0]['id'],
                            artist_name= response['items'][i]['track']['artists'][0]['name'],
                            )
                    else:
                        artist = SpotifyArtist.objects.get(artist_id=response['items'][i]['track']['artists'][0]['id'])
                        
                    playlist_track_id = response['items'][i]['track']['id'] #id取得
                    playlist_track_feature = self.get_track_feature(playlist_track_id)

                    track,created = SpotifyTracks.objects.get_or_create(
                        track_id= response['items'][i]['track']['id'],
                        track_name= response['items'][i]['track']['name'],
                        artist =  artist,
                        danceability=playlist_track_feature['danceability'],
                        energy=playlist_track_feature['energy'],
                        valence=playlist_track_feature['valence'],
                        acousticness=playlist_track_feature['acousticness'],
                        loudness=playlist_track_feature['loudness'],
                        tempo=playlist_track_feature['tempo'],
                        )
                    track.playlist.add(playlist)


    #全プレイリスト取得
    def get_playlist(self,user_id):
        def differential_adjustment(current_db_playlists, spotify_playlists):
        # 削除されたプレイリストを更新時にDBから削除する
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

        sp_user_id =self.spotify.me()['id']
        current_playlist = SpotifyPlaylist.objects.filter(user_id=user_id) #db内
        user_playlist_info = self.spotify.user_playlists(user=sp_user_id) #spotify内
        current_playlist_name = current_playlist.values('playlist_id')
        current_playlist_name = [current_playlist_name[i]['playlist_id'] for i in range(len(current_playlist_name))]
        user_playlists = [user_playlist_info['items'][i]["id"] for i in range(len(user_playlist_info['items']))]

        # db内にspotifyのプレイリストがないときにカラム作成
        for i in range(len(user_playlist_info['items'])):
            if not user_playlist_info['items'][i]['name'] in current_playlist_name:
                playlist,created= SpotifyPlaylist.objects.get_or_create(
                                        user = Users.objects.get(email=self.email),
                                        playlist_name=user_playlist_info['items'][i]['name'],
                                        playlist_id= user_playlist_info['items'][i]['id']
                                        )
        differential_adjustment(current_db_playlists=current_playlist_name,spotify_playlists=user_playlists)
        

    
        


    #指定されたプレイリスト内のトラックを取得し、DBに追加
    def playlist_tracks(self,playlist_id) -> list:
        playlist_tracks = self.spotify.playlist_items(playlist_id=playlist_id) #spotifyのプレイリストのトラックを取得
        playlist = SpotifyPlaylist.objects.get(playlist_id=playlist_id,user_id=self.user_id) #db内のプレイリストを取得
        
        current_tracks = SpotifyTracks.objects.filter(playlist=playlist)
        if not len(current_tracks)==len(playlist_tracks['items']):
            for i in range(len(playlist_tracks['items'])):
                if playlist_tracks['items'][i]['track'] == None:
                    continue
                else:
                    if not SpotifyArtist.objects.filter(artist_id = playlist_tracks['items'][i]['track']['artists'][0]['id']).exists():
                        artist,create = SpotifyArtist.objects.create(
                            artist_id = playlist_tracks['items'][i]['track']['artists'][0]['id'],
                            artist_name= playlist_tracks['items'][i]['track']['artists'][0]['name'],
                            )
                    else:
                        artist = SpotifyArtist.objects.get(artist_id=playlist_tracks['items'][i]['track']['artists'][0]['id'])
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

    def get_user_recently_played(self,limit_step=50):
        # result = self.spotify.current_user_recently_played()
        for offset in range(0, 1000,limit_step):
            result = self.spotify.current_user_top_tracks(limit=limit_step,offset=offset)
            if len(result) == 0:
                break
            for i in range(len(result['items'])):
                print(result['items'][i]['name'])
        # return result