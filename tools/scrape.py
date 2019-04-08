#This script scrapes laulu.wiki site for songs
import requests
import traceback
import re

# specify the url
lauluwiki="https://laulu.wiki/api/v1/songs/{}/?format=json"


def as_song(song_id, name, s, tune = ""):
    if tune:
        tune = "\n\t\\tuneof{{{}}}".format(tune)

    return "wiki{} = {} = {{".format(song_id, name) + tune + s + "\n}\n\n"

def as_verse(s):
    return "\n\\verse{\n\t" + clean_breaks(s) + "\\\\\n}"

def clean_breaks(s):
    br = "\\\\\\\n\t"
    return re.sub("(\r)?\n", br, s)
    #return s.replace("\r\n", br).replace("\n", br)

def format_lyrics(verses):
    lyrics = ""
    for v in verses:
        if v and v.strip():
            lyrics += as_verse(v).replace("\n", "\n\t")
    return lyrics

def get_lauluwiki(song_id):
    url = lauluwiki.format(song_id)

    page_response = requests.get(url, timeout=10).json()
    name = page_response['name']
    raw_lyrics = page_response['lyrics']    
    melody = "" # page_response['melody']   
    #verses = raw_lyrics.split("\r\n\r\n")
    verses = re.compile("(\r)?\n(\r)?\n").split(raw_lyrics)

    lyrics = format_lyrics(verses)
    
    return as_song(song_id, name, lyrics, melody)


def run():
    data = ""

    for u in range(0, 510):
        try:
            print("\nscraping id  {}".format(u))
            song = get_lauluwiki(u)
            data += song
        except Exception as e: 
            traceback.print_exc()
            break
            #print(e)

    with open('lauluwiki.dat', 'w') as outfile:
        print("Writing to file")
        outfile.write(data)

    print("Done")

run()