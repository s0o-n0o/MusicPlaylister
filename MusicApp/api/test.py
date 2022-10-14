#spotipyapiでバウンディのアーティスト情報を取得
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import info
username = 'lcl'

scope = 'user-library-read'
client_id = info.SPOTIPY_CLIENTID
client_secret = info.SPOTIPY_SECRET
redirect_uri =info.SPOTIPY_REDIRECTURI

auth_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret )
sp = spotipy.Spotify(auth_manager=auth_manager)
results = sp.search(q='vaundy', type='artist')
print(results)  
