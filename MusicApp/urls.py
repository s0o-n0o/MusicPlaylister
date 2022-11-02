from django.urls import path
from . import views

app_name = 'music_app'

urlpatterns = [
    path('', views.base, name='base'),
    path('home', views.home, name='home'),
    path('create', views.create, name='create'),
    path('favorite_tracks', views.get_user_favorite_tracks, name='favorite_tracks'),
    path('playlist_track/<str:id>', views.get_playlist_tracks, name='playlist_tracks'),
    path('user_all_track/', views.user_alltracks, name='user_all_tracks'),
]
