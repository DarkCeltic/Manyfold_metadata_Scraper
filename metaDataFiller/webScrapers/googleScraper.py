import configparser
import json
from collections import defaultdict
from urllib.error import HTTPError
from urllib.parse import quote
from httpx import Client
from parsel import Selector
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = 'https://www.google.com/search?q=allintext%3A'
language = '&lr=lang_en'


def scrape_google_for_file_info(search_params):
    formatted_response = {}
    api_url = url + search_params + language
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }
    req = Request(api_url, headers=headers)
    test = req.data
    response = urlopen(req)
    soup = BeautifulSoup(response, "html.parser")
    heading = soup.find_all('h1')
    for head in heading:
        if head.text == 'Search Results':
            heading = head
            continue
    try:
        results = heading.find_next_siblings('div')

        titleTest = results[0].findChildren('h3')
        title = []
        urls = []
        for t in titleTest:
            title.append(t.text)
            prev = t.parent
            urls.append(prev.get('href'))
    except AttributeError:
        # TODO need some error handling here, or return null
        return
    return formatted_response
