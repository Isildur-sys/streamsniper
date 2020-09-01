let flag = true;

/*Create new window for streamer given as param*/
function createTwitchFrame(name) {
    let div = document.createElement("div");
    let ifrm = document.createElement("iframe");
    ifrm.setAttribute("src", "https://player.twitch.tv/?channel=" + name + "&parent=localhost&muted=true");
    ifrm.setAttribute("height", "100%");
    ifrm.setAttribute("width", "100%");
    ifrm.setAttribute("frameborder", "0");
    ifrm.setAttribute("scrolling", "no");
    ifrm.setAttribute("allowfullscreen", "true");
    div.appendChild(ifrm);
    document.getElementById("stream-container").appendChild(div);
}

function askStreams() {
    var xhttp = new XMLHttpRequest();
    /* xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        // Typical action to be performed when the document is ready:
            
        }
    }; */
    xhttp.open("GET", "/new_stream", true);
    xhttp.onload = () => {
        resp = xhttp.responseText;
        if (resp != "") {
            createTwitchFrame(resp);
        }

    };
    xhttp.send();
    if (flag == true) {
        setTimeout(askStreams, 5000);
    } else {
        flag = true;
    }
    
}


/*Additional start button actionlistener for MainLoop + stop button*/
$(function() {
    $('#stopbtn').bind('click', function() {
        $.get("/stop");
    });
});

$(function() {
    $('#startbtn').bind('click', function() {
        $.ajax({
            type:"GET",
            url:"/background_process",
            contentType: "text/plain",
            success: function (data) {
                flag = false;
            }
        })
        return false;
    });
});


function getGame(game) {
    $.get( "/get_game/" + game.value );
}


/* createTwitchFrame("esl_csgo");
createTwitchFrame("Stewie2K"); */