import sys
import spotipy
import spotipy.util as util
import info
scope = 'user-library-read'

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()
# cledential = spotipy.SpotifyClientCredentials(client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET)

token = util.prompt_for_user_token(username="lcl", scope= scope,client_id=info.SPOTIPY_CLIENTID,client_secret=info.SPOTIPY_SECRET,redirect_uri=info.SPOTIPY_REDIRECTURI)

if token:
    sp = spotipy.Spotify(auth=token)
    print(sp.me())
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
# else:
#     print("Can't get token for", username)