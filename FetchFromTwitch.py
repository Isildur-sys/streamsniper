import requests, json

URL_BASE = "https://api.twitch.tv/helix/streams?"
CLIENT_ID = "76pwnuosjagrnba3do7gjnik3uxe53"
HEADERS = {"Client-ID": CLIENT_ID}

#fetch streamer data from twitch

def get_response(users):
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
        raise IndexError("Something terrbily wrong!")
    except KeyError:
        raise KeyError("Too many requests to Twitch API")

#usr = get_user("Lonnieyo&user_login=SchrodyCat")
#res = get_response("user_login=SchrodyCat&user_login=officialandypyro")
#response_live(res)

   
    


