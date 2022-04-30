
function createAllPlaylistSongs() {
    //create all the songs html
    let playlist = $("#playlist-container");

}

function createAllBrowseSongs() {
    let browse = $("#browseSongs");
    $.ajax({
        url: "getallsonginfo/" + id, //url = database
        type: "GET",
        success: function (data) {
            data.songs.forEach(function (song) {
                artists = song.artists.join(", ");
                browse.append(`
                <div class="row browsesong song" id=${song.id}>
                <div class="col-9">
                    <div class="songName">
                        ${song.name}
                    </div>
                    <div class="artists">
                        ${artists}
                    </div>
                </div>
                <div class="col-1" style="margin-right: 10px;">
                    <button class="btn bg-light bg-gradient  btn-sm"><i class="fa-solid fa-play" id="play-${song.id}"></i></button>
                </div>
                <div class="col-1">
                    <button class="btn bg-light bg-gradient  btn-sm"><i class="fa-solid fa-plus" id="add-${song.id}"></i></button>
                </div>
            </div>`);

                $("#play-" + song.id).click(function () {
                    playSong(song.id);
                });

                $("#add-" + song.id).click(function () {
                    addSong(song.id);
                });
            });
        }
    })


}

function playSong(id) {
    $.ajax({
        url: "songinfo/" + id, //url = database
        data: {
            'songId': id
        },
        type: "GET",
        success: function (data) {
            $("#audio")[0].attr("src", data.url)
            $(`#audio`)[0].load()
            $(`#audio`)[0].play()
        }
    })

}

function updatePlaylist() {
    $.ajax({
        url: "update/" + playlistid, //url = database
        data: {
            'songs': 1//songs stringified
        },
        type: "POST",
        success: function (data) {
            $("#audio")[0].attr("src", data.url)
            $(`#audio`)[0].load()
            $(`#audio`)[0].play()
        }
    })
}


function addSong(id) {
    updatePlaylist()

    // playlist was empyu, set the first song as the current song
    //if playlist had 1 song, set next song

    //otherwise just updated

}
function setCurrentSong() {
    //if playlist empty, return


    //delete top song, move everything up
    let songId = playlist[0];

    let audioLength = $("#playlist-audio1")[0].duration
    let currentTime = new Date().getTime();
    $.ajax({
        url: '/api/set_current_song',
        type: 'POST',
        data: {
            'songId': songId,
            'current_time': currentTime,
            'songTime': 0
        },
        dataType: 'json',
        success: function (data) {

        }
    });
    setTimeout(function () {
        setCurrentSong();
    }, audioLength);

    setNextSong()
}

function setNextSong() {
    //if theres a second song, set it as the next song
    $.ajax({
        url: '/api/set_current_song',
        type: 'POST',
        data: {
            'songId': songId,
        },
        dataType: 'json',
        success: function (data) {

        }
    });
}
