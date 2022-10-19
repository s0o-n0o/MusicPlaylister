import spotipy
import spotipy.util as util
import info
scope=("user-read-private user-read-email")

token= util.prompt_for_user_token(username="lcl", scope=scope, client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)
sp = spotipy.Spotify(auth=token)
id = sp.me()["id"]
user_info= sp.user(id)
print(user_info)