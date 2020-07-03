# Scraper Script for scrape Sinhala Lyrics from https://geepadura.blogspot.com/
# Scraped Song lyrics will be saved as a csv file

# Required imports
from bs4 import BeautifulSoup
import requests
import unicodecsv as csv

#This is the base URL for Sihala Lyrics blog
URL='https://geepadura.blogspot.com/'

DataArray = []


#Define the getSongData Method to scrape and save data to CSV
def getSongData(output_file_name,start_year,end_year):
    trackId =0  # Track ID - auto increment integer
    with open(output_file_name, mode='wb') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write the header column name to the CSV file
        csv_writer.writerow(["lyric_id","title","title_sinhala","title_english","artist","music","melody","lyrics_author","lyrics",'upload_year','upload_month'])

        step = int((end_year-start_year)/abs(end_year-start_year))
        sm = 1 if step == 1 else 12
        em = 13 if step == 1 else 0
        
        for year in range(start_year,end_year,step):
            for month in range(sm,em,step):
                print (str(year)+"/"+str(month))                                                      ## Get the month and year for generate blogger archive link 

                target = URL+str(year)+"/"+str(month)                                               ## Build the page link using blogger archive links 
                if(month<10):
                    target = URL+str(year)+"/0"+str(month)                                          ## Add 0 to single digit months to make it 2 digits
            
                response = requests.get(target)                                                     ## Send the GET request to page and receive content

                soup = BeautifulSoup(response.text,'html.parser')                                   ## Input to Scaper

                songList = soup.findAll(class_="post-outer-container")                              ## Get the song list in the page for given month 

                for song in songList:
                    
                    if (song.find(class_="post-title entry-title")!=None):                          ## Title tag is available
                        title=""
                        title =  song.find(class_="post-title entry-title").get_text().strip()      ## Scrape song Titles
                        titleSn =title
                        titleEn = title
                        if(title.find("|")!=-1):
                            titleSn = title.split("|")[0].strip()
                            titleEn = title.split("|")[1].strip()
                        songLink = song.find(class_="post-title entry-title").find('a')['href']     ## Scrape individual song lyric page link

                        songPageResponse = requests.get(songLink)                                   ## Get the song lyric page using GET request

                        songSoup = BeautifulSoup(songPageResponse.text,'html.parser')               ## Scaping the lyrics page


                        imageDiv = songSoup.find(class_="separator")            

                        songContentDiv = songSoup.find(class_="post-body entry-content float-container")

                        songVideoIframe=None    ## Prevent keeping in meomry throgh loops
                        if(songContentDiv.iframe!=None):
                            songVideoIframe = songContentDiv.iframe.extract()
                        ## SongContentDiv is the blog content which include the lyrics and few other metadata                            
                        ## String search for metadata
                        artsitId = str(songContentDiv).rfind("ගායනය")
                        musicId = str(songContentDiv).rfind("සංගීතය")
                        melodyId = str(songContentDiv).rfind("තනුව")
                        lyricsAuthorId = str(songContentDiv).rfind("ගී පද")
                        if(lyricsAuthorId==-1):
                            lyricsAuthorId =str(songContentDiv).rfind("පද රචනය")

                        artist = ""
                        music = ""
                        melody = ""
                        lyricsAuthor = ""

                        upload_date = str(target)
                        upload_year = upload_date.split('/')[-2]
                        upload_month = upload_date.split('/')[-1] 
                       
                        ## String cleaning for available metadata
                        if(artsitId!=-1):
                            artist = str(songContentDiv)[artsitId:artsitId + str(songContentDiv)[artsitId:].index("<")].replace("ගායනය","").replace(":","").replace("-","").strip()

                        if(musicId!=-1):
                            music = str(songContentDiv)[musicId:musicId + str(songContentDiv)[musicId:].index("<")].replace("සංගීතය","").replace(":","").replace("-","").strip()

                        if(melodyId!=-1):
                            melody = str(songContentDiv)[melodyId:melodyId + str(songContentDiv)[melodyId:].index("<")].replace("තනුව","").replace(":","").replace("-","").strip()

                        if(lyricsAuthorId!=-1):
                            lyricsAuthor = str(songContentDiv)[lyricsAuthorId:lyricsAuthorId + str(songContentDiv)[lyricsAuthorId:].index("<")].replace("ගී පද","").replace("පද රචනය","").replace(":","").replace("-","").strip()
                            
                        ## Lyrics string extracting and cleaning 
                        lyrics =  str(songContentDiv).replace(str(imageDiv),"").replace(str(songVideoIframe),"").replace("<br/>","\\n").replace("<div>","").replace("</div>","")
                        if(lyrics.find("\\n")!=-1 and lyrics.find("\\n")!=lyrics.rfind("<iframe")):
                            lyrics = lyrics[lyrics.index("\\n"):lyrics.rfind("<iframe")].strip()
                        if(artsitId!=-1):
                            if(lyrics.rfind("ගායනය")!=-1):
                                lyrics = lyrics[0:lyrics.rfind("ගායනය")]

                                
                        if(title!=""):          ## If title is empty no use 
                            csv_writer.writerow([trackId,title,titleSn,titleEn,artist,music,melody,lyricsAuthor,lyrics,upload_year,upload_month])
                            trackId+=1          ## Write to the CSV row and increase trackId
                            print (trackId)
                    else:
                        print ("no songs")

            
                
    print ("Lyrics Scraping is Completed !")
    print ("Number of lyrics retrieved : " + str(trackId))



##Using the scaping function 

getSongData('Sinhala_Unicode_Song_Lyrics_Corpus.csv',2020,2009)                
                
          
                    



     
    



