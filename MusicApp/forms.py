from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password

class CreatePlaylistArtistNameForm(forms.Form):
    artistname = forms.CharField(label="artistname" ,max_length=255,null=True)

