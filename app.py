from flask import Flask, render_template, request
from webui import WebUI
import requests, json, time
import MainLoop, FetchFromTwitch, FetchDataIngame, json

app = Flask(__name__)
ui = WebUI(app, debug=True)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/stop')
def stop():
    print("Stopping...")
    MainLoop.flag = False
    return ""

@app.route('/background_process')
def background_process():
    MainLoop.runMain()
    MainLoop.flag = True
    return ""
    

@app.route("/get_game/<name>")
def get_game(name):
    FetchFromTwitch.set_current_game(name)
    FetchDataIngame.set_current_game_frame(name)
    return "nothing"


@app.route("/new_stream", methods=["GET"])
def new_stream():
    if len(MainLoop.streamerQue) != 0:
        return MainLoop.streamerQue.pop()
    return ""


if __name__ == "__main__":
    ui.run()
    #app.run(debug=True)