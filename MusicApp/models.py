import email
from unittest.util import _MAX_LENGTH
from django.db import models
from user.models import Users
# Create your models here.

class SpotifyPlaylist(models.Model):
    user  = models.ForeignKey("user.Users", on_delete=models.CASCADE)
    playlist_id = models.CharField(max_length=255)
    playlist_name = models.CharField(max_length = 255)

    class Meta:
        db_table = 'spotify_playlist'
    
    def __str__(self) -> str:
        return self.playlist_name

class SpotifyArtist(models.Model):
    artist_id = models.CharField(max_length=255,primary_key=True)
    artist_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'spotify_artist'

    def __str__(self) -> str:
        return self.artist_name

class SpotifyTracks(models.Model):
    playlist =models.ManyToManyField(SpotifyPlaylist,related_name='spotifytracks',related_query_name='spotifytracks')
    track_id = models.CharField(max_length=255,primary_key=True)
    track_name = models.CharField(max_length=255)
    artist = models.ForeignKey("SpotifyArtist",on_delete=models.CASCADE)
    danceability=models.FloatField()
    energy=models.FloatField()
    valence=models.FloatField()
    acousticness=models.FloatField()
    loudness=models.FloatField()
    tempo=models.FloatField()

    class Meta:
        db_table = 'spotify_tracks'


    def __str__(self) -> str:
        return self.track_name