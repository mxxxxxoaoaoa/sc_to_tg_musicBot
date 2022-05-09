import json
from urllib import parse
# from modules.db import BotDatabase
from aiogram.types.message import ParseMode
from modules.sc import Soundcloud
from modules.soundcloud_searcher import SoundcloudSearcher
from modules.utils import *
from mysql.connector import Error
import asyncio, json_config, logging, re, os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import filters
logging.basicConfig(level=logging.INFO)


config = json_config.connect('config/config.json')

with open('tgMusicBot-main\config\messages.json', 'r', encoding='utf-8') as f:
    mes = json.load(f)
    f.close()
sc = Soundcloud()
sc_searcher = SoundcloudSearcher()
utils = BotUtils()
# db = BotDatabase()

bot = Bot(config['bot_token'])
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# db.create_table()

# bot states
# ['decode_state', 'playlist_dl_state', 'playlist_state', 'search_state', 'track_dl_state', 'track_state']
# ['playlist_dl_state', 'playlist_state', 'search_state', 'sub_state', 'track_dl_state', 'track_state']
subS = 3
pDlS = 0
pS = 1
ss = 2
tDlS = 4
tS = 5


playlist_button = InlineKeyboardButton(mes['pBut'], callback_data="playlist_button")
track_button = InlineKeyboardButton(mes['tBut'], callback_data="track_button")
select_search = InlineKeyboardMarkup(row = 2).add(playlist_button, track_button)


# async def channelSub(message: types.Message):
#     user = int(message.from_user.id)
#     response = await bot.get_chat_member(chat_id = config['channel_id'], user_id = user )
#     return response['status']

# async def checkerSub(message: types.Message):
#     user = int(message.from_user.id)
#     state = dp.current_state()
#     getter = db.get(user)

#     if getter == 0:
#         db.set(user)

#     status = await channelSub(message)
#     print(f"{status} - статус id{user}")
#     if status == "member":
#         db.updateFlag(user)
#     if status == "left":
#         db.deleteFlag(user)

#     flag = db.getFlag(user)
#     print(f"{flag} - флаг id{user}")
#     if flag == 0:
#         print(f"id{user} Уставновлено состояние - не подписан.")
#         await state.set_state(BotStates.all()[subS])
#         return 0

#     if flag == 1:
#         print(f"id{user} Подписан на сообщество, обнуляю состояние")
#         await state.reset_state()
#         return 1

    

async def searching(message: types.Message):
    return await message.answer(mes['search_1'], reply_markup=select_search)


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), commands=['start'])
async def send_start(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    await message.answer(mes['start'], reply_markup=utils.start_keyboard())
    return await state.reset_state()
    


async def set_state_track_dl(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    await message.answer(mes['track_dl'])
    return await state.set_state(BotStates.all()[tDlS])


async def set_state_playlist_dl(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    await message.answer(mes['playlist_dl'])
    return await state.set_state(BotStates.all()[pDlS])


@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), lambda c: c.data == 'track_button')
async def track_searching(callback_query: types.CallbackQuery):
    from_user = callback_query['from']['id']
    chat_id = callback_query['message']['chat']['id']
    state = dp.current_state(user = from_user)
    # ch = await checkerSub(callback_query)
    # if ch == 1:
    await state.set_state(BotStates.all()[tS])
    await bot.send_message(chat_id, mes['search_track'])
    return await callback_query.answer()


@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), lambda c: c.data == 'playlist_button')
async def playlist_searching(callback_query: types.CallbackQuery):
    from_user = callback_query['from']['id']
    chat_id = callback_query['message']['chat']['id']
    state = dp.current_state(user = from_user)
    # ch = await checkerSub(callback_query)
    # if ch == 1:
    await bot.send_message(chat_id, mes['search_playlist'])
    await state.set_state(BotStates.all()[pS])
    return await callback_query.answer()

