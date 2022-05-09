from .sc import Soundcloud
import json, json_config, requests
from urllib.parse import quote

sc = Soundcloud()
with open('tgMusicBot-main\config\config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    f.close()
# config = json_config.connect('./config/config.json')


class SoundcloudSearcher:
    def __init__(self) -> None:
        pass

    def request_tracks(self, track_name: str, offset: int = 0):
        limit = 20
        track_name_quotes = quote(track_name)
        href_track = f'https://api-v2.soundcloud.com/search?q={track_name_quotes}&facet=model&client_id={config["sc_client_id"]}&limit={limit}&offset={offset}&linked_partitioning=1&app_version=1633082668&app_locale=en'
        try:
            r = requests.get(href_track)
            responses = json.loads(r.text)
            info = []
            for response in responses['collection']:
                if response['kind'] == 'track':
                    uri = response['uri']
                    title = response['title']
                    username = response['user']['username']
                    info.append(
                        {
                            "username": username,
                            "title": title, 
                            "uri": uri
                        }
                    )
            info_json = json.dumps(info, indent=4, ensure_ascii=False)
            return info_json
        except:
            print('error')
            return 0
    
    def request_playlists(self, playlist_name: str, offset: int = 0):
        limit = 20
        playlist_name_quotes = quote(playlist_name)
        href_playlist = f'https://api-v2.soundcloud.com/search/playlists_without_albums?q={playlist_name_quotes}&client_id={config["sc_client_id"]}&limit={limit}&offset={offset}app_version=1633082668&app_locale=en'
        try:
            r = requests.get(href_playlist)
            responses = json.loads(r.text)
            info = []
            for response in responses['collection']:
                uri = response['uri']
                title = response['title']
                username = response['user']['username']
                track_count = response['track_count']
                link = response['permalink_url']
                info.append(
                    {
                        "username": username,
                        "title": title,
                        "track_count": track_count,
                        "link": link,
                        "uri": uri
                    }
                )
            info_json = json.dumps(info, indent=4, ensure_ascii=False)
            return info_json
        except: 
            print('error')
            return 0