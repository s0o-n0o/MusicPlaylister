#spotipyapiでバウンディのアーティスト情報を取得

import spotipy
import spotipy.util as util

username = 'lcl'
scope = 'user-library-read'

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.search(q='artist:bauddy', type='artist')
    print(results)
else:
    print("Can't get token for", username)