from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'music_app'

urlpatterns = [
    path('', views.base, name='base'),
    path('home', views.home, name='home'),
    path('create', views.create, name='create'),
    path('favorite_tracks', cache_page(60*5)(views.get_user_favorite_tracks), name='favorite_tracks'),
    path('playlist_track/<str:id>', cache_page(60*15)(views.get_playlist_tracks), name='playlist_tracks'),
    path('user_all_track/', cache_page(60*5)(views.user_alltracks), name='user_all_tracks'),
    path('play_track/<str:track_id>', views.play_track,name="play_track")
]
