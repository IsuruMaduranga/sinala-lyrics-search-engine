from elasticsearch import Elasticsearch
import queries
import mtranslate
from strsimpy.levenshtein import Levenshtein

client = Elasticsearch(HOST="http://localhost",PORT=9200)
INDEX = 'songs'

def isSinhala(search_str):
    """
    Identifies a given string is Sinhala or English
    """

    try:
        search_str.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return True
    else:
        return False


def get_all_lists():
    """
    Get all the names of artists,musicians,melodists and lyricists from ElasticSearch instance
    """

    query = queries.all_lists()
    r = client.search(index=INDEX, body=query)["aggregations"]

    artist = []
    for b in r["Artist"]["buckets"]:
        artist.append(b["key"])

    music = []
    for b in r["Music"]["buckets"]:
        music.append(b["key"])

    lyricist = []
    for b in r["Lyricist"]["buckets"]:
        lyricist.append(b["key"])

    melody = []
    for b in r["Melody"]["buckets"]:
        melody.append(b["key"])

    return artist,music,lyricist,melody


def query_boosting(search_str):
    """
    Query boosting algorithm
    """

    #Initializing weights
    weights = {"title_si":0,"title_en":0,"artist_si":0,"artist_en":0,"music_si":0,"melody_si":0,"lyricist_si":0, "lyrics":0}

    sinhala = isSinhala(search_str)
    num_words = len(search_str.split(" "))

    ####### The algorithm ########
    if( not sinhala ):

        weights["artist_en"] = 1
        weights["title_en"] = 1

    elif( num_words < 3 ):

        weights["artist_si"] = 1

        comp_str = search_str
        
        artist,music,lyricist,melody = get_all_lists()

        lev = Levenshtein()
        
        for a in artist:
            dist = lev.distance(a, comp_str)
            if (dist <= 4):
                weights["artist_si"] = 5
                break
 
        for m in music:
            dist = lev.distance(m, comp_str)
            if (dist <= 4):
                if(weights["artist_si"] == 5):
                    weights["music_si"] = 0
                else:
                    weights["music_si"] = 5

                break

        for l in lyricist:
            dist = lev.distance(l, comp_str)
            if (dist <= 4):
                if(weights["artist_si"] == 5):
                    weights["lyricist_si"] = 0
                else:
                    weights["lyricist_si"] = 5

                break
        
        for m in melody:
            dist = lev.distance(m, comp_str)
            if (dist <= 4):
                if(weights["artist_si"] == 5):
                    weights["melody_si"] = 0
                else:
                    weights["melody_si"] = 5

                break

    elif (5 > num_words >= 3):

        weights["lyrics"] = 2
        weights["title_si"] = 5

    elif (num_words  >= 5 ):
        weights["lyrics"] = 3

    # Query attributes building based on weights of each field
    title_si ="title_si^{}".format(weights["title_si"])
    title_en ="title_en^{}".format(weights["title_en"])
    artist_si ="artist_si^{}".format(weights["artist_si"])
    artist_en ="artist_en^{}".format(weights["artist_en"])
    music_si ="music_si^{}".format(weights["music_si"])
    melody_si ="melody_si^{}".format(weights["melody_si"])
    lyricist_si ="lyricist_si^{}".format(weights["lyricist_si"])
    lyrics ="lyrics^{}".format(weights["lyrics"])

    return [title_si,title_en,artist_si,artist_en,music_si,melody_si,lyricist_si,lyrics]


def query(search_str,filters = None,req_filters=0):

    # Tokenizing
    words = search_str.split(" ")
    best_syn = ['හොඳම','ප්‍රසිද්ධම','හොදම','ජනප්‍රියම', 'best', 'top', 'popular']

    # Identifing range queries
    n = None
    new_search_str = ""
    for word in words:
        if word.isdigit():
            n = int(word)
        elif word in best_syn:
            pass
        else:
            new_search_str += word
            new_search_str += " "

    new_search_str = new_search_str.strip()

    # Running the query boosting algorithm
    opt = query_boosting(new_search_str)

    # Building the right query based on the attributes and boosted paramaters
    if( not n):
        if(filters):
            query = queries.multi_match_filtered(search_str, filters,fields=opt)
        elif(req_filters):
            query = queries.agg_multi_match(search_str,fields=opt)
        else:
            query = queries.multi_match(search_str, fields=opt)
    else:
        query = queries.multi_match_best(new_search_str,n)

    # Executing the query
    r = client.search(index=INDEX, body=query)

    return r