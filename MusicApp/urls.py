from django.urls import path
from . import views

app_name = 'music_app'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('create', views.create, name='create'),
    path('all_tracks', views.get_user_tracks, name='all_tracks'),
    path('playlist_track/<str:id>', views.get_playlist_tracks, name='playlist_tracks'),
]
