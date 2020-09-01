from flask import Flask, render_template, request
import requests, json, time
import MainLoop, FetchFromTwitch, json

app = Flask(__name__)
streamers = ["esl_csgo", "stewie2K"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/stop')
def stop():
    MainLoop.flag = False
    return ""

@app.route('/background_process')
def background_process():
    MainLoop.runMain()
    return ""
    

@app.route("/get_game/<name>")
def get_game(name):
    FetchFromTwitch.set_current_game(name)
    return "nothing"


@app.route("/new_stream", methods=["GET"])
def new_stream():
    if len(streamers) != 0:
        return streamers.pop()
    return ""

def addToStreamers(name):
    streamers.append(name)


if __name__ == "__main__":
    app.run(debug=True)