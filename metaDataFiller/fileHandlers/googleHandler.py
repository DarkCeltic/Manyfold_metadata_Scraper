import os
from time import sleep

from metaDataFiller.objects.file_lists import nopdforreadme
from metaDataFiller.webScrapers import googleScraper


def google_handler():
    for f in nopdforreadme:
        filename = os.path.basename(f['url'])
        search_params = '"' + filename.split('#')[0].replace(' ', '+') + '"'
        for file in f['files']:
            search_params += '+"' + file.replace(' ', '+') + '"'
        googleScraper.scrape_google_for_file_info(search_params)
        sleep(60)
