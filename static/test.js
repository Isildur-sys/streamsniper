function createTwitchFrame(name) {
    let div = document.createElement("div");
    let ifrm = document.createElement("iframe")
    ifrm.setAttribute("src", "https://player.twitch.tv/?channel=" + name + "&parent=localhost&muted=true");
    ifrm.setAttribute("height", "100%");
    ifrm.setAttribute("width", "100%");
    ifrm.setAttribute("frameborder", "0");
    ifrm.setAttribute("scrolling", "no");
    ifrm.setAttribute("allowfullscreen", "true");
    div.appendChild(ifrm);
    document.getElementById("stream-container").appendChild(div);
}


/* function hello() {
    console.log("hello")
    let div = document.createElement("div") 
} */