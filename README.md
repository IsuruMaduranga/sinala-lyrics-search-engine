# Sinhala lyrics Search Engine

This project contains the source code for REST API based implementation of sinhala lyrics search engine using elastic-search and python.

## Requirements

1. ElasticSearch
    * ElasticSearch installation guide on ubuntu 18.04 [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-18-04)
2. Python 3.5 or higher ( Anaconda or a virtual environment is preferred)

## Installation

1. Start an ElasticSearch Instance on the port 9200
2. Clone the repository
3. Install python dependencies using requirements.txt <br />
    * ``` pip3 install -r requirements.txt ``` 
3. Add your own songs to the songs directory as a list of JSON objects
4. Add songs to the ELasticSearch instance
    * ```python3 populate.py <name_of_songs_file.json> ```
4. Run app.py
    *  ```python3 app.py ```

## Querying the REST API
Send search queries using HTTP POST request to http://localhost:5000/ with JSON payload

```
        {
            "search": "ඔබට මා",
            "top" : "10"
            "req_filters":0,
            "filters":  {
                    "artist_si":"මාලනී බුලත්සිංහල"
                }
        } 
```

search - search string <br />
top - return top 10 (or given number) search results <br />
req_filters - ask search engine to suggest most suitable filters to the given search string <br />
filters - list of filters to filter out the search results <br />

* artist_si - filter by name of the artist
* music_si - filter by name of the musician
* melody_si - filter by name of the melodist
* lyricist_si - filter by name of the lyricist

## Directory Structure

Repo <br />
├── songs: Where song corpuses are stored as a list of JSON objects <br />
├── app.py : Flask REST API and starting point of the App <br />
├── es.py : Query processing, boosting and dealing with ElasticSearch <br />
├── queries.py :  Dynamci ElasticSeacrch query building functions <br />
├── webscrape.py :  Webscraper <br />
├── process.py : Pre-processing song corpus <br />
├── populate.py : Uploading songs to the ElasticSearch instance <br />
├── requirements.txt : Python dependencies <br />

## Features of the search engine

The major capabilites of the engine are listed below.

* Filtered searches – The search results can be filtered using four filters.
     * Name of the singer
     * Name of the melodist
     * Name of the musician
     * Name of the lyricist
* Range Queries – The top n number of search results can be obtained as follows
    1. By searching as follows <br />
    Ex: මාලනී බුලත්සිංහල හොඳම/ප්‍රසිද්ධම/හොදම/ජනප්‍රියම 10, මාලනී බුලත්සිංහල top/best 10
    2. Providing a JSON query parameter (top)
* Suppors both English and Singlish queries
    * Ex: නොමග නොයන් පුතේ විල්බට් ඇන්තනි, Nomaga noyan puthe obata ratak athe Wilbert Anthony
* Query boosting - Queries are boosted intelligently to increase the search accuracy

## Query boosting and optimization



![Query boosting and optimization](algo.png)
