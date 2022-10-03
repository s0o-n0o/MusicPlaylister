from django.urls import path
from . import views

app_name = 'music_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('create', views.create, name='create'),
    path('all_tracks', views.get_user_tracks, name='all_tracks'),
    path('playlist_track/<str:id>', views.get_playlist_tracks, name='playlist_tracks'),
]
