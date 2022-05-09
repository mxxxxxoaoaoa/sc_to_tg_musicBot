from aiogram.utils.helper import Helper, HelperMode, ListItem
from future.utils import listitems
import requests, json, json_config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


# mes = json_config.connect('./config/messages.json')
with open('tgMusicBot-main\config\messages.json', 'r', encoding='utf-8') as f:
    mes = json.load(f)
    f.close()



class BotStates(Helper):
    mode = HelperMode.snake_case

    SEARCH_STATE = ListItem()
    TRACK_STATE = ListItem()
    PLAYLIST_STATE = ListItem()
    TRACK_DL_STATE = ListItem()
    PLAYLIST_DL_STATE = ListItem()
    SUB_STATE = ListItem()
    
print(BotStates.all())
# ['playlist_dl_state', 'playlist_state', 'search_state', 'sub_state', 'track_dl_state', 'track_state']

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    }

class BotUtils():
    def __init__(self) -> None:
        pass

    def url_decode(self, href: str):
        try:
            r = requests.get(href, headers = headers)
            raw_url = r.url
            link_to_track = raw_url.split("?")[0]
            return link_to_track
        except: 
            return 0

    def track_create(self, json_array: list):
        k = 1
        keyboard = InlineKeyboardMarkup(row_width=5)
        text = ""
        for item in json_array:
            username = item['username']
            title = item['title']
            uri = item['uri']
            text += f"{k}. {username} - {title}\n"
            splitted_uri = uri.split("https://api.soundcloud.com/")
            but = InlineKeyboardButton(k, callback_data = splitted_uri[1])
            keyboard.insert(but)
            k += 1
        return text, keyboard


    def playlist_create(self, json_array: list):
        k = 1
        text = ""
        keyboard = InlineKeyboardMarkup(row_width=5)
        for item in json_array:
            username = item['username']
            title = item['title']
            uri = item['uri']
            track_count = item['track_count']
            link = item['link']
            text += f"{k}. {username} - {title}.    Количество треков: {track_count}\n📍 {link}\n"
            splitted_uri = uri.split("https://api.soundcloud.com/")
            but = InlineKeyboardButton(k, callback_data = splitted_uri[1])
            keyboard.insert(but)
            k += 1
        return text, keyboard


    def start_keyboard(self):
        a = KeyboardButton(mes['a_button'])
        b = KeyboardButton(mes['b_button'])
        c = KeyboardButton(mes['c_button'])
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5).add(a, b, c)
        return kb