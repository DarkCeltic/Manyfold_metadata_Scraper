from urllib.parse import *

import pymupdf
from selenium.common import SessionNotCreatedException, TimeoutException
from urllib3.exceptions import ReadTimeoutError

from metaDataFiller.customErrors.notAvailableError import notAvailableError
from metaDataFiller.objects.creator import Creator
from metaDataFiller.objects.model import Model
from metaDataFiller.webScrapers import printablesWebScraper


def get_pdf_data(file, model: Model, creator: Creator):
    doc = pymupdf.open(file)
    tmp_model_url = ''

    for page_num in range(doc.page_count):
        page = doc[page_num]
        page_links = page.get_links()
        for link in page_links:
            if link["kind"] == pymupdf.LINK_URI:
                if 'model/' in link["uri"]:
                    tmp_model_url = link["uri"]

    if 'printables' in tmp_model_url:
        parsed = urlparse(tmp_model_url)
        if not parsed.netloc.startswith('www.'):
            parsed = parsed._replace(netloc='www.' + parsed.netloc)
        try:
            printablesWebScraper.scrape_printables(parsed.geturl(), creator, model)
        except (TimeoutException, ReadTimeoutError, SessionNotCreatedException, notAvailableError):
            return
