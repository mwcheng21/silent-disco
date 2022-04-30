import requests
from bs4 import BeautifulSoup

URL = "https://ncs.io/music?page="
songsAdded = set()

for i in range(1, 2):
    page = requests.get(URL + str(i))

    soup = BeautifulSoup(page.content, "html.parser")
    songs = soup.find_all("a", class_="player-play")
    for song in songs:
        tid = song['data-tid']
        mp3 = song['data-url']
        coverArt = song['data-cover']
        artists = song['data-artist'].split("</a>")
        artists = [artist[artist.find(">")+1:] for artist in artists][:-1]
        trackName = song['data-track']
        if tid not in songsAdded:
            print("INSERT INTO songs (tid, trackName, mp3, coverArt, artists) VALUES ('" + tid + "', '" + trackName + "', '" + mp3 + "', '" + coverArt + "', '" + str(artists) + "');")

        songsAdded.add(tid)