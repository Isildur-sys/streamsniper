import requests, json
import time

URL_BASE = "https://api.twitch.tv/helix/streams?"
CLIENT_ID = "76pwnuosjagrnba3do7gjnik3uxe53"
CLIENT_SECRET = "jv7fmovp2ie2oe6pk9xurxe01r80wl"
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
                return response_live
        return ""
    except IndexError:
        raise IndexError("Something terribly wrong!")
    except KeyError:
        #send error code upwards
        err = response_json["status"]
        raise KeyError(err)

#usr = get_user("Lonnieyo&user_login=SchrodyCat")
#res = get_response("user_login=summit1g&user_login=laeppastream")
#print(res.text)

#token = requests.post("https://id.twitch.tv/oauth2/token?client_id=76pwnuosjagrnba3do7gjnik3uxe53&client_secret=jv7fmovp2ie2oe6pk9xurxe01r80wl&grant_type=client_credentials")
#access_token = json.loads(token.text)
#head = {"Authorization": "Bearer {}".format(x["access_token"]), "Client-ID": CLIENT_ID}
#res = requests.get("https://api.twitch.tv/helix/streams?user_login=laeppastream", headers=head)
#clean = requests.post("https://id.twitch.tv/oauth2/revoke?client_id=76pwnuosjagrnba3do7gjnik3uxe53&token={}".format(x["access_token"]))
    


