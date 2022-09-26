from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .api.create_playlist import create_playlist
from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request,'music/home.html')

def login(request):
    if request.method == 'GET':
        print(request.GET.get("query_param"))
    return render(request,'music/login.html')

def create(request):
    if request.method == "POST":
        artist=request.POST["artist"]
        playlist_name= request.POST["playlist_name"]
        create_playlist(artist=artist,playlist_name=playlist_name)
        return render(request,"music/home.html")
    return render(request,"music/create.html")