# @dp.message_handler(state = BotStates.SUB_STATE)
# async def subStateHandler(message: types.Message):
#     print("я в стейте")
#     ch = await checkerSub(message)
#     if ch == 1:
#         return await message.answer(mes['thx'])
#     if ch == 0:
#         return await message.answer(mes['subscribe_message'])
    

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), state=BotStates.TRACK_STATE)
async def track_search(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    req = message.text
    print(req)
    res = sc_searcher.request_tracks(req)
    json_res = json.loads(res)
    kb_creator = utils.track_create(json_res)
    await message.answer(kb_creator[0], reply_markup=kb_creator[1])
    return await state.reset_state()


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), state=BotStates.PLAYLIST_STATE)
async def playlist_search(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    req = message.text
    res = sc_searcher.request_playlists(req)
    json_res = json.loads(res)
    kb_creator = utils.playlist_create(json_res)
    await message.answer(kb_creator[0], reply_markup=kb_creator[1])
    return await state.reset_state()


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), state = BotStates.TRACK_DL_STATE)
async def track_dl(message: types.Message):
    state = dp.current_state()
    href = message.text
    link_template = "https://soundcloud.app.goo.gl/"
    if link_template in href:
        href = utils.url_decode(href)
    m = await message.answer(mes['request_message'])
    track = await sc.getTrack(href)
    if track != 0 and track != 1:
        with open(track, "rb") as f:
            await bot.send_document(message.chat.id, f)
            f.close()
        os.remove(track)
        await bot.delete_message(message.chat.id, m.message_id)
        return await state.reset_state()
    if track == 0:
        await message.answer(mes['error'])
        return await state.reset_state()
    if track == 1:
        await message.answer(mes['error_writing'])
        return await state.reset_state()
    

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), state = BotStates.PLAYLIST_DL_STATE)
async def playlist_dl(message: types.Message):
    state = dp.current_state()
    href = message.text
    link_template = "https://soundcloud.app.goo.gl/"
    if link_template in href:
        href = utils.url_decode(href)
    m = await message.answer(mes['request_message'])
    playlist = await sc.getPlaylist(href)
    if playlist != 0:
        for track in playlist:
            with open(track, "rb") as f:
                await bot.send_document(message.chat.id, f)
                f.close()
            os.remove(track)
        await bot.delete_message(message.chat.id, m.message_id)
        await message.answer(mes['playlist_end'])
        return await state.reset_state()
    if playlist == 0:
        await message.answer(mes['error'])
        return await state.reset_state()



@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE), lambda c: "/" in c.data)
async def search_handler(callback_query: types.CallbackQuery):
    raw_data = callback_query.data
    processed_data = raw_data.split("/")
    print(processed_data)
    href = "https://api.soundcloud.com"
    if processed_data[0] == "playlists":
        f = await sc.getPlaylist(f'{href}/playlists/{processed_data[1]}')
        if f != 0:
            await bot.send_message(callback_query.message.chat.id, mes['request_message'])
            for path in f:
                with open(path, "rb") as fp:
                    await bot.send_document(callback_query.message.chat.id, fp)
                    fp.close()
                    await asyncio.sleep(2)
                os.remove(path)
            await bot.send_message(callback_query.message.chat.id, mes['playlist_end'])
        if f == 0:
            await bot.send_message(callback_query.message.chat.id, mes['error'])    
        return await callback_query.answer()
    if processed_data[0] == "tracks":
        f = await sc.getTrack(f'{href}/tracks/{processed_data[1]}')
        m = await bot.send_message(callback_query.message.chat.id, mes['request_message'])
        if f != 0:
            with open(f, "rb") as fp:
                await bot.send_document(callback_query.message.chat.id, fp)
                fp.close()
            os.remove(f)
        await bot.edit_message_text(mes['request_end'], m.chat.id, m.message_id)
        if f == 0:
            await bot.send_message(callback_query.message.chat.id, mes['error'])    
        return await callback_query.answer(text="")


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP) | filters.ChatTypeFilter(types.ChatType.PRIVATE))
async def button_handler(message: types.Message):
    if message.text == mes["a_button"]:
        await bot.delete_message(message.chat.id, message.message_id)
        # ch = await checkerSub(message)
        # if ch == 1:
        return await searching(message)
    if message.text == mes["b_button"]:
        await bot.delete_message(message.chat.id, message.message_id)
        # ch = await checkerSub(message)
        # if ch == 1:
        return await set_state_track_dl(message)
    if message.text == mes["c_button"]:
        await bot.delete_message(message.chat.id, message.message_id)
        # ch = await checkerSub(message)
        # if ch == 1:
        return await set_state_playlist_dl(message)



async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)