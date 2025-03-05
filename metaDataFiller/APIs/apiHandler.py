import configparser
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Access values from the configuration file
api_key = config.get('Thingiverse_API_Key', 'key')

url = 'https://api.thingiverse.com/things/'
url2 = '?access_token=' + api_key


def thingiverse_api_get_thing(thing_id):
    api_url = url + thing_id + url2
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }
    req = Request(api_url, headers=headers)
    try:
        response = urlopen(req)
    except HTTPError:
        # print('no longer available in Thingiverse')
        return 'no longer available'
    data = json.load(response)
    formatted_response = process_response(data)

    # TODO error handling here
    return formatted_response


def process_response(response):
    return {"creator": response.get("creator").get("name"),
            "creator_urls": [response.get("creator").get("public_url")],
            "model_urls": [response.get("public_url")],
            "license": response.get("license")}
