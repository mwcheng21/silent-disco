from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import os
import psycopg2


app = Flask(__name__)

def exec_statement(statement, mode="NONE"):
    conn = psycopg2.connect("postgresql://mwcheng:lMBa1RwkVbbuYlVq3ABi-w@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Drustic-fish-1550")
    with conn.cursor() as cur:
        cur.execute(statement)
        if (mode == "FETCHONE"):
            row = cur.fetchone()
            conn.commit()
            conn.close()
            return row
        elif (mode == "FETCHALL"):
            rows = cur.fetchall()
            conn.commit()
            conn.close()
            return rows
        conn.commit()
        conn.close()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    playlist = exec_statement("SELECT playlist FROM playlistIds WHERE playlistid=" + id + ";", "FETCHONE")[0]
    return render_template("edit.html", id=id, playlist=playlist.split(","))

@app.route('/stream/<id>', methods=['GET'])
def stream(id):
    return render_template("stream.html", id=id)


# API routes
def convertToJson(sqlReturn):
    return {"id": sqlReturn[1],
                    "TrackName": sqlReturn[2],
                    "Artists": sqlReturn[3],
                    "CoverArt": sqlReturn[4],
                    "Location": sqlReturn[5]}

@app.route('/songinfo/<id>', methods=['GET'])
def getSongInfo(id):
#     /get songinfo
    songinfo = exec_statement("SELECT * FROM song WHERE tid='" + id + "';", "FETCHONE")
    if songinfo:
        return jsonify(convertToJson(songinfo))

@app.route('/playlist/<id>', methods=['GET', "POST"])
def playlist(id):
    playlist = exec_statement("SELECT * FROM playlistIds WHERE playlistid=" + id + ";", "FETCHONE")
    if playlist == None:
        insert = '''INSERT INTO playlistIds (playlistId, playlist) VALUES ('%s', '%s');''' % (id, request.form['tid'])
        exec_statement(insert)
        return jsonify({"playlist": [request.form['tid']]})
    playlist = playlist[2].split(",")
    if ('' in playlist):
        playlist.remove('')
    if request.method == 'POST':
        # update playlist
        playlist.append(request.form['tid'])
        newplaylist = ",".join(playlist)
        exec_statement("UPDATE playlistIds SET playlist='" + newplaylist + "' WHERE playlistid='" + id + "';")
    return jsonify({"playlist": playlist})
    
@app.route('/current/<id>', methods=['GET', "POST"])
def current(id):
    if request.method == 'POST':
        exec_statement("UPDATE currentSongs SET tid='" + request.form['tid'] + "', SongCurrentTime='" + request.form['currentTime'] + "', MasterTime='" + request.form['masterTime'] + "' WHERE playlistId=" + id + ";")
        return jsonify("success")
    else:
        info = exec_statement("SELECT * FROM currentSongs WHERE playlistId=" + id + ";", "FETCHONE")
        return jsonify({"tid": info[2], "currentTime": info[3], "masterTime": info[4]})


@app.route('/getall', methods=['GET'])
def getAll():
    songs = exec_statement("SELECT * FROM song LIMIT 10;", "FETCHALL")
    return jsonify({"songs": [convertToJson(song) for song in songs]})





if __name__ == "__main__" :
    app.run(debug = True)

