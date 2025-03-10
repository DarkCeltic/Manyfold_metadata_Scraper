from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

url = 'https://www.google.com/search?q=allintext%3A'
language = '&lr=lang_en'
sites = '+site%3Aprintables.com+OR+site%3Athingiverse.com+OR+site%3Acults3d.com+OR+site%3Amakerworld.com'


def scrape_google_for_file_info(search_params):
    formatted_response = {}
    api_url = url + search_params + sites + language
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"
    }
    req = Request(api_url, headers=headers)
    # test = req.data
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
        print(api_url)
        return
    return formatted_response
