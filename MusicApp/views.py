from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from .api.create_playlist import create_playlist
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .api.user_playlist import Playlist


def login(request):
    if request.method == 'POST':
        global playlist 
        username = request.POST["user_name"]
        email = request.POST["email_address"]
        playlist = Playlist(username=username)
        return HttpResponseRedirect('/home')
    return render(request, 'music/login.html')


def home(request):
    playlists = playlist.get_playlist()
    return render(request, 'music/home.html',context={
        "playlists":playlists ,#dict
    })


def create(request):
    if request.method == "POST":
        artist_list = request.POST.getlist("artist")
        playlist_name = request.POST["playlist_name"]
        playlist.create_playlist(artist_list=artist_list, playlist_name=playlist_name)
        return HttpResponseRedirect('/home')
    return render(request, "music/create.html")


def get_user_favorite_tracks(request):
    favorite_tracks =playlist.get_all_saved_tracks() #お気に入りの全曲
    return render(request,'music/favorite_tracks.html',context={
        'favorite_tracks':favorite_tracks,
    })


def get_playlist_tracks(request,id):
    playlist_id = id
    playlist_tracks = playlist.playlist_tracks(playlist_id=playlist_id)
    # print(playlist_tracks)
        #[ { name; {id:id,artist:artist} , {id:id,artist:artist} ,...} ]
    return render(request, 'music/playlist_tracks.html',context={
        'playlist_tracks':playlist_tracks,
    })


# playlist.playlist_tracks()
def logout(request):
    del playlist
    return HttpResponseRedirect("")

def user_alltracks(request):
    # {"playlist":[{ name; {id:id,artist:artist} , {name:{id:id,artist:artist}} ,...}]}
    user_alltracks =playlist.user_all_tracks()
    print(user_alltracks)
    return render(request,'music/user_all_tracks.html',context={
        'user_alltracks':user_alltracks,

    })

