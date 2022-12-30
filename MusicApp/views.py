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
    global playlist,user_id,user_email
    user_id = request.user.id #重複する可能性あり
    # print(user_id)
    user_email= request.user.email #ユニーク
    if user_id == None:
        return HttpResponseRedirect('/user_login')
    playlist = Playlist(user_id=user_id,email=user_email)
    playlist.get_playlist(id=user_id) #dict
    playlists=SpotifyPlaylist.objects.filter(user_id=user_id)
    return render(request, 'music/home.html',context={
        "playlists":playlists ,#dict
    })

@login_required
def create(request):

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
        playlist.create_playlist(artist_list=artist_list, playlist_name=playlist_name)

        return HttpResponseRedirect('/home')
    return render(request, "music/create.html")

@login_required
def get_user_favorite_tracks(request):
    favorite_tracks =playlist.get_all_saved_tracks() #お気に入りの全曲
    return render(request,'music/favorite_tracks.html',context={
        'favorite_tracks':favorite_tracks,
    })

@login_required
def get_playlist_tracks(request,id):
    playlist_id = id
    playlist.playlist_tracks(playlist_id=playlist_id,user_id=request.user.id)
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
    for playlist_data in playlists:
        playlist.playlist_tracks(playlist_id=playlist_data.playlist_id, user_id=request.user.id)
    user_alltracks =  SpotifyTracks.objects.filter()
    # user_alltracks = alltracks.filter(playlist = playlists)
    print(user_alltracks)
    count= len(user_alltracks)
    
    return render(request,'music/user_all_tracks.html',context={
        'user_alltracks':user_alltracks,
        'count':count
    })

def play_track(request,track_id):
    pass



def page_not_found(request,exception):
    return render(request,'music/404.html',status=404)
