from django.shortcuts import render,redirect
from MusicApp.api.user_playlist import Playlist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from . import forms
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email= login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        print(email)
        print(password)
        user = authenticate(email=email,password=password)
        print(user)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request,'ログインしました')
                return redirect('music_app:home')
            else:
                messages.warning(request,'ユーザがアクティブではありません')
        else:
            messages.warning(request,'メールアドレスかパスワードが間違っています')
    return render(request, 'user/login.html',context={
        'login_form':login_form,
    })
    
    # if request.method == 'POST':
    #     global playlist 
    #     username = request.POST["user_name"]
    #     email = request.POST["email_address"]
    #     playlist = Playlist(username=username)
    #     return HttpResponseRedirect('')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'ログアウトしました')
    return redirect('music_app:base')

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('user:activate_user') #注意
        except ValidationError as e:
            regist_form.add_error('password',e)
    return render(request,'user/regist.html',context={
        'regist_form':regist_form,
    })

def activate_user(request,token):
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
    return render(request,'user/activate_user.html')