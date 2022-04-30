
function createAllPlaylistSongs() {
    //create all the songs html
    let playlist = $("#playlist-container");

}                   
function createAllBrowseSongs() {
    let browse = $("#browseSongs");
    $.ajax({
        url: "/getall" , //url = database
        type: "GET",
        success: function (data) {
            data.songs.forEach(function (song) {
                artists = song.Artists//.join(", ");
                browse.append(`
                <div class="row browsesong song" id=${song.id}>
                <div class="col-9">
                    <div class="songName">
                        ${song.TrackName}
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
function createPlaylist(){
    $("#playlistSongs").html('')

    playlist.forEach(function (song) {
        $.ajax({
            url: "/songinfo/" + song,
            type: "GET",
            success: function (data) {
                $("#playlistSongs").append(`<div class="row playlistsong song" data-bs-toggle="tooltip" data-bs-placement="top"
                title="This song is playing">
                <div class="col-10">
                    <div class="songName">
                        ${data.TrackName}
                    </div>
                    <div class="artists">
                        ${data.Artists}
                    </div>
                </div>
                <div class="col-1">
                    <button class="btn bg-danger bg-gradient btn-sm"><i class="fa-solid fa-trash"></i></button>
                </div>
            </div>`)
            }
        })

    })
}
function playSong(id) {
    $.ajax({
        url: "/songinfo/" + id, //url = database
        type: "GET",
        success: function (data) {
            $("#audio")[0].src = data.Location
            $(`#audio`)[0].load()
            $(`#audio`)[0].play()
        }
    })

}

function addSong(id) {
    playlist.push(id)
    if (playlist.length == 0) {
        $("#playlistAudio")[0].play()
        syncToOthers()
    }
    $.ajax({
        url: "/playlist/" + channel, //url = database
        data: {
            'tid': id//songs stringified
        },
        type: "POST",
        success: function (data) {
            createPlaylist()
        }
    })
}
var currentTid = ""
function syncToOthers(){
    
    $.ajax({
        url: "/current/" + channel, //url = database
        data: {
            'currentTime': $("#playlistAudio")[0].currentTime,
            'masterTime': new Date().getTime(),
            'tid': currentTid
        },
        type: "POST",
        success: function (data) {
            console.log(data)
        }
    })
}

setInterval(function(){
    syncToOthers()
}, 10000)
$("#playlistAudio")[0].volume = 0
$("#playlistAudio")[0].onended = function(){
    //play next
    playlist.pop(0)
    currentTid = playlist[0]
    $.ajax({
        url: "/songinfo/" + playlist[0],
        type: "GET",
        success: function (data) {
            $("#playlistAudio")[0].src = data.Location;
            $("#playlistAudio")[0].load()
            $("#playlistAudio")[0].play()
        }
    })
    createPlaylist()
    
}

$.ajax({
    url: "/songinfo/" + playlist[0],
    type: "GET",
    success: function (data) {
        $("#playlistAudio")[0].src = data.Location;
        $("#playlistAudio")[0].load()
        $("#playlistAudio")[0].play()
    }
})
currentTid = playlist[0]
createAllBrowseSongs()
createPlaylist()
