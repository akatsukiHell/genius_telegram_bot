import requests
from bs4 import BeautifulSoup
import re

import msgspec
from msgspec.json import decode, encode
from msgspec import Struct
import datetime

import orjson

start = datetime.datetime.now()



# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#     "Accept": "application/json"
# }

genius_link = "https://genius.com/albums/Og-buda/Miss-you-but-working"
req = requests.get(genius_link).text
soup = BeautifulSoup(req, 'lxml')


songs_in_album_link = [links['href'] for links in soup.find_all('a', {'class':'u-display_block'})]

for links in songs_in_album_link:

   songs_request = requests.get(f'{links}').text

   try:
      data = re.search(
                  r'window\.__PRELOADED_STATE__ = JSON\.parse\(\'(.*)\'\)', songs_request
            ).group(1).replace("\\\\\\\"", '\'').replace("\\","")
   except AttributeError:
        pass

   class songID(Struct):
         song: int

   class songData(Struct):
         songPage: songID

   # class 

# class Albums(Struct):
#       albums: list

   repo_data = decode(data, type=songData)
#    convert = msgspec.to_builtins(repo_data)
   print(repo_data.songPage.song)

   # print(orjson.dumps(repo_data))



# asjdkasd = {}

# print(repo_data)
# current_song_id = str(get_js['songPage']['song'])
# song_shortcut = get_js['entities']['songs'][current_song_id]['descriptionAnnotation']

# print(song_shortcut)

finish = datetime.datetime.now()

excecution_time = finish - start

print(f"Код выполнялся {excecution_time}")

# print(data)





# # # # # # # # # # 


#! need update, artist:his link

# replace('\u200b', '')

# for artist in primary_artist:
#    if '&' in artist or ',' in artist:
#       primary_artist = [j for i in artist.split(', ') for j in i.split(' & ')]

# try:
#    english_prim_trans = re.search(r'\((.+?)\)', artist)[1]
#    if artist[0] == translit(english_prim_trans[0], 'ru'):
#          index = primary_artist.index(artist)
#          primary_artist[index]  = re.sub(r"[\(\[].*?[\)\]]", "", artist).strip()
# except TypeError:
#    pass


# for album in album_name:
#    try:
#       english_alb_trans = re.search(r'\((.+?)\)', album)[1]
#       if album[0] == translit(english_alb_trans[0], 'ru'):
#          index = album_name.index(album)
#          album_name[index]  = re.sub(r"[\(\[].*?[\)\]]", "", album).strip()
#    except TypeError:
#       pass
   
# ! Need to delete (*this text*) after get RU song name
#! fix & and feat.