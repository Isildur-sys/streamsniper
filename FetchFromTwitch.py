import requests, json

URL_BASE = "https://api.twitch.tv/helix/"
CLIENT_ID = "76pwnuosjagrnba3do7gjnik3uxe53"
HEADERS = {"Client-ID": CLIENT_ID}

def get_response(user):
    url =  URL_BASE + user
    resp = requests.get(url, headers=HEADERS)
    return resp

def get_user(name):
    return "users?login={0}".format(name)

def print_response(response):
    response_json = response.json()
    print_response = json.dumps(response_json, indent=2)
    print(print_response)


