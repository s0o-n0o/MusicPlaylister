from audioop import reverse
from urllib.parse import urlencode
from django.shortcuts import render,redirect
from MusicApp.api.user_playlist import Playlist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from .models import UserActivateTokens, Users
from . import forms
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email= login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email,password=password)
        if user:
            if user.is_active:
                login(request,user)
                # messages.success(request,'ログインしました')
                return redirect('music_app:home')
            else:
                messages.warning(request,'ユーザがアクティブではありません')
        else:
            messages.warning(request,'メールアドレスかパスワードが間違っています')
    return render(request, 'user/login.html',context={
        'login_form':login_form,
    })

@login_required
def user_logout(request):
    logout(request)
    # messages.success(request,'ログアウトしました')
    return redirect('music_app:base')

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('user:user_login') #注意
        except ValidationError as e:
            regist_form.add_error('password',e)
    return render(request,'user/regist.html',context={
        'regist_form':regist_form,
    })

# def activate_user(request,token):
#     user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
#     return render(request,'user/activate_user.html')

@login_required
def user_edit(request):
    user_edit_form= forms.UserEditForm(request.POST or None, instance=request.user)
    if  user_edit_form.is_valid():
        # messages.success(request,'更新完了しました')
        user_edit_form.save()
    return render(request,'user/user_edit.html',context={
        'user_edit_form':user_edit_form,
    })

@login_required
def change_password(request):
    password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            # messages.success(request,'パスワード更新完了しました')
            update_session_auth_hash(request,request.user)
        except ValidationError as e:
            password_change_form.add_error('password',e)
    return render(request,'user/change_password.html',context={
        "password_change_form":password_change_form,
    })

            