import email
from django.db import models

# Create your models here.
class User(models.Model):
    user_id  = models.ForeignKey()
    user_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.user_name

    class Meta:
        db_table = "user"

class Spotify_playlist(models.Model):
    playlist_id = models.ForeignKey()
    playlist_name = models.CharField()

class Sptoify_tracks(models.Model):
    playlist_id = models.CharField()
    track_id = models.CharField()
    track_name = models.CharField()
    artist_id = models.ForeignKey()

class Spotify_artist(models.Model):
    artist_id = models.CharField()
    artist_name = models.CharField()