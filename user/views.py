from xml.dom import ValidationErr
from django.shortcuts import render,redirect
from MusicApp.api.user_playlist import Playlist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from . import forms
# Create your views here.
def login(request):
    if request.method == 'POST':
        global playlist 
        username = request.POST["user_name"]
        email = request.POST["email_address"]
        playlist = Playlist(username=username)
        return HttpResponseRedirect('/home')
    return render(request, 'user/login.html')

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('home') #注意
        except ValidationError as e:
            regist_form.add_error('password',e)
    return render(request,'user/regist.html',context={
        'regist_form':regist_form,
    })