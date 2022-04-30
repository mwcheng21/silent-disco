var currentId = 1

function createWave(id) {
    let audioElement = document.querySelector(`#audio${id}`);
    let canvasElement = document.querySelector(`#wave${id}`);

    let wave = new Wave(audioElement, canvasElement);

    if (channel == 1) {
        wave.addAnimation(new wave.animations.Glob({
            fillColor: { gradient: ["red", "blue", "green"], rotate: 45 },
            lineWidth: 10,
            lineColor: "#fff"
        }));
    }
    else if (channel == 2) {
        wave.addAnimation(new wave.animations.Wave({
            lineWidth: 10,
            lineColor: "red",
            count: 20
        }));
    } else if (channel == 3) {
        wave.addAnimation(new wave.animations.Cubes({
            bottom: !0,
            count: 60,
            cubeHeight: 5,
            fillColor: {
                gradient: ["#FAD961", "#F76B1C"]
            },
            lineColor: "rgba(0,0,0,0)",
            radius: 10
        })),
            wave.addAnimation(new wave.animations.Cubes({
                top: !0,
                count: 60,
                cubeHeight: 5,
                fillColor: {
                    gradient: ["#FAD961", "#F76B1C"]
                },
                lineColor: "rgba(0,0,0,0)",
                radius: 10
            })),
            wave.addAnimation(new wave.animations.Circles({
                lineColor: {
                    gradient: ["#FAD961", "#FAD961", "#F76B1C"],
                    rotate: 90
                },
                lineWidth: 4,
                diameter: 20,
                count: 10,
                frequencyBand: "base"
            }))
    } else {
        wave.addAnimation(new wave.animations.Square({
            lineColor: {
                gradient: ["#21D4FD", "#B721FF"]
            }
        })),
            wave.addAnimation(new wave.animations.Arcs({
                lineWidth: 4,
                lineColor: {
                    gradient: ["#21D4FD", "#B721FF"]
                },
                diameter: 500,
                fillColor: {
                    gradient: ["#21D4FD", "#21D4FD", "#B721FF"],
                    rotate: 45
                }
            }))
    }
}


function sync() {
    // $.ajax({
    //     url: "/current/" + channel, //url = database
    //     type: "GET",
    //     success: function (data) {
    //         //get the current song
    //         $.ajax({
    //             url: "/songinfo/" + data.tid, //url = database
    //             type: "GET",
    //             success: function (data2) {
    //                 $(`#audio${currentId}`)[0].src = data2.Location
    //                 $(`#audio${currentId}`)[0].load()

    //                 let masterTime = parseFloat(data.masterTime)
                        
    //                 $(`#audio${currentId}`)[0].currentTime = parseFloat(data.currentTime) + ((new Date().getTime() - masterTime) / 1000)
    //                 $(`#audio${currentId}`)[0].play()
    //             }
    //         })

    //     },
    //     error: function (error) {
    //         console.log(error)
    //     }
    // })
    $("#audio1")[0].play()
}

function playNext() {
    let next = currentId == 2 ? 1 : 2
    $(`#wave${currentId}`).hide()
    $(`#wave${next}`).show()
    $(`#audio${next}`)[0].play()
    song = getNextSong()
    $(`#audio${currentId} source`).attr("src", `${song}`)
    $(`#audio${currentId}`)[0].load()
}

function getNextSong(idToPlace) {
    $.ajax({
        url: "http://localhost:5000/stream/next" + channel, //url = database
        type: "GET",
        success: function (data) {
            //replace the url of source
            $(`#audio${currentId == 2 ? 1 : 2} source`).attr("src", data.url)
            $(`#audio${currentId == 2 ? 1 : 2}`)[0].load()
        },
        error: function (error) {
            console.log(error)
        }
    })
}