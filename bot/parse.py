import re
from transliterate import translit

import scrapy
from scrapy.crawler import CrawlerProcess

from msgspec.json import encode, decode
from msgspec import Struct, field

# from scrapy.utils.project import get_project_settings

import transliterate

start_link = "https://genius.com/albums/Sagath/Its-all-magic"
BLOCKED_LINK = "https://genius.com/a/the-page-you-re-attempting-to-visit-is-not-available-in-your-region"
ALL_ARTISTS = 'https://genius.com/artists-index/' #! p/all


class albumData(scrapy.Spider):
   name = "album_data"
   allowed_domains = ["genius.com"]

   def parse(self, response):

      main_json = response.xpath('//meta[@itemprop="page_data"]/@content').get()

      # Получаем ID альбома, ссылку на обложку и название альбома
      class AlbumID(Struct):
         id: int

      class findID(Struct):
         name: str
         cover_art_url: str
         description_annotation: AlbumID

      class albumDict(Struct):
         album: findID

      album_id = decode(main_json, type=albumDict)

      # Получаем информацию об артистах на альбоме
      class primArtInfo(Struct):
         name: str
         url: str
         slug: str

      class pimArtPath(Struct):
         primary_artists: list[primArtInfo]
      
      class AlbumData(Struct):
         album: pimArtPath

      repo_data = decode(main_json, type=AlbumData)
      for artist in repo_data.album.primary_artists:

         yield {
            artist.name: artist.url,

            #TODO: нужно добавить проверку и очистку лишних символов -> получать имя артиста как на площадках
         }

      yield {
         'album_name': album_id.album.name,
         'cover_url': album_id.album.cover_art_url,
         'id': album_id.album.description_annotation.id

         #TODO: нужно добавить проверку и очистку лишних символов -> получать имя артиста как на площадках
      }


class SongDataSpider(albumData):
   name = "song_data"
   allowed_domains = ["genius.com"]

   def parse(self, response):
      songs_links = response.xpath('//a[contains(@class, "u-display_block")]/@href').getall()
      
      for link in songs_links:
         yield scrapy.Request(url=link, callback=self.parse_songs)

   # Получаем ID песни в JSON -> конвертируем в str и ищем другие данные
   def parse_songs(self, response):
      try:
         album_json = re.search(r'window\.__PRELOADED_STATE__ = JSON\.parse\(\'(.*)\'\)', response.text).group(1).replace("\\\\\\\"", '\'').replace("\\","")

      except TypeError:
         raise TypeError
      
      except AttributeError:
         pass

      # # # # # # 

      class songID(Struct):
         song: int

      class songData(Struct):
         songPage: songID

      try:
         song_id = decode(album_json, type=songData)
      except AttributeError:
         pass

      # # # # # # 
      class songs(Struct):
         songs: dict

      class songShortPath(Struct):
         entities: songs

      try:
         song_dict = decode(album_json, type=songShortPath)
      except AttributeError:
         pass

      class Test(Struct):
         title: str
         descriptionAnnotation: int

      zxczxc = decode(encode(song_dict.entities.songs[str(song_id.songPage.song)]), type=Test)

      #TODO: ^ изменить название переменной, + добавить сортировку Primary Artists и Featured Artisti
      #TODO: настроить добавление 'with' или feat. {artist} при указании треков

      yield {
         zxczxc.title: zxczxc.descriptionAnnotation,
         }
      


process = CrawlerProcess()
process.crawl(albumData, start_urls = [start_link])
process.crawl(SongDataSpider, start_urls = [start_link])
process.start()