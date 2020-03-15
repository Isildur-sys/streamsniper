import requests, json

URL_BASE = "https://api.twitch.tv/helix/"
CLIENT_ID = "76pwnuosjagrnba3do7gjnik3uxe53"
HEADERS = {"Client-ID": CLIENT_ID}

#fetch streamer data from twitch

def get_response(user):
    url =  URL_BASE + user
    resp = requests.get(url, headers=HEADERS)
    return resp

def get_user(name):
    return "streams?user_login={0}".format(name)

def print_response(response):
    response_json = response.json()
    print_response = json.dumps(response_json["data"], indent=2)
    print(print_response)

def response_live(response):
    #get response from twitch API
    response_json = response.json()
    try:
        response_live = response_json["data"][0]["type"]
        print(response_live)
    except IndexError:
        print("Player not found or not online")
    except KeyError:
        print("Too many requests")

   
    


