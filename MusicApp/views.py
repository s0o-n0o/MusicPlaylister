from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from .api.create_playlist import create_playlist
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .api.user_playlist import Playlist

def login(request):
    if request.method == 'POST':
        global username, playlist 
        username = request.POST["user_name"]
        emailaddress = request.POST["email_address"]
        playlist = Playlist(username=username)
        return render(request,"music/home.html")
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

def get_user_tracks(request):
    favorite_tracks =playlist.get_all_saved_tracks() #お気に入りの全曲
    return render(request,'music/all_tracks.html',context={
        'favorite_tracks':favorite_tracks,
    })


def get_playlist_tracks(request,id):
    playlist_id = id
    playlist = playlist.playlist_tracks(playlist_id=playlist_id)
    return render(request, 'music/playlist_tracks.html',context={
        'playlist':playlist,
    })


