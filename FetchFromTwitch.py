import requests, json
import time, os

URL_BASE = "https://api.twitch.tv/helix/streams?"
CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")
PUBG_ID = 493057
REALM_ROYALE_ID = 505845

current_game = PUBG_ID #store currently selected game id (initialize to default)

#fetch streamer data from twitch

def get_response(users):
    #request a token and load response as json
    tokenResp = requests.post("https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CLIENT_ID, CLIENT_SECRET))
    token = json.loads(tokenResp.text)

    HEADERS = {"Authorization": "Bearer {}".format(token["access_token"]), "Client-ID": CLIENT_ID}
    url =  URL_BASE + users
    resp = requests.get(url, headers=HEADERS)
    return resp

def print_response(response):
    #for debugging
    response_json = response.json()
    print_response = json.dumps(response_json, indent=2)
    print(print_response)

def response_live(response):
    #get response from twitch API
    response_json = response.json()
    try:
        for i in range(0, len(response_json["data"])):
            response_live = response_json["data"][i]["type"]
            if response_live == "live":
                game_id = int(response_json["data"][i]["game_id"])
                if game_id == current_game:
                    return response_live
        return ""
    except IndexError:
        raise IndexError("Something terribly wrong!")
    except KeyError:
        #send error code upwards
        err = response_json["status"]
        raise KeyError(err)

def set_current_game(game):
    if game == "PUBG":
        current_game = PUBG_ID
        print("Game set to PUBG")
    elif game == "Realm_Royale":
        current_game = REALM_ROYALE_ID
        print("Game set to Realm Royale")

#res = get_response("user_login=dobbydore_")
#print(response_live(res))
    


