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



def base(request):
    return render(request,"music/base.html")

@login_required
def home(request):
    username = request.user.username
    if username == None:
        return HttpResponseRedirect('/user_login')
    global playlist
    playlist = Playlist(username=username)
    playlist.get_playlist() #dict
    playlists=SpotifyPlaylist.objects.all()
    # for playlist_data in playlists.values():
    #     playlist.playlist_tracks(playlist_data['playlist_id'])
    return render(request, 'music/home.html',context={
        "playlists":playlists ,#dict
    })

@login_required
def create(request):
    if request.method == "POST":
        artist_list = request.POST.getlist("artist")
        playlist_name = request.POST["playlist_name"]
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
    playlist_tracks = SpotifyTracks.objects.all()
    tracks = []
    for track in playlist_tracks:
        if track.playlist.filter(playlist_id=playlist_id):
            tracks.append(track)
    
    #[ { name; {id:id,artist:artist} , {id:id,artist:artist} ,...} ]
    return render(request, 'music/playlist_tracks.html',context={
        'playlist_tracks':tracks,
    })


# playlist.playlist_tracks()
@login_required
def user_alltracks(request):
    # {"playlist":[{ name; {id:id,artist:artist} , {name:{id:id,artist:artist}} ,...}]}
    # user_alltracks =playlist.user_all_tracks()
    user_alltracks =  SpotifyTracks.objects.all()
    playlists=  SpotifyPlaylist.objects.all()
    # for track in user_alltracks:
    #     for playlist in playlists:
    #         print(track.playlist.filter(playlist_id = playlist.playlist_id))
    return render(request,'music/user_all_tracks.html',context={
        'user_alltracks':user_alltracks,
    })


def page_not_found(request,exception):
    return render(request,'music/404.html',status=404)
