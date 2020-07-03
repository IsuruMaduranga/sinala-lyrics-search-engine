from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json,re
client = Elasticsearch(HOST="http://localhost",PORT=9200)
INDEX = 'songs'


def createIndex():
    index = Index(INDEX,using=client)
    index.create()

def deleteIndex(index_name):
    es = Elasticsearch()
    es.indices.delete(index=index_name, ignore=[400, 404])

def read_all_songs():
    with open('songs/processed_songs.json','r') as f:
        all_songs = json.loads(f.read())
        return all_songs 


def genData(song_array):
    """
    Preprocessing data before uploading to the ElasticSearch Instance
    """

    for song in song_array:

        title_si = song.get("title_si",None)
        title_en = song.get("title_en",None)
        artist_si = song.get("artist_si",None)
        artist_en = song.get("artist_en",None)
        music_si = song.get("music_si",None)
        melody_si = song.get("melody_si",None)
        lyricist_si = song.get("lyricist_si",None)
        views = song.get("views",None)
        lyrics = song.get("lyrics",None)


        yield {
            "_index": "songs",
            "_source": {
                "title_si" : title_si,
                "title_en" : title_en,
                "artist_si" : artist_si,
                "artist_en" : artist_en,
                "music_si" : music_si,
                "melody_si" : melody_si,
                "lyricist_si" : lyricist_si,
                "views" : views,
                "lyrics" : lyrics
            },
        }

if __name__ == "__main__":

    #deleteIndex('songs')

    createIndex()
    all_songs = read_all_songs()
    helpers.bulk(client,genData(all_songs))
    