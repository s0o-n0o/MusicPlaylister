from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .api.create_playlist import create_playlist
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .api.get_user_playlist import get_playlist, get_all_saved_tracks, playlist_tracks


def home(request):
    playlists = get_playlist()
    return render(request, 'music/home.html',context={
        "playlists":playlists ,#dict
    })


def login(request):
    if request.method == 'GET':
        print(request.GET.get("query_param"))
    return render(request, 'music/login.html')


def create(request):
    if request.method == "POST":
        artist_list = request.POST.getlist("artist")
        playlist_name = request.POST["playlist_name"]
        create_playlist(artist_list=artist_list, playlist_name=playlist_name)
        return HttpResponseRedirect('/home')
    
    return render(request, "music/create.html")

def get_user_tracks(request):
    favorite_tracks = get_all_saved_tracks() #お気に入りの全曲
    return render(request,'music/all_tracks.html',context={
        'favorite_tracks':favorite_tracks,
    })


def get_playlist_tracks(request,id):
    playlist_id = id
    playlist = playlist_tracks(playlist_id=playlist_id)
    return render(request, 'music/playlist_tracks.html',context={
        'playlist':playlist,
    })


