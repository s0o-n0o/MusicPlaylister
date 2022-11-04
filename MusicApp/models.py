import email
from unittest.util import _MAX_LENGTH
from django.db import models
from user.models import Users
# Create your models here.

class SpotifyPlaylist(models.Model):
    user  = models.ForeignKey("user.Users", on_delete=models.CASCADE)
    playlist_id = models.CharField(max_length=255,primarykey=True)
    playlist_name = models.CharField(max_length = 255)

    class Meta:
        db_table = 'spotify_playlist'

class SpotifyArtist(models.Model):
    artist_id = models.CharField(max_length=255,unique=True)
    artist_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'spotify_artist'

class SpotifyTracks(models.Model):
    playlist_id = models.ForeignKey('SpotifyPlaylist',on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255,unique=True)
    track_name = models.CharField(max_length=255)
    artist_id = models.ForeignKey("SpotifyArtist",on_delete=models.CASCADE)
    danceability=models.IntegerField()
    energy=models.IntegerField()
    valence=models.IntegerField()
    acousticness=models.IntegerField()
    loudness=models.IntegerField()
    tempo=models.IntegerField()

    class Meta:
        db_table = 'spotify_tracks'