from urllib.parse import *

import pymupdf
from selenium.common import SessionNotCreatedException, TimeoutException
from urllib3.exceptions import ReadTimeoutError

from metaDataFiller.GlobalVariables.Global import add_new_creator_urls, add_new_model_urls, convert_license
from metaDataFiller.webScrapers import printablesWebScraper
from metaDataFiller.objects.creator import Creator
from metaDataFiller.objects.model import Model


def get_pdf_data(file, model: Model, creator: Creator):
    doc = pymupdf.open(file)
    tmp_license = ''
    tmp_model_url = ''
    tmp_creator_url = ''
    tmp_username = ''

    for page_num in range(doc.page_count):
        page = doc[page_num]
        page_links = page.get_links()
        for link in page_links:
            if link["kind"] == pymupdf.LINK_URI:
                if 'creativecommons' in link["uri"]:
                    tmp_license = link["uri"]
                elif 'social' in link["uri"] or '@' in link["uri"]:
                    tmp_creator_url = link["uri"]
                    if '@' in tmp_creator_url:
                        tmp_username = tmp_creator_url.split('@')[1]
                elif 'model/' in link["uri"]:
                    tmp_model_url = link["uri"]
    if tmp_model_url and 'printables' in tmp_model_url:
        parsed = urlparse(tmp_model_url)
        if not parsed.netloc.startswith('www.'):
            parsed = parsed._replace(netloc='www.' + parsed.netloc)
        # try:
        printables_info = printablesWebScraper.scrape_printables(parsed.geturl(), creator, model)
        # except (TimeoutException, ReadTimeoutError,SessionNotCreatedException):
        #     return
        # if printables_info == 'url no longer available':
        #     if 'www' not in tmp_model_url:
        #         parsed_url = urlparse(tmp_model_url)
        #         netloc = 'www.' + parsed_url.netloc
        #         tmp_model_url = urlunparse(parsed_url._replace(netloc=netloc))
        #     add_new_model_urls(tmp_model_url, model)
        #     model.license = convert_license(tmp_license)
        #     if tmp_username:
        #         creator.creatorName = tmp_username
        #     if 'www' not in tmp_creator_url:
        #         parsed_url = urlparse(tmp_creator_url)
        #         netloc = 'www.' + parsed_url.netloc
        #         tmp_creator_url = urlunparse(parsed_url._replace(netloc=netloc))
        #     add_new_creator_urls(tmp_creator_url, creator)
