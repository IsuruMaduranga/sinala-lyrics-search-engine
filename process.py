import json,re
import mtranslate
import random
from time import sleep

def read_all_songs():
    with open('songs/songs.json','r') as f:
        all_songs = json.loads(f.read())
        return all_songs 

def process(songs):
    processed = []

    for song in songs:
        new = {}

        new["title_si"] = song["title_sinhala"].split(" - ")[0]
        new["title_en"] = song["title_english"].split(" - ")[0]

        new["artist_si"] = song["artist"]

        try:
            new["artist_en"] = song["title_english"].split(" - ")[1]
        except:
            new["artist_en"] = ""


        new["music_si"] = song["music"]

        new["melody_si"] = song["melody"]

        new["lyricist_si"] = song["lyrics_author"]

        new["lyrics"] = song["lyrics"].strip('\n')

        new["views"] = random.randint(100,10000)

        processed.append(new)

    return processed

if __name__ == "__main__":
    
    songs = read_all_songs()
    new_songs = process(songs)

    with open('songs/processed_songs.json', 'w') as t:
        t.write(json.dumps(new_songs))


