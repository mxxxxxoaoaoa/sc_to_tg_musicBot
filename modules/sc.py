import json_config, os
from sclib.asyncio import SoundcloudAPI, Track, Playlist

config = json_config.connect('./config/config.json')

class Soundcloud: 
    def __init__(self):
        self.api = SoundcloudAPI(config['sc_client_id'])


    async def getTrack(self, t_link: str):
        try:
            print(f'_. downloading track starting now.')
            track = await self.api.resolve(t_link)
            assert type(track) is Track
            filename = f'{track.artist} - {track.title}.mp3'
            filename = self.validName(filename=filename)
            print(f'-. {filename} downloaded! saving to file.')
            try:
                with open(filename, "wb+") as fp:
                    await track.write_mp3_to(fp)
                return filename
            except:
                print("error writing")
                os.remove(filename)
                return 1
        except:
            print('error')
            return 0

    async def getPlaylist(self, p_link: str):
        try:
            print(f'-. downloading playlist starting now.')
            playlist = await self.api.resolve(p_link)
            filenames = []
            assert type(playlist) is Playlist
            for track in playlist.tracks:
                filename = f'{track.artist} - {track.title}.mp3'    
                filename = self.validName(filename=filename)
                filenames.append(filename)
                print(f'_. {filename} downloaded! saving to file.')
                try:
                    with open(filename, "wb+") as fp:
                        await track.write_mp3_to(fp)
                except: 
                    print("error on writing")
                    del filenames[-1]
            return filenames
        except: 
            print('error')
            return 0  


    def validName(self, filename):
        bad_symbols = [
            "/",
            ":",
            "*",
            "?",
            '"',
            "<",
            ">",
            "|",
            "+",
            "!"
        ]
        fn = list(filename) 
        for sym in fn:
            if sym in bad_symbols:
                i = fn.index(sym)
                fn[i] = ""
        filename = ''.join(fn)
        return filename
          