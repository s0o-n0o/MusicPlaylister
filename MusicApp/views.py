from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from .api.create_playlist import create_playlist
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .api.user_playlist import Playlist
from MusicApp.models import SpotifyArtist,SpotifyPlaylist,SpotifyTracks
from user.models import Users
from django.core.cache import cache
from django.contrib import messages




def base(request):
    return render(request,"music/base.html")

@login_required
def home(request):
    user_id = request.user.id      #重複する可能性あり
    user_email= request.user.email #ユニーク
    if user_id == None:
        return HttpResponseRedirect('/user_login')

    sp_playlist = Playlist(user_id=user_id,email=user_email)
    sp_playlist.get_playlist(user_id=user_id) 
    sp_playlist.get_user_recently_played()
    playlists=SpotifyPlaylist.objects.filter(user_id=user_id)
    return render(request, 'music/home.html',context={
        "playlists":playlists ,#dict
    })

@login_required
def create(request):
    sp_playlist = Playlist(user_id=request.user.id,email=request.user.email)
    if request.method == "POST":
        artist_list = request.POST.getlist("artist")
        playlist_name = request.POST["playlist_name"]

        #valid
        artist_none_flag = False
        for i in range(len(artist_list)):
            if artist_list[i] != "":
                artist_none_flag = True
        if artist_none_flag == False:
            messages.warning(request,'アーティストを入力してください')
        if playlist_name == "":
            messages.error(request,'プレイリスト名を入力してください')
        if  artist_none_flag==False or playlist_name == "":    
            return render(request, "music/create.html")

        #success
        sp_playlist.create_playlist(artist_list=artist_list, playlist_name=playlist_name)
        for artist in artist_list:
            if artist=='':
                break
            artist_id = sp_playlist.search_artist_id(artist)
            track_ids = list(sp_playlist.get_artist_top_track(artist_id).values())
        return HttpResponseRedirect('/home')

    return render(request, "music/create.html",context={
    })


@login_required
def random_playlist_create(request):    
    sp_playlist = Playlist(user_id=request.user.id,email=request.user.email)
    #全トラック取得
    playlists=  SpotifyPlaylist.objects.filter(user_id=request.user.id)        
    all_playlist_tracks ={}
    for playlist_data in playlists:
        sp_playlist.playlist_tracks(playlist_id=playlist_data.playlist_id)
    
    # 全曲数カウント
    track_list=[]
    number_of_track = 0
    for i in range(len(playlists)):
        playlist = SpotifyPlaylist.objects.get(playlist_name=playlists[i].playlist_name)
        playlist_track_all = playlist.spotifytracks.all()
        for track in playlist_track_all:
            track_id = track.track_id
            track_list.append(track_id)
    track_list = list(set(track_list))
    number_of_track = len(track_list)

    if request.method == "POST":
        playlist_name = request.POST["playlist_name"]
        number_of_track = request.POST["number_of_track"]
        #valid
        if playlist_name == "":
            messages.error(request,'プレイリスト名を入力してください')
            return render(request, "music/user_randomplaylist_create.html")
        #success
        sp_playlist.user_random_playlist(playlist_name=playlist_name,track_list=track_list,number_of_track=number_of_track)
        return HttpResponseRedirect('/home')

    return render(request, "music/user_randomplaylist_create.html",context={
        "number_of_track":number_of_track,
        })

@login_required
def get_user_favorite_tracks(request):
    sp_playlist = Playlist(user_id=request.user.id,email=request.user.email)
    favorite_tracks =sp_playlist.get_all_saved_tracks() #お気に入りの全曲
    # favorite_tracks=  SpotifyTracks.playlist(plylist_id=f'{request.user.id}_Favorite')
    favorite_list = SpotifyPlaylist.objects.get(playlist_id=f'{request.user.id}_Favorite').id
    favorite_tracks = SpotifyTracks.objects.filter(playlist=favorite_list)

    return render(request,'music/favorite_tracks.html',context={
        'favorite_tracks':favorite_tracks,
    })


@login_required
def get_playlist_tracks(request,id):
    sp_playlist = Playlist(user_id=request.user.id,email=request.user.email)
    playlist_id = id
    sp_playlist.playlist_tracks(playlist_id=playlist_id)
    playlist_tracks = SpotifyTracks.objects.all()
    tracks = []
    for track in playlist_tracks:
        if track.playlist.filter(playlist_id=playlist_id):
            tracks.append(track)
    
    return render(request, 'music/playlist_tracks.html',context={
        'playlist_tracks':tracks,
    })


@login_required
def user_alltracks(request):
    playlists=  SpotifyPlaylist.objects.filter(user_id=request.user.id)
    all_playlist_tracks =[]
    for i in range(len(playlists)):
        playlist = SpotifyPlaylist.objects.get(playlist_name=playlists[i].playlist_name)
        playlist_track_all = playlist.spotifytracks.all()
        for track in playlist_track_all:
            all_playlist_tracks.append(track)

    return render(request,'music/user_all_tracks.html',context={
        'user_alltracks':all_playlist_tracks,
    })


def page_not_found(request,exception):
    return render(request,'music/404.html',status=404)
