import requests
from bs4 import BeautifulSoup
import os
import psycopg2


def exec_statement(conn, stmt):
    # try:
    with conn.cursor() as cur:
        cur.execute(stmt)
        # row = cur.fetchone()
        conn.commit()
        # if row: print(row[0])
    # except psycopg2.ProgrammingError:
    #     return


def main():

    # Connect to CockroachDB
    connection = psycopg2.connect("postgresql://mwcheng:lMBa1RwkVbbuYlVq3ABi-w@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Drustic-fish-1550")
    # connection = psycopg2.connect(os.environ['DATABASE_URL'])

    statements = [
        
        "CREATE TABLE IF NOT EXISTS song (id SERIAL PRIMARY KEY, tid VARCHAR(255), TrackName VARCHAR(255), Artists VARCHAR(255), CoverArt VARCHAR(255), Location VARCHAR(255))",
        "CREATE TABLE IF NOT EXISTS currentSongs (id SERIAL PRIMARY KEY, playlistId INT, tid VARCHAR(255), SongCurrentTime VARCHAR(255), MasterTime VARCHAR(255))",
        "CREATE TABLE IF NOT EXISTS nextSongs (id SERIAL PRIMARY KEY, playlistId INT, tid VARCHAR(255))",
        "CREATE TABLE IF NOT EXISTS playlistIds (id SERIAL PRIMARY KEY, playlistId INT, playlist VARCHAR(65535))",
            ]

    for statement in statements:
        exec_statement(connection, statement)

# main()
URL = "https://ncs.io/music?page="
songsAdded = set()
connection = psycopg2.connect("postgresql://mwcheng:lMBa1RwkVbbuYlVq3ABi-w@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Drustic-fish-1550")

for i in range(1, 56):
    page = requests.get(URL + str(i))

    soup = BeautifulSoup(page.content, "html.parser")
    songs = soup.find_all("a", class_="player-play")
    for song in songs:
        tid = song['data-tid'].replace("'", "")
        mp3 = song['data-url'].replace("'", "")
        coverArt = song['data-cover'].replace("'", "")
        artists = song['data-artist'].split("</a>")
        artists = [artist[artist.find(">")+1:].replace("'", "") for artist in artists][:-1]
        trackName = song['data-track'].replace("'", "")
        if tid not in songsAdded:
            insert = '''INSERT INTO song (tid, TrackName, Location, CoverArt, Artists) VALUES ('%s', '%s', '%s', '%s', '%s');''' % (tid, trackName, mp3, coverArt, artists)
            exec_statement(connection, insert)
            # print(insert)
        
        songsAdded.add(tid)
connection.close()
