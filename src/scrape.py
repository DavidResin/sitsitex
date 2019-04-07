#This script scrapes laulu.wiki site for songs
import requests
import traceback

# specify the url
lauluwiki="https://laulu.wiki/api/v1/songs/{}/?format=json"


def as_song(name, s, tune = ""):
    if tune:
        tune = "\n\t\\tuneof{{{}}}".format(tune)

    return "{} = {} = {{".format(name.replace(" ", "").lower(), name) + tune + s + "\n}\n\n"

def as_verse(s):
    return "\n\\verse{\n\t" + s.replace("\r\n", "\\\\\n\t") + "\n}"

def format_lyrics(verses):
    lyrics = ""
    for v in verses:
        if v.strip():
            lyrics += as_verse(v).replace("\n", "\n\t")
    return lyrics

def get_lauluwiki(song_id):
    url = lauluwiki.format(song_id)

    page_response = requests.get(url, timeout=10).json()
    name = page_response['name']
    raw_lyrics = page_response['lyrics']    
    melody = "" # page_response['melody']
    verses = raw_lyrics.split("\r\n\r\n")

    lyrics = format_lyrics(verses)
    
    return as_song(name, lyrics, melody)


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